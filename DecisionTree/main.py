from dec_tree import *

bank_attr_names = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']
bank_attrs = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome']
bank_attr_vals = [
	[], 
	['admin.', 'unknown', 'unemployed', 'management', 'housemaid', 'entrepreneur', 'student', 'blue-collar', 'self-employed', 'retired', 'technician', 'services'], 
	['married', 'divorced', 'single'],
	['unknown', 'secondary', 'primary', 'tertiary'],
	['yes', 'no'],
	[],
	['yes', 'no'],
	['yes', 'no'],
	['unknown', 'telephone', 'cellular'],
	[],
	['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
	[],
	[],
	[],
	[],
	['unknown', 'other', 'failure', 'success'],
	['yes', 'no']
]


car_attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']
car_attrs = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
car_attr_vals = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]

attr_names = car_attr_names
attrs = car_attrs
attr_vals = car_attr_vals

examples = []

examples = populateExamples('car/train.csv')

root = id3(examples, attrs, 'label', 0)

print('EVALUATING TRAINING EXAMPLES')
correct = 0
total = 0
for ex in examples:
	total += 1
	label = evaluateExample(root, ex)
	if label == ex[6]:
		correct +=1

correct_ratio = correct / total
print('Evaluated', total, 'examples')
print(correct, 'were evaluated correctly')
print(correct_ratio, '%')

print('EVALUATING TEST EXAMPLES')

test_examples = populateExamples('car/test.csv')
correct = 0
total = 0
for ex in test_examples:
	total += 1
	label = evaluateExample(root, ex)
	if label == ex[6]:
		correct +=1

correct_ratio = correct / total
print('Evaluated', total, 'examples')
print(correct, 'were evaluated correctly')
print(correct_ratio, '%')

