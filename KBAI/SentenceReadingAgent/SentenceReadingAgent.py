import re
from knowledge_base import NAMES, LEMMAS, WORD_TYPES, AUXILIARIES, ADVERBS, NEGATIVES

class SentenceReadingAgent:
    def __init__(self):
        self.names = set(NAMES)
        self.lemmas = LEMMAS
        self.word_types = WORD_TYPES
        self.auxiliaries = set(AUXILIARIES)
        self.adverbs = set(ADVERBS)
        self.negatives = set(NEGATIVES)
        self.determiners = {
            "a", "an", "the", "this", "that",
            "these", "those", "each", "every",
            "some", "all", "my", "your",
            "his", "her", "our", "their"
        }


    def tokenize_text(self, text):
        pattern = r"\d{1,2}:\d{2}(?:AM|PM)?|[A-Za-z]+(?:'[A-Za-z]+)?"
        return re.findall(pattern, text, flags=re.IGNORECASE)

    def normalize_word(self, word):
        word = word.lower()
        return self.lemmas.get(word, word)

    def classify_word(self, word):
        if (word in self.names):
            return["PROPN"]

        if re.fullmatch(r"\d{1,2}:\d{2}(?:AM|PM)?",word,flags=re.IGNORECASE):
            return ["TIME"]

        if word.lower() in self.determiners:
          types = self.word_types.get(word.lower(), [])
          return sorted(set(types) | {"DET"})

        return self.word_types.get(word.lower(), ["UNKNOWN"])

    
    def get_noun_segments(self, text, tokens):
        segments = []
        current_index = 0

        while( current_index < len(tokens)):
            word = tokens[current_index]
            types = self.classify_word(word)

            if ("NOUN" not in types and "PROPN" not in types and "PRON" not in types):
                current_index += 1
                continue

            start = current_index
            determiner = None
            modifiers = []

            previous_index = current_index - 1

            while( previous_index >= 0):
                previous_word = tokens[previous_index]
                previous_types = self.classify_word(previous_word)

                if ("ADJ" in previous_types or "NUM" in previous_types or "POSS" in previous_types):
                    modifiers.insert(0, previous_word)
                    start = previous_index
                    previous_index -= 1
                    continue

                if("DET" in previous_types):
                    determiner = previous_word
                    start = previous_index
                    break

                break

            segments.append({
                "start": start,
                "end": current_index,
                "key_index": current_index,
                "base": self.normalize_word(word),
                "original": word,
                "determiner": determiner,
                "modifiers": modifiers
            })

            current_index += 1

        return segments         


    def get_verb_segments(self, text, tokens):
        segments = []
        current_index = 0

        while (current_index < len(tokens)):
            word = tokens[current_index]
            types = self.classify_word(word)

            if("VERB" not in types and "AUX" not in types):
                current_index +=1
                continue

            start = current_index
            auxiliaries = []
            modifiers = []
            negative= False

            previous_index = current_index-1

            while(previous_index >=0):
                previous_word = tokens[previous_index]
                previous_types = self.classify_word(previous_word)

                if(previous_word.lower() in self.negatives):
                    negative = True

                    if "AUX" in previous_types:
                      auxiliaries.insert(0, previous_word)

                    start = previous_index
                    previous_index -=1
                    continue

                if("ADV" in previous_types):
                    modifiers.insert(0, previous_word)
                    start = previous_index
                    previous_index -= 1
                    continue

                if("AUX" in previous_types):
                    auxiliaries.insert(0, previous_word)
                    start = previous_index
                    previous_index -= 1
                    continue

                break

            # don't forget that verbs can have following moidifiers
            end = current_index
            next_index = current_index+1

            while(next_index < len(tokens)):
                 next_word = tokens[next_index]
                 next_types = self.classify_word(next_word)
                 if("ADV" in next_types):
                     modifiers.append(next_word)
                     end = next_index
                     next_index+=1
                     continue

                 break

            segments.append({
                  "start": start,
                  "end": end,
                  "key_index": current_index,
                  "base": self.normalize_word(word),
                  "original": word,
                  "auxiliaries": auxiliaries,
                  'modifiers': modifiers,
                  "negative": negative
              })


            current_index += 1

        return segments

    
    def get_preposition_segments(self, text, tokens, noun_segments):
        segments = []
        current_index = 0

        while(current_index <len(tokens)):
            word = tokens[current_index]
            types = self.classify_word(word)

            if("ADP" not in types):
                current_index +=1
                continue

            for noun_segment in noun_segments:
                if(noun_segment["start"] != current_index+1):
                    continue

                segments.append({
                    "start": current_index,
                    "end": noun_segment["end"],
                    "key_index": current_index,
                    "base": self.normalize_word(word),
                    "original": word,
                    "object_index": noun_segment["key_index"]
                  })
            
            current_index +=1

        return segments


    def filter_segments(self, tokens, noun_segments, verb_segments, preposition_segments):
        prep_object_indices = set()

        for preposition in preposition_segments:
            prep_object_indices.add(preposition["object_index"])

        filtered_nouns = []

        for noun in noun_segments:
            if(noun["key_index"] not in prep_object_indices):
                filtered_nouns.append(noun)

        resolved_nouns = []

        for noun in filtered_nouns:
            is_contained = False

            for other in filtered_nouns:
                if noun is other:
                    continue

                if(other["start"] <= noun["start"] and other["end"] >= noun["end"] and (other["start"] < noun["start"] or other["end"] > noun["end"])):
                    is_contained = True
                    break

            if not is_contained:
                resolved_nouns.append(noun)

        filtered_verbs = []
        filtered_prepositions = preposition_segments.copy()

        for verb in verb_segments:
            verb_index = verb["key_index"]
            is_noun_phrase = False

            for noun in noun_segments:
                if(noun["key_index"] == verb_index and noun["determiner"] is not None):
                    is_noun_phrase = True
                    break

            if not is_noun_phrase and verb_index not in prep_object_indices:
                filtered_verbs.append(verb)

        resolved_verbs = []

        for verb in filtered_verbs:
            verb_index = verb["key_index"]
            is_aux_candidate = "AUX" in self.classify_word(tokens[verb_index])

            if(is_aux_candidate):
                used_as_aux = False

                for other in filtered_verbs:
                    if(other is verb):
                        continue

                    if(other["key_index"] > verb_index) and other["start"] <= verb_index and tokens[verb_index] in other["auxiliaries"]:
                        used_as_aux = True
                        break
                if used_as_aux:
                    is_linking_verb = (
                        verb["base"] == "be"
                        and any(
                            other["key_index"] > verb_index
                            and other["start"] <= verb_index
                            and tokens[verb_index] in other["auxiliaries"]
                            and "ADJ" in self.classify_word(
                                tokens[other["key_index"]]
                            )
                            for other in filtered_verbs
                        )
                    )

                    if not is_linking_verb:
                        continue

            resolved_verbs.append(verb)

        return resolved_nouns, resolved_verbs, filtered_prepositions
        
    def solve(self, sentence, question):
    
        '''
          You can use a library like spacy (https://spacy.io/usage/linguistic-features) to preprocess the
            mostcommon.txt file. There are others that could be used but you must use them in preprocessing only.
            You CANNOT import the library into Gradescope.
          
          You must include whatever preprocessing you've done into your SentenceReadingAgent.py.
          
          DO NOT use another file .txt or .csv. Hard code your DICTS | LISTS into this .py file
          
          While the supplied mostcommon.txt contains most of the common words you will need
            you can (and SHOULD) expand the file as you find cases that the agent has problems
            processing. 
            
          Also not all words will be processed using the correct lexing for every possible problem the 
            agent might encounter and you are ENCOURAGED to expand these in your agents knowledge representation.
        '''
    
        sentence_tokens = self.tokenize_text(sentence)
        question_tokens = self.tokenize_text(question)

        # for word in sentence_tokens:
        #     print(word, self.normalize_word(word), self.classify_word(word))

        # for word in question_tokens:
        #     print(word, self.normalize_word(word), self.classify_word(word))

        noun_segments = self.get_noun_segments(sentence, sentence_tokens)
        verb_segments = self.get_verb_segments(sentence, sentence_tokens)
        preposition_segments = self.get_preposition_segments(
          sentence,
          sentence_tokens,
          noun_segments
      )

        resolved_nouns, filtered_verbs, filtered_prepositions = (
          self.filter_segments(
              sentence_tokens,
              noun_segments,
              verb_segments,
              preposition_segments
          )
      )

        print("NOUN SEGMENTS")
        for segment in noun_segments:
            print(segment)

        print("resolved Nouns")
        for segment in resolved_nouns:
            print(segment)

        print("VERB SEGMENTS")
        for segment in verb_segments:
            print(segment)

        print("FILTERED VERBS:")
        for segment in filtered_verbs:
            print(segment)

        # print("PREP SEGMENTS")
        # for segment in preposition_segments:
        #     print(segment)

        return ""

if __name__ == "__main__":
    agent = SentenceReadingAgent()
    sentences = [
    # Simple prepositional objects
    "David brought a note from Ada to Lucy.",
    "Lucy gave the book to him.",
    "Ada brought a note to Irene.",

    # Pronoun objects
    "David ran with her.",
    "Lucy sat with Ada.",

    # Multiple prepositional phrases
    "The dog ran from the house to the tree.",
    "David went from home to school.",

    # Overlapping noun candidates
    "Lucy went with the small dog.",
    "Ada went to the dog's house.",

    # Prepositions with descriptive nouns
    "The dog ran under the table.",
    "Lucy sat with the big red dog.",

    # No prepositions (regression tests)
    "Ada brought a short note.",
    "The dog ran home.",
    "Lucy saw two dogs.",
    "The dog's tail is short."
]

    for sentence in sentences:
        agent.solve(sentence, "")