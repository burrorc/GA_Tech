import numpy as np
import RTLearner as rt

learner = rt.RTLearner(
    leaf_size=5,
    verbose=False
)

# Synthetic training data
data_x = np.arange(30).reshape(-1, 1)

data_y = np.array(
    [-1] * 10 +
    [0] * 10 +
    [1] * 10
)

learner.add_evidence(data_x, data_y)

predictions = learner.query(data_x)

print("EXPECTED")
print(data_y)

print("\nPREDICTIONS")
print(predictions)

print("\nUNIQUE PREDICTIONS")
print(np.unique(predictions))

print("\nACCURACY")
print(np.mean(predictions == data_y))

print("\nVALID CLASSES")
print(np.isin(predictions, [-1, 0, 1]).all())

# Test 2: Identical training labels
data_x = np.arange(30).reshape(-1, 1)
data_y = np.ones(30)

learner.add_evidence(data_x, data_y)
predictions = learner.query(data_x)

print("\nIDENTICAL LABELS")
print(np.all(predictions == 1))


# Test 3: Identical feature values
data_x = np.ones((30, 1))
data_y = np.array([-1] * 5 + [0] * 20 + [1] * 5)

learner.add_evidence(data_x, data_y)
predictions = learner.query(data_x)

print("\nIDENTICAL FEATURES")
print(np.all(predictions == 0))


# Test 4: Leaf size stopping condition
data_x = np.arange(5).reshape(-1, 1)
data_y = np.array([-1, 1, 1, 0, 1])

learner.add_evidence(data_x, data_y)
predictions = learner.query(data_x)

print("\nLEAF SIZE CONDITION")
print(np.all(predictions == 1))