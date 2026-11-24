class MonsterDiagnosisAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, diseases, patient):

        vector_values = {
            "+": 1,
            "-": -1,
            "0": 0
        }

        disease_vectors = {}

        for name, symptoms in diseases.items():
            disease_values= {}
            for vitamin, value in symptoms.items():
                if(value != "0"):
                    disease_values[vitamin] = (vector_values[value])
            disease_vectors[name] = disease_values

        patient_vector = {}
        for vitamin, value in patient.items():
            patient_vector[vitamin] = vector_values[value]


        disease_names = list(diseases)
        target_diseases = []
        sums_diseases = {vitamin: 0 for vitamin in patient}

        for size in range(len(diseases)+1):

            diagnosis = self.find_diagnoses(disease_names, disease_vectors, patient_vector, target_diseases, sums_diseases, 0, size)

            if diagnosis is not None:
                return diagnosis
            
        return []


    
    def get_is_match(self, sums_diseases:dict, patient_vector: dict) -> bool:
        is_match = True
        for vitamin, total in sums_diseases.items():

            if (total > 0):
                predicted = 1
            elif (total < 0):
                predicted = -1
            else:
                predicted = 0

            if (predicted != patient_vector[vitamin]):
                is_match = False
                break

        return is_match

    def recalculate_sums_disease(self, sums_diseases, symptoms, operation):
        for vitamin, value in symptoms.items():
            sums_diseases[vitamin] += value * operation


    def find_diagnoses(self, disease_names, disease_vectors, patient_vector, 
                       target_diseases, sums_diseases, start, size):

        
        if (len(target_diseases) == size):
            if self.get_is_match(sums_diseases, patient_vector):
                return target_diseases.copy()

            return None

        remaining_diseases = size - len(target_diseases)

        if not self.valid_path(sums_diseases, patient_vector, remaining_diseases):
            return None

        
        for index in range(start, len(disease_names) - remaining_diseases + 1):
            disease = disease_names[index]
            symptoms = disease_vectors[disease]

            target_diseases.append(disease)
            self.recalculate_sums_disease(sums_diseases, symptoms, 1)

            result = self.find_diagnoses(disease_names,disease_vectors, patient_vector, target_diseases,
                sums_diseases, index + 1,size)

            self.recalculate_sums_disease(sums_diseases, symptoms, -1)
            target_diseases.pop()

            if result is not None:
                return result

        return None

    def valid_path(self, sums_diseases, patient_vector, remaining_diseases):
        for vitamin, value in sums_diseases.items():
            if(patient_vector[vitamin] == 1 and value + remaining_diseases <= 0):
                return False
            elif(patient_vector[vitamin] == -1 and value - remaining_diseases >= 0):
                return False
            elif(patient_vector[vitamin] == 0 and abs(value) > remaining_diseases):
                return False
        return True

