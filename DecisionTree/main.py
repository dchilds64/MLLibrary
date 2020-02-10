from dec_tree import *


examples = []

if car:
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
	print('Training error was:', (1 - correct_ratio) * 100, '%')

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
	print(correct, 'examples were evaluated correctly')
	print('Test error was:', (1 - correct_ratio) * 100, '%')
else:
	examples = populateExamples('bank/train.csv')
	calculateMedians(examples)
	findCommonAttrVals(examples)
	root = id3(examples, attrs, 'y', 0)

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

	test_examples = populateExamples('bank/test.csv')
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
