import math
import sys
sys.path.append('../DecisionTree')

from dec_tree import *
from pre_processor import *

attrs = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']
label_index = 16

examples = []
test_examples = []
attr_vals = []
t = 50
ctr = 0
weights = []
trees = []
votes = []
updates = []


def load_data():
    global examples
    global test_examples
    global attr_vals
    global attrs

    # Get the training and testing data from file
    examples = populateExamples('../DecisionTree/bank/train.csv')
    test_examples = populateExamples('../DecisionTree/bank/test.csv')

    # Populate attr_vals
    attr_vals = learnDataFormat(examples)

    # Handle numeric values by taking the median and comparing each of them
    # to it, replacing the number with either 'over' or 'under'
    calculateMedians(examples, test_examples)


def calculate_error(root, examples):
    total = sum(weights)
    correct = 0
    for index in range(0, len(examples)):
        label = evaluateExample(root, examples[index])
        # Correct guess
        if label == examples[index][label_index]:
            correct += weights[index]
            updates.append(1)
        # Incorrect guess
        else:
            updates.append(-1)
    return 1 - correct / total


def update_weights(vote):
    global weights
    global updates

    for index in range(0, len(weights)):
        weights[index] = weights[index] * math.exp(-vote * updates[index])
    updates = []


def normalize_weights():
    global weights
    total = sum(weights)
    for index in range(0, len(weights)):
        weights[index] = weights[index] / total


load_data()
for ex in examples:
    weights.append(1/len(examples))

while ctr < t:
    # Learn a decision stump
    root = learnTree(attrs, attr_vals, examples, 1, 'entropy', weights)
    error = calculate_error(root, examples)
    vote = 0.5 * math.log((1 - error) / error)
    print(root.name, error, vote)
    trees.append(root)
    votes.append(vote)
    update_weights(vote)
    normalize_weights()
    ctr += 1
