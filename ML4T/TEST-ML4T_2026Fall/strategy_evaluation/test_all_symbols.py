"""Standalone exploratory ML4T P8 comparison; not part of the submission.
Run from strategy_evaluation: PYTHONPATH=../:. python test_all_symbols.py --data-dir ../data
Uses the existing strategies unchanged; no random seed is set here.
"""
import argparse
import datetime as dt
import os
from pathlib import Path
import time
import warnings

import numpy as np
import pandas as pd

IS = (dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31))
OOS = (dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31))
SV = 100000
EPS = 1e-10


def category(symbol):
    if symbol.startswith(('ML4T-', 'SINE_', 'FAKE')):
        return 'course_test_series'
    if symbol.startswith('$'):
        return 'index'
    return 'market_symbol'  # includes ETFs and other listed instruments


def winner(a, b):
    if abs(a - b) <= EPS:
        return 'Tie'
    return 'Learner' if a > b else 'Manual'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', default=os.environ.get('MARKET_DATA_DIR', '../data'))
    parser.add_argument('--group', choices=['all', 'market', 'test', 'index'], default='all')
    parser.add_argument('--symbols', nargs='+', help='Optional explicit symbol list')
    parser.add_argument('--runs', type=int, default=1, help='Independent learner fits per symbol')
    parser.add_argument('--commission', type=float, default=9.95)
    parser.add_argument('--impact', type=float, default=0.005)
    parser.add_argument('--output', default='all_symbol_results')
    args = parser.parse_args()
    if args.runs < 1 or not np.isfinite([args.commission, args.impact]).all() or min(args.commission, args.impact) < 0:
        parser.error('Use at least one run and finite, nonnegative costs.')
    data_dir = Path(args.data_dir).expanduser().resolve()
    if not (data_dir / 'SPY.csv').is_file():
        parser.error(f'SPY.csv not found in {data_dir}; specify the course data directory.')
    os.environ['MARKET_DATA_DIR'] = str(data_dir)
    # Import after setting the data path, so util uses the same directory.
    from util import get_data
    import ManualStrategy as ms
    import StrategyLearner as sl
    import marketsimcode as msc
    import indicators as ind

    symbols = sorted(set(args.symbols or [p.stem for p in data_dir.glob('*.csv')]))
    groups = {'market': 'market_symbol', 'test': 'course_test_series', 'index': 'index'}
    if args.group != 'all':
        symbols = [s for s in symbols if category(s) == groups[args.group]]
    if not symbols:
        parser.error('No matching symbols.')
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    # Prevent an accidental mixture of different experiments.
    outputs = [out / n for n in ('runs.csv', 'skipped.csv', 'ranking.csv', 'summary.csv', 'summary.txt')]
    if any(p.exists() for p in outputs):
        parser.error(f'Output files already exist in {out}; choose a new --output directory.')

    calendar = {}
    for name, (sd, ed) in [('IS', IS), ('OOS', OOS)]:
        calendar[name] = get_data(['SPY'], pd.date_range(sd, ed)).index
        if len(calendar[name]) == 0:
            raise RuntimeError(f'No SPY trading days in {name}')

    def check_data(symbol, name, period):
        sd, ed = period
        prices, features = ind.get_features(symbol, sd, ed)
        idx = calendar[name]
        if not prices.index.equals(idx) or not features.index.equals(idx):
            raise ValueError(f'{name}: trading dates differ from SPY calendar')
        valid = np.isfinite(prices.to_numpy()) & (prices.to_numpy() > 0)
        if not valid.all():
            raise ValueError(f'{name}: {int((~valid).sum())} missing/nonpositive/nonfinite prices; full coverage required')
        # Missing warmup features are allowed; the existing strategies handle them.
        if not np.isfinite(features.to_numpy()).all(axis=1).any():
            raise ValueError(f'{name}: no valid feature rows')
        return prices, features

    def evaluate(trades, symbol, name):
        if not trades.index.equals(calendar[name]) or list(trades.columns) != [symbol]:
            raise ValueError(f'{name}: unexpected trade dates or columns')
        orders = trades[symbol]
        if not orders.isin([-2000, -1000, 0, 1000, 2000]).all() or not orders.cumsum().isin([-1000, 0, 1000]).all():
            raise ValueError(f'{name}: illegal orders or holdings')
        values = msc.compute_portvals(trades, SV, args.commission, args.impact)
        if not values.index.equals(calendar[name]) or not np.isfinite(values.to_numpy()).all():
            raise ValueError(f'{name}: invalid portfolio values')
        if values.iloc[0, 0] <= 0:
            raise ValueError(f'{name}: nonpositive initial portfolio value; CR undefined or misleading')
        stats = msc.get_stats(values)
        if not np.isfinite(stats['CR']):
            raise ValueError(f'{name}: nonfinite cumulative return')
        return {'CR': stats['CR'], 'SDDR': stats['SDDR'], 'ADR': stats['ADR'],
                'Trades': int(orders.ne(0).sum()), 'CashDays': int(orders.cumsum().eq(0).sum()),
                'EndingValue': float(values.iloc[-1, 0]), 'NonpositiveDays': int(values.iloc[:, 0].le(0).sum())}

    rows, skipped = [], []
    start = time.perf_counter()
    periods = [('IS', IS), ('OOS', OOS)]
    for i, symbol in enumerate(symbols, 1):
        group = category(symbol)
        try:
            if not (data_dir / (symbol + '.csv')).is_file():
                raise FileNotFoundError('Symbol CSV missing')
            train_prices, train_features = check_data(symbol, 'IS', IS)
            check_data(symbol, 'OOS', OOS)
            manual = ms.ManualStrategy(impact=args.impact, commission=args.commission)
            fixed = {}
            for name, (sd, ed) in periods:
                fixed[name] = {'Manual': evaluate(manual.testPolicy(symbol, sd, ed, SV), symbol, name),
                               'Benchmark': evaluate(msc.get_benchmark(symbol, sd, ed), symbol, name)}
            for run in range(1, args.runs + 1):
                try:
                    learner = sl.StrategyLearner(impact=args.impact, commission=args.commission)
                    labels = learner.get_labels(train_prices)
                    valid = train_features.notna().all(axis=1) & labels.notna()
                    if not valid.any():
                        raise ValueError('No valid training labels')
                    learner.add_evidence(symbol, *IS, SV)
                    row = {'Symbol': symbol, 'Group': group, 'Run': run, 'Impact': args.impact,
                           'Commission': args.commission, 'TrainingRows': int(valid.sum())}
                    for name, (sd, ed) in periods:
                        result = dict(fixed[name])
                        result['Learner'] = evaluate(learner.testPolicy(symbol, sd, ed, SV), symbol, name)
                        for strategy, stats in result.items():
                            for metric, value in stats.items():
                                row[f'{name}_{strategy}_{metric}'] = value
                        a, b = result['Learner']['CR'], result['Manual']['CR']
                        row[f'{name}_ExcessCR'] = a - b
                        row[f'{name}_Winner'] = winner(a, b)
                    rows.append(row)
                except Exception as exc:
                    skipped.append({'Symbol': symbol, 'Group': group, 'Run': run, 'Reason': f'{type(exc).__name__}: {exc}'})
            successful = [r for r in rows if r['Symbol'] == symbol]
            if successful:
                mean = np.mean([r['OOS_ExcessCR'] for r in successful])
                print(f'[{i}/{len(symbols)}] {symbol}: {len(successful)}/{args.runs} runs; OOS learner minus manual {mean:+.2%}', flush=True)
            else:
                print(f'[{i}/{len(symbols)}] {symbol}: all runs failed', flush=True)
        except Exception as exc:
            skipped.append({'Symbol': symbol, 'Group': group, 'Run': 'all', 'Reason': f'{type(exc).__name__}: {exc}'})
            print(f'[{i}/{len(symbols)}] {symbol}: skipped ({exc})', flush=True)
        # Save progress after each symbol, including failures.
        pd.DataFrame(rows).to_csv(outputs[0], index=False, float_format='%.10f')
        pd.DataFrame(skipped, columns=['Symbol', 'Group', 'Run', 'Reason']).to_csv(outputs[1], index=False)

    if not rows:
        print('No successful comparisons. See skipped.csv.'); return
    df = pd.DataFrame(rows)
    # Each symbol receives equal weight, regardless of number of successful fits.
    rank = df.groupby(['Group', 'Symbol']).size().rename('SuccessfulRuns').to_frame()
    for name, _ in periods:
        for strategy in ('Manual', 'Learner', 'Benchmark'):
            for metric in ('CR', 'SDDR', 'Trades', 'CashDays'):
                col = f'{name}_{strategy}_{metric}'
                rank[col] = df.groupby(['Group', 'Symbol'])[col].mean()
        rank[f'{name}_ExcessCR'] = rank[f'{name}_Learner_CR'] - rank[f'{name}_Manual_CR']
        rank[f'{name}_Winner'] = [winner(a, b) for a, b in zip(rank[f'{name}_Learner_CR'], rank[f'{name}_Manual_CR'])]
        rank[f'{name}_LearnerWinRate'] = df.assign(win=df[f'{name}_Winner'].eq('Learner')).groupby(['Group', 'Symbol'])['win'].mean()
    rank = rank.reset_index().sort_values('OOS_ExcessCR', ascending=False)
    rank.to_csv(outputs[2], index=False, float_format='%.10f')
    summaries = []
    for group, sub in [('all', rank)] + list(rank.groupby('Group')):
        for name, _ in periods:
            w = sub[f'{name}_Winner']
            summaries.append({'Group': group, 'Period': name, 'Symbols': len(sub),
                              'LearnerWins': int(w.eq('Learner').sum()), 'ManualWins': int(w.eq('Manual').sum()),
                              'Ties': int(w.eq('Tie').sum()), 'LearnerWinRate': w.eq('Learner').mean(),
                              'MeanLearnerCR': sub[f'{name}_Learner_CR'].mean(),
                              'MeanManualCR': sub[f'{name}_Manual_CR'].mean(),
                              'MeanBenchmarkCR': sub[f'{name}_Benchmark_CR'].mean(),
                              'MeanExcessCR': sub[f'{name}_ExcessCR'].mean(),
                              'LearnerBeatsBenchmark': int((sub[f'{name}_Learner_CR'] > sub[f'{name}_Benchmark_CR'] + EPS).sum()),
                              'LearnerNoTrades': int(sub[f'{name}_Learner_Trades'].eq(0).sum())})
    summary = pd.DataFrame(summaries)
    summary.to_csv(outputs[3], index=False, float_format='%.6f')
    cols = ['Symbol', 'Group', 'OOS_Manual_CR', 'OOS_Learner_CR', 'OOS_Benchmark_CR', 'OOS_ExcessCR']
    report = (f'Discovered/requested symbols: {len(symbols)}\nSuccessful symbols: {len(rank)}\n'
              f'Failed/skipped symbols (no successful runs): {len(symbols)-len(rank)}\n'
              f'Successful fits: {len(df)}; requested fits per symbol: {args.runs}\n'
              f'Commission: {args.commission}; impact: {args.impact}\n'
              f'Elapsed seconds: {time.perf_counter()-start:.1f}\n\n'
              'Win rates compare mean cumulative returns per symbol, not pooled portfolio returns.\n'
              'Full SPY-calendar coverage required in both periods. No price filling or retuning.\n'
              'Course test series and indices are reported separately from market symbols.\n\n'
              + summary.to_string(index=False, float_format=lambda x: f'{x:.6f}')
              + '\n\nTop 20 out-of-sample learner advantages (all groups):\n'
              + rank[cols].head(20).to_string(index=False, float_format=lambda x: f'{x:.6f}')
              + '\n\nTop 20 out-of-sample learner advantages (market symbols):\n'
              + rank.loc[rank.Group.eq('market_symbol'), cols].head(20).to_string(index=False, float_format=lambda x: f'{x:.6f}') + '\n')
    outputs[4].write_text(report)
    print('\n' + report)


if __name__ == '__main__':
    main()
