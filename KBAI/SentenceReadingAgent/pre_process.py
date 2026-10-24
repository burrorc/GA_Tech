import json
import spacy
from nltk.corpus import wordnet as wn

# Used only during preprocessing; not imported by SentenceReadingAgent.py.
nlp = spacy.load("en_core_web_sm")

with open("mostcommon.txt", "r") as file:
    words = [line.strip() for line in file if line.strip()]

AUXILIARIES = {
    "am", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did",
    "can", "could", "will", "would", "may", "might",
    "must", "should"
}

NUMBERS = {
    "one", "two", "three", "four", "five",
    "six", "ten", "hundred", "thousand"
}

AUXILIARY_TYPES = {
    "am": ["AUX", "VERB"],
    "is": ["AUX", "VERB"],
    "are": ["AUX", "VERB"],
    "was": ["AUX", "VERB"],
    "were": ["AUX", "VERB"],
    "be": ["AUX", "VERB"],
    "been": ["AUX", "VERB"],

    "have": ["AUX", "VERB"],
    "has": ["AUX", "VERB"],
    "had": ["AUX", "VERB"],

    "do": ["AUX", "VERB"],
    "does": ["AUX", "VERB"],
    "did": ["AUX", "VERB"],

    "can": ["AUX", "NOUN", "VERB"],
    "will": ["AUX", "NOUN", "VERB"],

    "could": ["AUX"],
    "would": ["AUX"],
    "should": ["AUX"],
    "may": ["AUX"],
    "might": ["AUX"],
    "must": ["AUX"]
}

ADVERBS = {
    "fast", "well", "soon", "often", "always", "never",
    "just", "still", "again", "together", "early", "late"
}

NEGATIVES = {"no", "not", "never", "don't"}

# Curated function-word classifications (and a few specific grammatical forms).
POS_OVERRIDES = {
    # Determiners
    "a": ["DET"],
    "an": ["DET"],
    "the": ["DET"],
    "this": ["DET", "PRON"],
    "that": ["DET", "PRON", "SCONJ"],
    "these": ["DET", "PRON"],
    "those": ["DET", "PRON"],
    "each": ["DET", "PRON"],
    "every": ["DET"],
    "some": ["DET", "PRON"],
    "all": ["DET", "PRON"],
    "my": ["DET"],
    "your": ["DET"],
    "his": ["DET", "PRON"],
    "her": ["DET", "PRON"],
    "our": ["DET"],
    "their": ["DET"],

    # Conjunctions and comparison words
    "and": ["CCONJ"],
    "or": ["CCONJ"],
    "but": ["CCONJ"],
    "if": ["SCONJ"],
    "while": ["SCONJ"],
    "though": ["SCONJ"],
    "than": ["SCONJ", "ADP"],
    "since": ["SCONJ", "ADP", "ADV"],
    "until": ["SCONJ", "ADP"],

    # Prepositions / particles
    "to": ["ADP", "PART"],
    "of": ["ADP"],
    "with": ["ADP"],
    "from": ["ADP"],
    "at": ["ADP"],
    "for": ["ADP"],
    "by": ["ADP"],
    "in": ["ADP", "ADV"],
    "on": ["ADP", "ADV"],
    "under": ["ADP", "ADV"],
    "over": ["ADP", "ADV"],
    "between": ["ADP"],
    "through": ["ADP", "ADV"],
    "against": ["ADP"],
    "toward": ["ADP"],
    "among": ["ADP"],
    "during": ["ADP"],
    "before": ["ADP", "ADV"],
    "after": ["ADP", "ADV"],

    # Pronouns and question words
    "i": ["PRON"],
    "me": ["PRON"],
    "you": ["PRON"],
    "he": ["PRON"],
    "him": ["PRON"],
    "she": ["PRON"],
    "it": ["PRON"],
    "we": ["PRON"],
    "us": ["PRON"],
    "they": ["PRON"],
    "them": ["PRON"],
    "who": ["PRON"],
    "what": ["PRON"],
    "which": ["DET", "PRON"],
    "where": ["ADV"],
    "when": ["ADV", "SCONJ"],
    "why": ["ADV"],
    "how": ["ADV"],

    # Negation / contraction
    "no": ["DET", "ADV"],
    "not": ["PART"],
    "never": ["ADV"],
    "don't": ["AUX"],
}

POS_MAP = {
    wn.NOUN: "NOUN",
    wn.VERB: "VERB",
    wn.ADJ: "ADJ",
    wn.ADV: "ADV",
}

names = sorted(set(words[:20]))
vocabulary = words[20:]
vocabulary = sorted(set(vocabulary) | set(POS_OVERRIDES) | AUXILIARIES | ADVERBS | NEGATIVES)
vocabulary = sorted(set(vocabulary) | {"gone", "store"})
word_data = {}

for word in vocabulary:
    normalized_word = word.lower()
    doc = nlp(word)
    if not doc:
        continue

    if normalized_word.endswith("'s"):
        lemma = normalized_word[:-2]
        # The possessive token is a noun with a possessive marker,
        # not a verb merely because its base has a verb sense.
        possible_pos = {"NOUN", "POSS"}
    else:
        lemma = doc[0].lemma_.lower()
        possible_pos = set()

        # Morphological analysis is POS-specific: it doesn't blindly
        # transfer every lexical sense of the spaCy lemma.
        for wordnet_pos, grammatical_type in POS_MAP.items():
            if wn.morphy(normalized_word, wordnet_pos):
                possible_pos.add(grammatical_type)

        if normalized_word in AUXILIARIES:
            possible_pos.add("AUX")
        if normalized_word in ADVERBS:
            possible_pos.add("ADV")

        if normalized_word in POS_OVERRIDES:
            possible_pos = set(POS_OVERRIDES[normalized_word])

        if normalized_word in AUXILIARY_TYPES:
            possible_pos = set(AUXILIARY_TYPES[normalized_word])

        if normalized_word in NUMBERS:
            possible_pos.add("NUM")

    word_data[word] = {
        "lemma": lemma,
        "pos": sorted(possible_pos) if possible_pos else ["UNKNOWN"],
    }

with open("vocabulary_analysis.json", "w") as file:
    json.dump({"names": names, "words": word_data}, file, indent=2)

lemmas = {
    word.lower(): data["lemma"]
    for word, data in word_data.items()
    if word.lower() != data["lemma"]
}
word_types = {word.lower(): data["pos"] for word, data in word_data.items()}

with open("knowledge_base.py", "w") as file:
    file.write("# Preprocessed vocabulary data\n")
    file.write("# WordNet 3.0 Copyright 2006 Princeton University\n\n")
    file.write(f"NAMES = {repr(names)}\n\n")
    file.write(f"LEMMAS = {repr(lemmas)}\n\n")
    file.write(f"WORD_TYPES = {repr(word_types)}\n\n")
    file.write(f"AUXILIARIES = {repr(sorted(AUXILIARIES))}\n\n")
    file.write(f"ADVERBS = {repr(sorted(ADVERBS))}\n\n")
    file.write(f"NEGATIVES = {repr(sorted(NEGATIVES))}\n")

print(f"Processed {len(word_data)} vocabulary entries.")
for word in ["brought", "went", "ran", "came", "note", "walk", "short", "to", "than", "since", "until", "dog's"]:
    print(f"{word}: {word_data.get(word)}")

unknown_words = [
    word for word, data in word_data.items() if data["pos"] == ["UNKNOWN"]
]
print("Words needing review:", unknown_words)
