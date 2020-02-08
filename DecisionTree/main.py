from dec_tree import *


attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']
attrs = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
attr_vals = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
examples = []
			

examples = populateExamples('car/train.csv')

root = id3(examples, attrs, 'label')

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

