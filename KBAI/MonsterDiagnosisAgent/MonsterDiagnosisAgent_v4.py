class MonsterDiagnosisAgent:
    def __init__(self):
        pass

    def solve(self, diseases, patient):

        vector_values = {
            "+": 1,
            "-": -1,
            "0": 0
        }

        disease_vectors = {}

        for name, symptoms in diseases.items():
            disease_values = {}
            for vitamin, value in symptoms.items():
                if value != "0":
                    disease_values[vitamin] = vector_values[value]
            disease_vectors[name] = disease_values

        patient_vector = {}
        for vitamin, value in patient.items():
            patient_vector[vitamin] = vector_values[value]

        disease_names = list(diseases)
        selected_diseases = []
        sums_diseases = {vitamin: 0 for vitamin in patient}

        for size in range(len(diseases) + 1):

            result = self.search(
                disease_names,
                disease_vectors,
                patient_vector,
                selected_diseases,
                sums_diseases,
                0,
                size
            )

            if result is not None:
                return result

        return []

    def search(self, disease_names, disease_vectors,
               patient_vector, selected_diseases,
               sums_diseases, start_index, target_size):

        # Base case: evaluate a complete combination
        if len(selected_diseases) == target_size:
            if self.get_is_match(sums_diseases, patient_vector):
                return selected_diseases.copy()

            return None

        remaining = target_size - len(selected_diseases)

        # Generate combinations without duplicates
        for index in range(
            start_index,
            len(disease_names) - remaining + 1
        ):
            disease = disease_names[index]
            symptoms = disease_vectors[disease]

            # Select disease
            selected_diseases.append(disease)
            self.update_sums(sums_diseases, symptoms, 1)

            # Explore next level
            result = self.search(
                disease_names,
                disease_vectors,
                patient_vector,
                selected_diseases,
                sums_diseases,
                index + 1,
                target_size
            )

            # Backtrack
            self.update_sums(sums_diseases, symptoms, -1)
            selected_diseases.pop()

            if result is not None:
                return result

        return None

    def update_sums(self, sums_diseases, symptoms, multiplier):

        for vitamin, value in symptoms.items():
            sums_diseases[vitamin] += value * multiplier

    def get_is_match(self, sums_diseases: dict,
                     patient_vector: dict) -> bool:

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