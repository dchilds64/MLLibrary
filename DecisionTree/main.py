from dec_tree import *
from pre_processor import *
import sys

# Names of the two datasets we are using
bank_attr_names = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day',
                   'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']
car_attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']

# Decision tree variables
attr_names = []
attrs = []
attr_vals = []
examples = []

# Configuration variables
car = False
train_file = 'bank/train.csv'
test_file = 'bank/test.csv'
max_depth = 100
purity = 'entropy'
accept_unknown = True
label_index = 0


# Evaluate the data on the learned decision trees
def evaluateExamples(msg, examples):
    print('')
    print(msg)
    correct = 0
    total = 0
    for ex in examples:
        total += 1
        label = evaluateExample(root, ex)
        if label == ex[label_index]:
            correct += 1

    correct_ratio = correct / total
    print('Evaluated:', total)
    print('Correct:  ', correct)
    print('Error:     ', round((1 - correct_ratio) * 100, 2), '%', sep='')


# Get the arguments passed in to the script
if len(sys.argv) == 7:
    car = sys.argv[1] == 'car'
    train_file = sys.argv[2]
    test_file = sys.argv[3]
    max_depth = int(sys.argv[4])
    purity = sys.argv[5]
    accept_unknown = sys.argv[6] == 'True'

# Get the training and testing data from file
examples = populateExamples(train_file)
test_examples = populateExamples(test_file)

# Populate attr_vals
attr_vals = learnDataFormat(examples)
if car:
    attrs = car_attr_names
else:
    attrs = bank_attr_names

label_index = len(attrs) - 1

# Handle numeric values by taking the median and comparing each of them
# to it, replacing the number with either 'over' or 'under'
calculateMedians(examples, test_examples)

# Populate common_vals and replace unknown if necessary
if not accept_unknown:
    remove_unknown(examples, test_examples, attr_vals)

# Learn the decision tree
root = learnTree(attrs, attr_vals, examples, max_depth, purity)

# Evaluate the quality of the learned tree on the training and test data
evaluateExamples('EVALUATING TRAINING EXAMPLES', examples)
evaluateExamples('EVALUATING TEST EXAMPLES', test_examples)
