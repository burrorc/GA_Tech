ATTRIBUTE_VALUES = {
    "size": ["tiny","small","medium","large","huge"],
    "color": ["black","white","brown","gray","red","yellow","blue","green","orange","purple"],
    "covering": ["fur","feathers","scales","skin"],
    "foot-type": ["paw","hoof","talon","foot","none"],
    "leg-count": [0,1,2,3,4,5,6,7,8],
    "arm-count": [0,1,2,3,4,5,6,7,8],
    "eye-count": [0,1,2,3,4,5,6,7,8],
    "horn-count": [0,1,2],
    "lays-eggs": [True,False],
    "has-wings": [True,False],
    "has-gills": [True,False],
    "has-tail": [True,False],
}


class MonsterClassificationAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, samples, new_monster):
        #Add your code here!
        #
        #The first parameter to this method will be a labeled list of samples in the form of
        #a list of 2-tuples. The first item in each 2-tuple will be a dictionary representing
        #the parameters of a particular monster. The second item in each 2-tuple will be a
        #boolean indicating whether this is an example of this species or not.
        #
        #The second parameter will be a dictionary representing a newly observed monster.
        #
        #Your function should return True or False as a guess as to whether or not this new
        #monster is an instance of the same species as that represented by the list.
        

        positive_attribute_values = self.learn_positive_values(samples)
        negative_attribute_values, neg_constraints = self.learn_negative_values(samples, positive_attribute_values)

        unknown_attribute_values = set()

        for attribute, value in new_monster.items():
            if value not in positive_attribute_values[attribute]:
                unknown_attribute_values.add((attribute, value))

                
        for attribute, value in new_monster.items():
            if value in negative_attribute_values[attribute]:
                return False

        if not self.is_positive_candidate(new_monster, neg_constraints):
            return False

        # probable_neg_constraints = self.get_probable_neg_constraints(neg_constraints)

        # for attribute, value in new_monster.items():
        #     if(attribute, value) in probable_neg_constraints:
        #         return False

        # return True
        return len(unknown_attribute_values) <= 4

    def learn_positive_values(self, samples):
        positive_attribute_values = {attribute: set() for attribute in ATTRIBUTE_VALUES}

        for monster, is_positive in samples:
            if is_positive:
                for attribute, value in monster.items():
                    positive_attribute_values[attribute].add(value)

        return positive_attribute_values

    def learn_negative_values(self, samples, positive_attribute_values):
        negative_attribute_values = {attribute: set() for attribute in ATTRIBUTE_VALUES}

        neg_constraints = []

        for monster, is_positive in samples:
            if not is_positive:
                unknown_attribute_values = set()

                for attribute, value in monster.items():
                    if value not in positive_attribute_values[attribute]:
                        unknown_attribute_values.add((attribute, value))

                if unknown_attribute_values:
                    neg_constraints.append(unknown_attribute_values)


                if (len(unknown_attribute_values) == 1):
                    attribute, value = next(iter(unknown_attribute_values))
                    negative_attribute_values[attribute].add(value)

        return negative_attribute_values, neg_constraints

    def is_positive_candidate(self, monster, neg_constraints):
        for constraint in neg_constraints:
            if all(
                monster[attribute] == value
                for attribute, value in constraint
            ):
                return False

        return True

    def get_probable_neg_constraints(self, neg_constraints):
        probable_candidates = set()

        constraint_list = list(neg_constraints)

        while constraint_list:
            counts = {}

            for constraint in constraint_list:
                for attribute_value in constraint:
                    counts[attribute_value] = counts.get(attribute_value,0) +1

            highest_count = max(counts, key=counts.get)
            probable_candidates.add(highest_count)

            constraint_list= [
                constraint 
                for constraint in constraint_list
                if highest_count not in constraint
            ]

        return probable_candidates