from dec_tree import *
import sys

bank_attr_names = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']
car_attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']

common_vals = []
attr_names = []
attrs = []
attr_vals = []

examples = []

car = False
train_file = 'bank/train.csv'
test_file = 'bank/test.csv'
max_depth = 3
purity = 'entropy'
accept_unknown = False
label_index = 0


def learnDataFormat(examples):
	global attr_vals

	for index in range(0, len(examples[0])):
		possible_vals = []
		for ex in examples:
			if not ex[index] in possible_vals:
				possible_vals.append(ex[index])
		is_int = True
		for val in possible_vals:
			if not representsInt(val):
				is_int = False
				break
		if is_int:
			possible_vals = ['over', 'under']
		attr_vals.append(possible_vals)


def findCommonAttrVals(examples):
	global common_vals
	for val in attrs:
		common_val = commonValue(examples, attrs, attr_vals, val)
		# If the common value happens to be unknown, get the subset of examples where that
		# attribute's value is not unknown and find the most common value based off of that
		# set.
		if common_val == 'unknown':
			subset = []
			index = attrs.index(val)
			for ex in examples:
				if not ex[index] == 'unknown':
					subset.append(ex)
			common_val = commonValue(subset, attrs, attr_vals, val)
		common_vals.append(common_val)


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
learnDataFormat(examples)
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
	findCommonAttrVals(examples)
	for ex in examples:
		for index in range(0, len(ex)):
			if ex[index] == 'unknown':
				ex[index] = common_vals[index]
	for ex in test_examples:
		for index in range(0, len(ex)):
			if ex[index] == 'unknown':
				ex[index] = common_vals[index]
	for vals in attr_vals:
		if 'unknown' in vals:
			del vals[vals.index('unknown')]

# Learn the decision tree
root = learnTree(attrs, attr_vals, examples, max_depth, purity)

print('EVALUATING TRAINING EXAMPLES')
correct = 0
total = 0
for ex in examples:
	total += 1
	label = evaluateExample(root, ex)
	if label == ex[label_index]:
		correct += 1
	else:
		label = evaluateExample(root, ex)

correct_ratio = correct / total
print('Evaluated', total, 'examples')
print(correct, 'examples were evaluated correctly')
print('Training error was:', (1 - correct_ratio) * 100, '%')
print('EVALUATING TEST EXAMPLES')

correct = 0
total = 0
for ex in test_examples:
	total += 1
	label = evaluateExample(root, ex)
	if label == ex[label_index]:
		correct += 1

correct_ratio = correct / total
print('Evaluated', total, 'examples')
print(correct, 'examples were evaluated correctly')
print('Test error was:', (1 - correct_ratio) * 100, '%')
