from dec_tree import *
import sys

bank_attr_names = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']
# bank_attrs = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome']
bank_attr_vals = [
	['over', 'under'],
	['admin.', 'unknown', 'unemployed', 'management', 'housemaid', 'entrepreneur', 'student', 'blue-collar', 'self-employed', 'retired', 'technician', 'services'], 
	['married', 'divorced', 'single'],
	['unknown', 'secondary', 'primary', 'tertiary'],
	['yes', 'no'],
	['over', 'under'],
	['yes', 'no'],
	['yes', 'no'],
	['unknown', 'telephone', 'cellular'],
	['over', 'under'],
	['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
	['over', 'under'],
	['over', 'under'],
	['over', 'under'],
	['over', 'under'],
	['unknown', 'other', 'failure', 'success'],
	['yes', 'no']
]

car_attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']
# car_attrs = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
car_attr_vals = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]

attr_names = []
attrs = []
attr_vals = []

examples = []
attrs = []

car = True
train_file = 'car/train.csv'
test_file = 'car/test.csv'
max_depth = 500
purity = 'entropy'
accept_unknown = True


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


if len(sys.argv) == 7:
	car = sys.argv[1] == 'car'
	train_file = sys.argv[2]
	test_file = sys.argv[3]
	max_depth = int(sys.argv[4])
	purity = sys.argv[5]
	accept_unknown = sys.argv[6] == 'True'

# if car:
# 	examples = populateExamples('car/train.csv')
#
# 	root = learnTree(car_attr_names, car_attrs, car_attr_vals, 6, car, examples, max_depth, purity, accept_unknown)
#
# 	print('EVALUATING TRAINING EXAMPLES')
# 	correct = 0
# 	total = 0
# 	for ex in examples:
# 		total += 1
# 		label = evaluateExample(root, ex)
# 		if label == ex[6]:
# 			correct += 1
#
# 	correct_ratio = correct / total
# 	print('Evaluated', total, 'examples')
# 	print(correct, 'were evaluated correctly')
# 	print('Training error was:', (1 - correct_ratio) * 100, '%')
#
# 	print('EVALUATING TEST EXAMPLES')
#
# 	test_examples = populateExamples('car/test.csv')
# 	correct = 0
# 	total = 0
# 	for ex in test_examples:
# 		total += 1
# 		label = evaluateExample(root, ex)
# 		if label == ex[6]:
# 			correct += 1
#
# 	correct_ratio = correct / total
# 	print('Evaluated', total, 'examples')
# 	print(correct, 'examples were evaluated correctly')
# 	print('Test error was:', (1 - correct_ratio) * 100, '%')
# else:
examples = populateExamples(train_file)
# for ex in examples:

test_examples = populateExamples(test_file)
learnDataFormat(examples)
if car:
	attrs = car_attr_names
else:
	attrs = bank_attr_names
calculateMedians(examples, test_examples)
findCommonAttrVals(examples)
root = learnTree(attrs, attr_vals, examples, max_depth, purity, accept_unknown)

print('EVALUATING TRAINING EXAMPLES')
correct = 0
total = 0
for ex in examples:
	total += 1
	label = evaluateExample(root, ex)
	if label == ex[16]:
		correct +=1

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
	if label == ex[16]:
		correct +=1

correct_ratio = correct / total
print('Evaluated', total, 'examples')
print(correct, 'examples were evaluated correctly')
print('Test error was:', (1 - correct_ratio) * 100, '%')
