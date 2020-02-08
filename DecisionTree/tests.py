from dec_tree import *

notes = []
tests_run = 0
tests_passed = 0

label_examples = [
['low','vhigh','2','2','big','med','good'],
['vhigh','vhigh','5more','more','small','low','unacc'],
['vhigh','med','2','2','small','med','acc'],
['med','high','4','2','med','low','unacc'],
['low','high','2','more','small','high','good'],
['high','vhigh','4','2','small','high','vgood'],
['vhigh','high','3','2','small','med','unacc'],
['med','med','3','4','med','low','unacc'],
['high','high','3','more','med','med','vgood'],
['high','vhigh','2','4','big','med','vgood']
]


def testReadExamples():
	examples = populateExamples('car/train.csv')
	if len(examples) != 1000:
		notes.append("Ended with the wrong number of examples read from file.")
		return False
	else:
		return True


def testNoLabels():
	if allSameLabels([]):
		return True
	else:
		notes.append('There were no labels, so it should be impossible for the labels to be different.')
		return False


def testOneLabel():
	examples = [['', '', '', '', '', '', 'acc']]
	if allSameLabels(examples):
		return True
	else:
		notes.append('There was only one label, so it has to be the same as itself.')
		return False


def testAllLabelsSame():
	examples = [['', '', '', '', '', '', 'acc'], ['', '', '', '', '', '', 'acc'], ['', '', '', '', '', '', 'acc']]
	if allSameLabels(examples):
		return True
	else: 
		notes.append('All the labels are the same, but they were found to be different.')
		return False


def testLabelsDiff():
	examples = [['', '', '', '', '', '', 'acc'], ['', '', '', '', '', '', 'uacc'], ['', '', '', '', '', '', 'good']]
	if allSameLabels(examples):
		notes.append('All the labels are different, but they were found to be the same.')
		return False
	else:
		return True


def testNumUnacc():
	if numLabelVals(label_examples, 'unacc') == 4:
		return True
	else:
		notes.append('Expected to find 4 labels with value of unacc, but found a different number.')
		return False


def testNumAcc():
	if numLabelVals(label_examples, 'acc') == 1:
		return True
	else:
		notes.append('Expected to find 1 label with value of acc, but found a different number.')
		return False


def testNumGood():
	if numLabelVals(label_examples, 'good') == 2:
		return True
	else:
		notes.append('Expected to find 2 labels with value of good, but found a different number.')
		return False


def testNumVgood():
	if numLabelVals(label_examples, 'vgood') == 3:
		return True
	else:
		notes.append('Expected to find 3 labels with value of vgood, but found a different number.')
		return False


def testEntropy():
	exp_entropy = 1.8464393446710154
	calc_entropy = entropy(label_examples, attr_vals[6])
	if calc_entropy == exp_entropy:
		return True
	else:
		note = 'Expected entropy to be', exp_entropy, 'but it was', calc_entropy, 'instead.'
		notes.append(note)
		return False


def testExamplesSubset():
	exp_subset = [
		['high','vhigh','4','2','small','high','vgood'],
		['high','high','3','more','med','med','vgood'],
		['high','vhigh','2','4','big','med','vgood']
	]
	calc_subset = exampleSubset(label_examples, 'buying', 'high')
	if exp_subset == calc_subset:
		return True
	else:
		notes.append('Found the wrong subset of examples for attr \'buying\' and value \'high\'')
		return False


def testAttrsSubset():
	attrs = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
	exp_subset = ['buying', 'maint', 'doors', 'persons', 'lug_boot']
	calc_subset = attrSubset(attrs, 'safety')
	if exp_subset == calc_subset:
		return True
	else:
		notes.append('Expected safety to be removed from the attributes set, but it was not')
		return False


def testCommonVal():
	exp_val = 'unacc'
	calc_val = commonValue(label_examples, 'label')
	if exp_val == calc_val:
		return True
	else:
		notes.append('Expected to find the common value of label to be unacc, but it was not')
		return False


def testInfoGain():
	print(infoGain(label_examples, attr_names[0]))
	print(infoGain(label_examples, attr_names[1]))
	print(infoGain(label_examples, attr_names[2]))
	print(infoGain(label_examples, attr_names[3]))
	print(infoGain(label_examples, attr_names[4]))
	print(infoGain(label_examples, attr_names[5]))

	return True


tests_run +=1
if testReadExamples():
	tests_passed +=1
tests_run+=1
if testNoLabels():
	tests_passed +=1
tests_run+=1
if testOneLabel():
	tests_passed +=1
tests_run+=1
if testAllLabelsSame():
	tests_passed +=1
tests_run+=1
if testLabelsDiff():
	tests_passed +=1
tests_run+=1
if testNumUnacc():
	tests_passed+=1
tests_run+=1
if testNumAcc():
	tests_passed+=1
tests_run+=1
if testNumGood():
	tests_passed+=1
tests_run+=1
if testNumVgood():
	tests_passed+=1
tests_run+=1
if testEntropy():
	tests_passed+=1
tests_run+=1
if testInfoGain():
	tests_passed+=1
tests_run+=1
if testExamplesSubset():
	tests_passed+=1
tests_run+=1
if testAttrsSubset():
	tests_passed+=1
tests_run+=1
if testCommonVal():
	tests_passed+=1


if tests_run == tests_passed:
	print("All tests passed successfully!")
else:
	print("Failed", tests_run - tests_passed, "tests")
	for note in notes:
		print(note)


