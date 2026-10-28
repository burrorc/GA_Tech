import re
from knowledge_base import NAMES, LEMMAS, WORD_TYPES, AUXILIARIES, ADVERBS, NEGATIVES


MODIFIER_TYPES = {
    "color": {
        "red", "blue", "green", "black", "white",
        "yellow", "orange", "purple", "pink", "brown",
        "gray", "grey", "gold", "silver"
    },
    "size": {
        "small", "big", "large", "little", "tiny",
        "huge", "giant", "short", "long", "tall",
        "large", "wide", "narrow", "thin", "thick"
    },
    "quantity": {
        "zero", "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "twenty", "hundred",
        "many", "few", "several"
    },
    "shape": {
        "round", "square", "circle", "circular",
        "triangle", "triangular", "rectangular",
        "oval", "flat", "straight", "curved"
    },
    "age": {
        "young", "old", "new", "ancient", "modern"
    },
    "speed": {
        "fast", "slow", "quick", "rapid"
    }
}


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


    def get_infinitive_segments(self, tokens, verb_segments):
        segments = []

        for verb in verb_segments:
            verb_index = verb["key_index"]

            if(verb_index ==0):
                continue

            previous_index = verb_index -1
            previous_word = tokens[previous_index]

            if (previous_word.lower() != "to"):
                continue

            if (self.normalize_word(tokens[verb_index]) != tokens[verb_index].lower()):
                continue

            segments.append({"start": previous_index, "end": verb["end"], "key_index": verb_index, "base": verb["base"], "original": verb["original"]})

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

        resolved_prepositions = []

        for preposition in preposition_segments:
            is_contained = False

            for other in preposition_segments:
                if preposition is other:
                  continue

                if(other["start"] <= preposition["start"] and other["end"] >= preposition["end"] and (other["start"] < preposition["start"] or other["end"] > preposition["end"])):
                    is_contained = True
                    break

            if not is_contained:
                resolved_prepositions.append(preposition)

        return resolved_nouns, resolved_verbs, resolved_prepositions

    def find_predicate(self, tokens, resolved_nouns, resolved_verbs, preposition_segments):
        if not resolved_verbs:
            return None

        # best_candidate = None
        # best_score = -1

        candidates = []

        for verb in resolved_verbs:
            score = 0
            verb_index = verb["key_index"]

            for noun in resolved_nouns:
                if (noun["end"] < verb['start']):
                    score +=2
                    break 

            for noun in resolved_nouns:
                if noun["key_index"] == verb_index:
                    if noun["determiner"] is not None or noun["modifiers"]:
                        score -= 3
                        break

            if (verb["auxiliaries"]):
                score +=2

            if (verb["end"] > verb_index):
                score +=1

            for other in resolved_verbs:
                if other is verb:
                    continue

                if(other["start"] <= verb_index and verb_index <= other['end'] and verb["original"] in other["modifiers"]):
                    score -= 3
                    break

            if (verb["base"] == "be" ):
                for other in resolved_verbs:
                    if other is verb:
                        continue

                    if (other["key_index"] > verb_index and "ADJ" in self.classify_word(tokens[other["key_index"]]) and other['start'] <= verb_index):
                        score += 3
                        break

            # if best_candidate is None or score > best_score:
                # best_candidate = verb
                # best_score = score
            candidates.append({
                  "verb": verb,
                  "score": score
              })

        best_score = max(candidate["score"] for candidate in candidates)

      
        minimum_score = best_score - 2
        best_candidate = None

        for candidate in candidates:
            if (candidate["score"] < minimum_score):
                continue

            verb = candidate["verb"]

            if (best_candidate is None or verb["key_index"] < best_candidate["key_index"]):
                best_candidate = verb

        return best_candidate

    def find_subject(self, tokens, resolved_nouns, predicate):
        if predicate is None:
            return None

        subject = None
        predicate_start = predicate["start"]

        for noun in resolved_nouns:
            if(noun["end"] >= predicate_start):
                continue

            if (subject is None or noun["end"] > subject["end"]):
                subject = noun

        if subject is None:
            return None

        subjects = [subject]
        conjunction = None

        while True:
            con_index = subjects[0]["start"]-1

            if con_index < 0:
              break

            word = tokens[con_index].lower()

            if word not in ("and", 'or', "nor"):
                break

            previous_noun = None

            for noun in resolved_nouns:
                if noun["end"] == con_index -1:
                    previous_noun = noun
                    break

            if previous_noun is None:
                break

            subjects.insert(0, previous_noun)
            conjunction = word

        return {"nouns": subjects, "conjunction": conjunction}

    
    def find_object_relationships(self,resolved_nouns,noun_segments,resolved_prepositions,predicate):
        if predicate is None:
            return None

        objects = []
        prepositions = []

        for noun in resolved_nouns:
            if noun["start"] > predicate["end"]:
                objects.append(noun)

        
        for preposition in resolved_prepositions:
            object_noun = None

            for noun in noun_segments:
                if (noun["key_index"] == preposition["object_index"]):
                    object_noun = noun
                    break

            if object_noun is not None:
                prepositions.append({"preposition": preposition,"object": object_noun})

        return {
            "objects": objects,
            "prepositions": prepositions
        }


    def analyze_question(self, question_tokens):
        if not question_tokens:
            return None

        words = []

        for token in question_tokens:
            words.append(token.lower())

        question_type = words[0].upper()
        preposition = None

        if question_type == "WHEN":
            question_type = "TIME"

        elif (question_type == "WHAT" and len(words) > 1 and words[1] == "time"):
            question_type = "TIME"

        elif (len(words) >= 3 and (words[0] == "at" and words[1] == "what" and words[2] == "time")):
            question_type = "TIME"
            preposition = None

        if (question_type == "HOW" and len(words) >1):
            if(words[1] in ("long", "far", "many")):
                question_type = "HOW_"+ words[1].upper()

        for word in words:
            if ("ADP" in self.classify_word(word)):
                preposition = word

        return {"type": question_type, "preposition": preposition}

    def answer_question(self, question_tokens, question_info, subject, object_relationships, predicate, sentence_tokens, resolved_nouns):
        if (question_info == None or object_relationships == None):
            return None

        if (question_info["type"] == "WHO"):
            question_words = []

            for word in question_tokens:
                question_words.append(word.lower())

            if ("was" in question_words or "were" in question_words):
                if (len(object_relationships["objects"]) > 1):
                    return object_relationships["objects"][0]["original"]
                
            if subject is not None and object_relationships["objects"]:

                subject_mentioned = False

                for noun in subject["nouns"]:
                    for word in question_tokens:
                        if (self.normalize_word(word) == noun["base"]):
                            subject_mentioned = True
                            break

                if not subject_mentioned and len(object_relationships["objects"]) > 1:
                    recipient = object_relationships["objects"][0]

                    if("NOUN" in self.classify_word(recipient["original"]) or "PRON" in self.classify_word(recipient["original"])):
                        return recipient["original"]
                    
            if question_info["preposition"] in ("in", "at", "on"):
              if subject is not None and subject["nouns"]:
                  return subject["nouns"][0]["original"]

            if (subject is not None and len(subject["nouns"]) > 1):
                if (subject["conjunction"] == "and"):

                    mentioned_subjects = []
                    other_subjects = []

                    for noun in subject["nouns"]:
                        mentioned = False

                        for word in question_tokens:
                            if (self.normalize_word(word) == noun["base"]):
                                mentioned = True
                                break

                        if mentioned:
                            mentioned_subjects.append(noun)
                        else:
                            other_subjects.append(noun)

                    if (question_info["preposition"] == "with" and mentioned_subjects and other_subjects):
                        return other_subjects[0]["original"]

            
            preposition = question_info["preposition"]

            if preposition is not None:

              for relationship in object_relationships["prepositions"]:

                  if (relationship["preposition"]["base"] != preposition):
                      continue

                  object_name = relationship["object"]["base"]

                  if (preposition == "with" and subject is not None):
                      for word in question_tokens:
                          if self.normalize_word(word) == object_name:
                              return subject["nouns"][0]["original"]

                  return relationship["object"]["original"]

              return None

            words = []

            for token in question_tokens:
                words.append(token.lower())

            if subject is not None:
                for noun in subject["nouns"]:
                    if noun["original"].lower() in words:

                        for object in object_relationships["objects"]:
                            if "PROPN" in self.classify_word(object["original"]):
                                return object["original"]

                        return None

            if subject is not None and subject["nouns"]:
                return subject["nouns"][0]['original']

        if question_info["type"] == "WHAT":
          if subject is not None:
              for noun in subject["nouns"]:

                  noun_mentioned = False

                  for word in question_tokens:
                      if self.normalize_word(word) == noun["base"]:
                          noun_mentioned = True
                          break

                  if not noun_mentioned:
                      continue
                  
                  for word in question_tokens:
                      modifier_type = word.lower()

                      if modifier_type not in MODIFIER_TYPES:
                          continue

                      for modifier in noun["modifiers"]:
                          if modifier.lower() in MODIFIER_TYPES[modifier_type]:
                              return modifier

          if subject is not None:
            for person_or_name in subject["nouns"]:

                if person_or_name["base"] not in [self.normalize_word(word) for word in question_tokens]:
                    continue

                for noun in resolved_nouns:
                    # if (noun["end"] == person_or_name["start"] - 1):
                    if (
                        noun["end"] == person_or_name["start"] - 1
                        and noun["determiner"] is None
                    ):
                        if ("NOUN" in self.classify_word(noun["original"])):
                            return noun["original"]

          if subject is not None:
            subject_mentioned = False

            for noun in subject["nouns"]:
                for word in question_tokens:
                    if (self.normalize_word(word) == noun["base"]):
                        subject_mentioned = True
                        break

            if not subject_mentioned and not object_relationships["objects"]:
                return subject["nouns"][0]["original"]

          for noun in object_relationships["objects"]:

              if "PRON" in self.classify_word(noun["original"]):
                  continue

              answer = noun["original"]

          return answer if "answer" in locals() else None

        if (question_info["type"] == "HOW_LONG"):

          for noun in object_relationships["objects"]:

              for word in question_tokens:
                  if (self.normalize_word(word) == noun["base"]):
                      if noun["modifiers"]:
                          return noun["modifiers"][0]

          return None

        if question_info["type"] == "HOW_MANY":
          for noun in resolved_nouns:
              for modifier in reversed(noun["modifiers"]):
                  if "NUM" in self.classify_word(modifier):
                      return modifier

        
        if question_info["type"] == "WHERE":

            if object_relationships is None:
                return None

            destination = None

            for relationship in object_relationships["prepositions"]:

                preposition = relationship["preposition"]
                noun = relationship["object"]

                if preposition["base"] in ("to", "in", "at", "on"):
                    destination = noun["original"]

            return destination

        if question_info["type"] == "HOW_FAR":

          if object_relationships is None:
              return None

          distance_units = {"mile", "foot", "yard", "meter", "kilometer"}

          for noun in object_relationships["objects"]:
              if noun["base"] in distance_units:
                  return noun["original"]

          return None

        
        if question_info["type"] == "HOW":

            for word in question_tokens:
              word = word.lower()

              for category, values in MODIFIER_TYPES.items():
                  if word in values:

                      if predicate is not None:
                          for modifier in predicate["modifiers"]:
                              if modifier.lower() in values:
                                  return modifier

            if predicate is not None:
                return predicate["original"]

            return None

        if question_info["type"] == "TIME":

          for word in sentence_tokens:
              if "TIME" in self.classify_word(word):
                  return word

          return None



        return None

                
        
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
        try:
            sentence_tokens = self.tokenize_text(sentence)
            question_tokens = self.tokenize_text(question)

            # for word in sentence_tokens:
            #     print(word, self.normalize_word(word), self.classify_word(word))

            # for word in question_tokens:
            #     print(word, self.normalize_word(word), self.classify_word(word))

            noun_segments = self.get_noun_segments(sentence, sentence_tokens)
            verb_segments = self.get_verb_segments(sentence, sentence_tokens)
            infinitive_segments = self.get_infinitive_segments(sentence_tokens,verb_segments)
            preposition_segments = self.get_preposition_segments(
                sentence,
                sentence_tokens,
                noun_segments
            )

            resolved_nouns, resolved_verbs, resolved_prepositions = (
                self.filter_segments(
                    sentence_tokens,
                    noun_segments,
                    verb_segments,
                    preposition_segments
                )
            )

            predicate = self.find_predicate(
                sentence_tokens,
                resolved_nouns,
                resolved_verbs,
                preposition_segments
            )

            subject = self.find_subject(
                sentence_tokens,
                resolved_nouns,
                predicate
            )


            object_relationships = self.find_object_relationships(
                resolved_nouns,
                noun_segments,
                resolved_prepositions,
                predicate
            )

            question_info = self.analyze_question(question_tokens)

            # print("QUESTION:", question)
            # print("QUESTION INFO:", question_info)
            # print("\nSENTENCE:", sentence)

            # print("INFINITIVE CANDIDATES:")
            # for infinitive in infinitive_segments:
            #     print(infinitive)

            # print("\nSENTENCE:", sentence)

            # print("NOUN SEGMENTS")
            # for segment in noun_segments:
            #     print(segment)

            print("resolved Nouns")
            for segment in resolved_nouns:
                print(segment)


            # print("RAW PREPOSITIONS:")
            # for preposition in preposition_segments:
            #     print(preposition)

            # print("RESOLVED PREPOSITIONS:")
            # for preposition in resolved_prepositions:
            #     print(preposition)

            # print("VERB SEGMENTS")
            # for segment in verb_segments:
            #     print(segment)

            # print("Resolved VERBS:")
            # for segment in resolved_verbs:
            #     print(segment)

            print("SUBJECT:", subject)

            print("PREDICATE:", predicate)

            print("OBJECT RELATIONSHIPS:", object_relationships)

            answer = self.answer_question(
                question_tokens,
                question_info,
                subject,
                object_relationships,
                predicate,
                sentence_tokens,
                resolved_nouns
            )

            # print("QUESTION:", question)
            # print("ANSWER:", answer)

            return answer if answer is not None else ""
        except Exception as error:
          print(f"Agent error: {type(error).__name__}: {error}")
          return ""





if __name__ == "__main__":
    agent = SentenceReadingAgent()

    tests = [
        (
            "There are three men in the car.",
            "How many men are in the car?",
            "three"
        ),
        (
            "There are one hundred adults in that city.",
            "How many adults are in that city?",
            "hundred"
        ),
        (
            "David and Lucy walk one mile to school.",
            "How far do David and Lucy walk?",
            "mile"
        ),
        (
            "Ada brought a short note to Irene.",
            "How long was the note?",
            "short"
        )
    ]

    for i, (sentence, question, expected) in enumerate(tests, start=1):
        actual = agent.solve(sentence, question)

        print(f"\n========== TEST {i} ==========")
        print(f"Sentence: {sentence}")
        print(f"Question: {question}")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")
        print(f"Result: {'PASS' if actual == expected else 'FAIL'}")

