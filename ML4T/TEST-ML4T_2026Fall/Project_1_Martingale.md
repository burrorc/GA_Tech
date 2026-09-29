# Project 1: Martingale

**Course:** Machine Learning for Trading (ML4T)  
**Assignment:** Project 1: Martingale (Report)  
**Due:** September 7 at 8:00 AM  
**Points:** 100  
**Submission:** File upload  
**Report file type:** PDF

---

## Revision History

This assignment is subject to change up until 3 weeks before the due date. Changes, if any, will be logged in the assignment.

1. Published — Start of Term

---

# 1. Overview

In this course, you are building a simplified AI-based trading system. The system is constructed over 8 projects, with each project contributing toward a more intricate system combining machine learning with practical algorithmic trading strategies.

For Project 1, you will write software that performs probabilistic experiments involving an **American Roulette wheel**. The project is intended to give you an initial feel for risk, probability, and betting.

You will:

- Submit your code to **Gradescope SUBMISSION**
- Submit a **report** to Canvas discussing your experimental findings

Course project overview:

- Machine Learning for Trading Project page:  
  https://gatech.instructure.com/courses/536288/pages/machine-learning-for-trading-project

Roulette reference:

- https://en.wikipedia.org/wiki/Roulette

## 1.1 Learning Objectives

### Mathematical Tools

Develop an understanding of probabilistic and statistical tools associated with machine learning, including:

- Expectations
- Standard deviations
- Sampling
- Minimum values
- Maximum values
- Convergence

### Research

Gain experience researching conceptual and programming material needed to successfully complete the assignment.

### Programming & Academic Writing

Assignments build upon one another. Techniques involving:

- Experimentation
- Graphs
- Interpretation
- Analysis

will continue to matter in future projects.

### Course Conduct

Practice:

- Developing and testing code locally in the Conda `ml4t` environment
- Pre-validating in **Gradescope TESTING**
- Submitting final code to **Gradescope SUBMISSION**

---

# 2. About the Project

You will build a **Simple Gambling Simulator** by modifying `martingale.py`.

The simulator will model **1000 successive bets** on an American roulette wheel.

Each series of 1000 successive bets is called an **episode**.

Use successive calls to:

```python
get_spin_result(win_prob)
```

You must set `win_prob` to the correct probability of winning a bet on black using an American roulette wheel.

## Martingale Betting Strategy

The assignment provides the following strategy:

```text
episode_winnings = $0

while episode_winnings < $80:
    won = False
    bet_amount = $1

    while not won:
        wager bet_amount on black
        won = result of roulette wheel spin

        if won == True:
            episode_winnings = episode_winnings + bet_amount
        else:
            episode_winnings = episode_winnings - bet_amount
            bet_amount = bet_amount * 2
```

### Even-money roulette bet

Betting on black or red is an **even-money** bet:

- If you bet `N` and win, your net winnings increase by `N`.
- If you bet `N` and lose, your net winnings decrease by `N`.

This project assumes an **American roulette wheel**.

---

# 3. Your Implementation

Implement the simulator and conduct the required experiments.

Before the deadline:

1. Test locally
2. Submit to **Gradescope TESTING**
3. Once satisfied, submit to **Gradescope SUBMISSION**

> Only code submitted to **Gradescope SUBMISSION** will be graded. Submitting only to TESTING results in a zero.

---

## 3.1 Getting Started

The starter framework assumes your ML4T development environment is already configured.

Project framework:

- `martingale_2026Fall.zip`
- Canvas / course-provided download
- Dropbox version provided by the course

Extract the project so your ML4T directory contains a `martingale` folder.

Inside the folder is:

```text
martingale/
└── martingale.py
```

You must modify:

```text
martingale.py
```

The file must remain in the `martingale` directory.

Run it from inside that directory with:

```bash
PYTHONPATH=../:. python martingale.py
```

---

## 3.2 Experiment 1 — Explore the Strategy and Create Charts

Experiment 1 uses Professor Balch's original Martingale betting strategy with an **unlimited bankroll**.

The methodology is a **Monte Carlo simulation**: repeatedly run randomized simulations and evaluate the aggregate results.

### Figure 1

Run the simple simulator for **10 episodes**.

Requirements:

- Start winnings at `0` each episode
- Plot all 10 episodes on one chart
- X-axis range: `0` to `300`
- Y-axis range: `-256` to `+100`

Some lines may exceed the plot bounds.

### Figure 2

Run the simple simulator for **1000 episodes**.

For each spin number:

- Compute the **mean** winnings across the 1000 episodes
- Plot the mean
- Plot:
  - `mean + standard deviation`
  - `mean - standard deviation`

Use the same axis bounds as Figure 1.

### Figure 3

Use the **same data as Figure 2**.

For each spin number:

- Compute the **median**
- Plot the median
- Plot:
  - `median + standard deviation`
  - `median - standard deviation`

Use the same axis bounds.

### Stopping at $80

If the target of `$80` winnings is reached:

- Stop betting
- Carry the final value forward for all remaining spins

Example:

```text
..., 78, 79, 80, 80, 80, 80, ...
```

If the final win places the gambler above `$80`, carry that value forward instead.

### Chart Requirements

All charts must:

- Be generated using Matplotlib
- Have appropriate titles
- Have labeled axes
- Have legends
- Use consistent axis ranges

The charts must be included in the report with supporting analysis and discussion.

---

## 3.3 Experiment 2 — A More Realistic Gambling Simulator

Experiment 2 adds a realistic bankroll constraint.

The gambler begins with a **$256 bankroll**.

Therefore:

- Maximum retained winnings: `$80`
- Maximum possible loss: `-$256`

### Bankrupt condition

If:

```text
episode_winnings == -256
```

then:

- Stop betting
- Carry `-256` forward for all remaining spins

### Partial-bet corner case

Suppose the Martingale strategy says the next bet should be `$N`, but the gambler has only `$M` remaining, where:

```text
M < N
```

The gambler may only wager `$M`.

In other words:

```python
actual_bet = min(intended_bet, bankroll_remaining)
```

### Figure 4

Run the realistic simulator for **1000 episodes**.

For each spin:

- Plot mean winnings
- Plot `mean + standard deviation`
- Plot `mean - standard deviation`

Use the same axis bounds as Figure 1.

### Figure 5

Use the **same data as Figure 4**.

For each spin:

- Plot median winnings
- Plot `median + standard deviation`
- Plot `median - standard deviation`

Use the same axis bounds.

### Chart Requirements

All charts must:

- Be generated using Matplotlib
- Have appropriate titles
- Have labeled axes
- Have legends
- Use consistent axis ranges

---

## 3.4 Technical Requirements

1. `martingale.py` must implement the course API specification.

2. All winnings must be stored in a **NumPy array**.

   Example concept:

   ```python
   winnings[0] = 0
   winnings[1] = winnings_after_first_spin
   winnings[2] = winnings_after_second_spin
   ```

3. Use the **population standard deviation**.

   The plotted lines are:

   ```text
   center + stdev
   center - stdev
   ```

4. You may set a specific random seed.

   If you do:

   - Call the seed only **once**
   - Use your **GT ID as the numeric seed**
   - A starting seed is strongly recommended for reproducibility

5. You may optionally write statistics, tables, or text output to:

   ```text
   p1_results.txt
   ```

   or:

   ```text
   p1_results.html
   ```

   If used, the file(s) must be created in the same folder as the `.py` file being run.

6. You must implement:

   ```python
   author()
   ```

   and:

   ```python
   study_group()
   ```

---

## 3.5 Notes and Hints

### 3.5.1 Structuring the NumPy Array

A useful structure is:

```text
                Spin[0]  Spin[1]  Spin[2]  ... Spin[1000]
Episode[0]         0        ...      ...          ...
Episode[1]         0        ...      ...          ...
Episode[2]         0        ...      ...          ...
...
```

Each row represents one episode.

Each episode contains:

- Initial winnings value at spin 0
- Results for up to 1000 spins

Therefore, each row has **1001 entries**.

Conceptually:

```python
winnings.shape == (num_episodes, 1001)
```

Statistics such as the mean, median, and standard deviation can then be calculated **column-wise** across all episodes.

### 3.5.2 Expectations

An expectation can be thought of as an arithmetic mean:

```text
E[X] = Σx x P[X = x]
```

Given a distribution `X`, the expected value is the weighted sum of each possible value multiplied by its probability.

Suggested references from the assignment:

- Foundation of Machine Learning, Appendix C  
  https://cs.nyu.edu/~mohri/mlbook/
- Mitchell's *Machine Learning*, chapter 5.3
- Probabilistic Machine Learning, chapter 2.2.5  
  https://probml.github.io/pml-book/book1.html

---

# 4. Contents of the Report — 100 Points

In addition to code, you must write a report describing:

- Experimental hypotheses
- Experimental design
- Findings
- Analysis

The results and analysis must be based on **experimental observation**, although theoretical or mathematical arguments may also support your analysis.

Your submitted code must contain everything necessary to generate the charts used in the report.

> Up to 30 points may be deducted from the report score for unmet implementation requirements or code that fails to run.

## Report Format

Use the course-provided **JDF format**.

Do not alter its required:

- Font sizes
- Margins

Charts must:

- Be generated by the code
- Be saved as `.png`
- Be saved in either:
  - the current project directory, or
  - `./images`
- Be inserted into the report without additional post-processing/editing
- Have legible titles, labels, and legends
- Use the same axis bounds

### Maximum report length

**7 pages maximum**, excluding references.

Content beyond 7 pages will not be considered for grading.

---

## Report Questions

### Question Set 1

For **Experiment 1**:

Calculate and provide the **estimated probability of winning exactly $80 within 1000 sequential bets**.

Thoroughly explain your reasoning using the experiment output.

Do **not** estimate the answer by visually inspecting the plots.

Use simulation output/data.

---

### Question 2

For **Experiment 1**:

What is the **estimated expected value of winnings after 1000 sequential bets**?

Thoroughly explain your reasoning.

---

### Question Set 3

For **Experiment 1**:

1. Do the upper standard deviation line (`mean + stdev`) and lower standard deviation line (`mean - stdev`) stabilize at a maximum or minimum value?
2. Do the standard deviation lines converge toward one another as the number of sequential bets increases?

Thoroughly explain why or why not.

---

### Question 4

For **Experiment 2**:

Calculate and provide the **estimated probability of winning exactly $80 within 1000 sequential bets**.

Thoroughly explain your reasoning using the experiment output.

Do **not** estimate the answer by visually inspecting the plots.

---

### Question 5

For **Experiment 2**:

What is the **estimated expected value of winnings after 1000 sequential bets**?

Thoroughly explain your reasoning.

---

### Question Set 6

For **Experiment 2**:

1. Do the upper standard deviation line (`mean + stdev`) and lower standard deviation line (`mean - stdev`) stabilize at a maximum or minimum value?
2. Do the standard deviation lines converge toward one another as the number of sequential bets increases?

Thoroughly explain why or why not.

---

### Question 7

What are some benefits of using **expected values** when conducting experiments instead of simply using the result of one specific random episode?

---

## Clarification on Convergence vs. Stabilization

The assignment distinguishes these terms:

### Convergence

The upper and lower standard-deviation lines move toward one another and appear to merge.

### Stabilization

A line levels off and remains around a particular value.

You can have:

- Stabilization without convergence
- Convergence without stabilization
- Both
- Neither

If lines stabilize or converge, discuss the approximate value(s) where that behavior occurs.

If they do not, explain why.

---

# 5. Testing Recommendations

No separate local testing script is provided.

Test the assignment from within the `martingale` directory using:

```bash
PYTHONPATH=../:. python martingale.py
```

The grader will invoke the `__main__` section using that command.

The program should:

- Run completely
- Produce all required output
- Generate all required charts

## Gradescope TESTING

You are encouraged to submit to **Gradescope TESTING**.

Important:

- TESTING performs basic pre-validation
- TESTING does **not** grade the assignment
- You may submit to TESTING an unlimited number of times
- Code that does not pass the provided validations will not be eligible for regrade requests

---

# 6. Submission Requirements

This is an **individual assignment**.

All submitted work must be your own.

Cite any sources you use, and use quotes/in-line citations for direct quotations.

## Due-date behavior

Canvas displays the assignment deadline converted from:

```text
23:59 AOE
```

to your configured Canvas time zone.

Late assignments are generally not accepted without advance agreement, except for medical or family emergencies handled through the Dean of Students process.

---

## 6.1 Report Submission

Use JDF format and submit:

```text
p1_martingale_report.pdf
```

Submit the PDF to **Canvas**.

Submit only this one report file.

Do **not** separately submit chart image files.

However, your code must generate and save all five required `.png` figures when it runs.

Canvas allows unlimited report submissions.

---

## 6.2 Code Submission

Submit this file to **Gradescope SUBMISSION**:

```text
martingale.py
```

Do not submit any other code files.

Important:

- Only Gradescope SUBMISSION is graded
- Code that crashes in SUBMISSION receives a zero
- Test locally and in TESTING before making the final submission
- You are allowed a **maximum of 5 code submissions** to Gradescope SUBMISSION

---

# 7. Grading Information

The report is worth **100% of the assignment grade**.

The report is graded on a 100-point scale.

The submitted code is executed as a batch job after the project deadline.

All assignment points are returned through the Canvas report score.

---

## 7.1 Grading Rubric

### 7.1.1 Report

Possible deductions include:

- Up to `-5` points for each incorrect answer
- Up to `-5` points for each question whose reasoning is incorrect or insufficiently supported
- Up to `-8` points for each chart that is missing or incorrect, or lacks:
  - title
  - labeled axes
  - legend
- Up to `-100` points if the report does not reflect project requirements
- Up to `-100` points if the required report is not provided

### 7.1.2 Code

Possible deductions include:

- `-20` if the code does not produce all charts as `.png` files in one run
- `-20` if the code displays charts in a window or on screen
- `-20` if the code saves content outside the project directory
- Up to `-100` if the code fails to execute completely
- Up to `-100` if the code does not reflect project requirements
- Up to `-100` if required code is missing, including code needed to recreate the charts

### 7.1.3 Auto-Grader

A private grading script is **not used** for this project.

When the instructions say "up to -X points," assume the full deduction may be applied.

---

# 8. Development Guidelines — Allowed & Prohibited

Follow the course-wide:

**Course Development Recommendations, Guidelines, and Rules**

Project-specific exemptions:

```text
N/A
```

---

# 9. Additional Resources

Suggested resources from the assignment:

- Wikipedia — Expected Value  
  https://en.wikipedia.org/wiki/Expected_value

- Martelli, A., Ravenscroft, A., and Holden, S. (2017)  
  *Python in a Nutshell*, 3rd Edition  
  https://learning.oreilly.com/library/view/python-in-a/9781491913833/

- James, G., Witten, D., Hastie, T., Tibshirani, R. (2017)  
  *An Introduction to Statistical Learning*, Chapter 2  
  https://www.statlearning.com/

- Murphy, K. (2021)  
  *Probabilistic Machine Learning: An Introduction*, Chapter 2  
  https://probml.github.io/pml-book/book1.html

---

# Quick Reference Checklist

## Simulator

- [ ] American roulette probability used correctly
- [ ] `get_spin_result(win_prob)` used for spins
- [ ] Start each episode at `$0`
- [ ] Up to `1000` bets per episode
- [ ] Stop once winnings reach at least `$80`
- [ ] Fill remaining values forward
- [ ] Experiment 2 stops at `-$256`
- [ ] Experiment 2 prevents betting more money than remains

## NumPy

- [ ] Winnings stored in NumPy arrays
- [ ] Initial value stored at index `0`
- [ ] 1001 columns per full episode
- [ ] Population standard deviation used

## Experiment 1

- [ ] Figure 1 — 10 individual episodes
- [ ] Figure 2 — 1000 episodes, mean ± stdev
- [ ] Figure 3 — same data, median ± stdev

## Experiment 2

- [ ] `$256` bankroll
- [ ] Figure 4 — 1000 episodes, mean ± stdev
- [ ] Figure 5 — same data, median ± stdev

## All Figures

- [ ] Matplotlib
- [ ] X-axis: `0–300`
- [ ] Y-axis: `-256–100`
- [ ] Title
- [ ] X-axis label
- [ ] Y-axis label
- [ ] Legend
- [ ] Same axis bounds
- [ ] Saved as `.png`
- [ ] No plot window displayed

## APIs / Code

- [ ] `author()`
- [ ] `study_group()`
- [ ] Code runs with:

```bash
PYTHONPATH=../:. python martingale.py
```

## Report

- [ ] JDF format
- [ ] 7 pages maximum, excluding references
- [ ] All 5 charts included
- [ ] All 7 question sets answered
- [ ] Answers supported by experimental evidence

## Submission

### Canvas

```text
p1_martingale_report.pdf
```

### Gradescope SUBMISSION

```text
martingale.py
```

- [ ] Tested locally
- [ ] Tested in Gradescope TESTING
- [ ] Final code submitted to Gradescope SUBMISSION
- [ ] No more than 5 SUBMISSION attempts
