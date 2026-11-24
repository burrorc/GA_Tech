import numpy as np
import RTLearner as rt
import BagLearner as bl

learner = bl.BagLearner(
    learner=rt.RTLearner,
    kwargs={"leaf_size": 5},
    bags=20,
    boost=False,
    verbose=False
)

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

print("\nPREDICTION SHAPE")
print(predictions.shape)

print("\nUNIQUE PREDICTIONS")
print(np.unique(predictions))

print("\nACCURACY")
print(np.mean(predictions == data_y))

print("\nVALID CLASSES")
print(np.isin(predictions, [-1, 0, 1]).all())

print("\nCONSISTENT PREDICTIONS")
print(np.array_equal(
    predictions, learner.query(data_x)
))