from dec_tree import *
import sys

# Names of the two datasets we are using
bank_attr_names = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']
car_attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']

# Decision tree variables
common_vals = []
attr_names = []
attrs = []
attr_vals = []
examples = []

# Configuration variables
car = False
train_file = 'bank/train.csv'
test_file = 'bank/test.csv'
max_depth = 3
purity = 'entropy'
accept_unknown = False
label_index = 0


# Goes through the examples provided and pulls the possible values of each of the attributes.
def learnDataFormat(examples):
	global attr_vals

	# Loop through each attribute index in the examples
	for index in range(0, len(examples[0])):
		possible_vals = []
		# Get the possible values for the current attribute index
		for ex in examples:
			if not ex[index] in possible_vals:
				possible_vals.append(ex[index])
		is_int = True
		# There are some attributes which have individual values that are numeric, but not all, so
		# this checks that all of the possible values are numeric
		for val in possible_vals:
			if not representsInt(val):
				is_int = False
				break
		# For the purposes of this library, numeric values are treated as categorical data by comparing
		# each value to the median of the values in the training data and being replaced with 'over' or
		# 'under', with 'over' including values that are equal to the median.
		if is_int:
			possible_vals = ['over', 'under']
		attr_vals.append(possible_vals)


# Goes through the examples provided and finds the common values for each of the attributes.
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

# Evaluate the quality of the learned tree on the training and test data
evaluateExamples('EVALUATING TRAINING EXAMPLES', examples)
evaluateExamples('EVALUATING TEST EXAMPLES', test_examples)
