from itertools import combinations

class MonsterDiagnosisAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, diseases, patient):
        # Add your code here!
        #
        # The first parameter to this method is a list of diseases, represented as a
        # dictionary. The key in each dictionary entry is the name of a disease. The
        # value for the key item is another dictionary of symptoms of that disease, where
        # the keys are letters representing vitamin names ("A" through "Z") and the values
        # are "+" (for elevated), "-" (for reduced), or "0" (for normal).
        #
        # The second parameter to this method is a particular patient's symptoms, again
        # represented as a dictionary where the keys are letters and the values are
        # "+", "-", or "0".
        #
        # This method should return a list of names of diseases that together explain the
        # observed symptoms. If multiple lists of diseases can explain the symptoms, you
        # should return the smallest list. If multiple smallest lists are possible, you
        # may return any sufficiently explanatory list.
        #
        # The solve method will be called multiple times, each of which will have a new set
        # of diseases and a new patient to diagnose.

        vector_values = {
            "+": 1,
            "-": -1,
            "0": 0
        }

        disease_vectors = {}

        for name, symptoms in diseases.items():
            disease_values= {}
            for vitamin, value in symptoms.items():
                disease_values[vitamin] = (vector_values[value])
            disease_vectors[name] = disease_values

        patient_vector = {}
        for vitamin, value in patient.items():
            patient_vector[vitamin] = vector_values[value]
        
        
        # sums_diseases = {vitamin: 0 for vitamin in patient}

        # for name, symptoms in disease_vectors.items():
        #     for vitamin, value in symptoms.items():
        #         sums_diseases[vitamin] += value
        
        # selected_diseases = ["Alphaitis", "Betatosis"]

        for size in range(len(diseases)+1):
            for combination in combinations(diseases, size):
                sums_diseases = self.get_sums_disease(combination, disease_vectors)
                is_match = self.get_is_match(sums_diseases, patient_vector)
                if(is_match):
                    print("Selected diseases:", combination)
                    print("Valid diagnosis:", is_match)
                    return list(combination)
        # sums_diseases = {vitamin: 0 for vitamin in patient}
        
        # for name in selected_diseases:
        #     symptoms = disease_vectors[name]
        #     for vitamin, value in symptoms.items():
        #         sums_diseases[vitamin] += value

        # is_match = True
        # for vitamin, total in sums_diseases.items():

        #     if total > 0:
        #         predicted = 1
        #     elif total < 0:
        #         predicted = -1
        #     else:
        #         predicted = 0

        #     if predicted != patient_vector[vitamin]:
        #         is_match = False
        #         break

        # print("Selected diseases:", selected_diseases)
        # print("Valid diagnosis:", is_match)

        pass

    def get_sums_disease(self, selected_diseases, disease_vectors):
        sums_diseases = {vitamin: 0 for vitamin in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        for name in selected_diseases:
            symptoms = disease_vectors[name]
            for vitamin, value in symptoms.items():
                sums_diseases[vitamin] += value

        return sums_diseases

    def get_is_match(self, sums_diseases:dict, patient_vector: dict) -> bool:
        is_match = True
        for vitamin, total in sums_diseases.items():

            if total > 0:
                predicted = 1
            elif total < 0:
                predicted = -1
            else:
                predicted = 0

            if predicted != patient_vector[vitamin]:
                is_match = False
                break

        return is_match

