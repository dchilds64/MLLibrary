import math
from node import *


attr_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'label']
attr_vals = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
max_depth = 6
#purity_measure = 'gini'
purity_measure = 'entropy'
#purity_measure = 'error'


# Determines whether all the examples in the set e have the same label
# Returns True if so, False otherwise
# ex: An array containing the examples to be tested
def allSameLabels(e):
	if len(e) == 0:
		return True
	else:
		label = e[0][6]
		for ex in e:
			if ex[6] != label:
				return False
	return True


# Reads in the examples from a .csv file and puts them into the examples array
# file_name: The file where the examples are located
def populateExamples(file_name):
	examples = []
	with open(file_name, 'r') as f:
		for line in f:
			terms = line.strip().split(',')
			examples.append(terms)
	return examples


def numLabelVals(examples, val):
	ctr = 0
	for ex in examples:
		if ex[6] == val:
			ctr += 1
	return ctr


# Takes a set of examples and calculates the entropy for them based on the labels they can
# take. 
# examples: The set of examples to calculate the entropy for.
# label_vals: The values the labels for the examples can take.
def entropy(examples, label_vals):
	# TODO: This isn't quite general yet, because I am assuming the format of the examples,
	# should look at this based on the format of the examples instead.
	num_examples = len(examples)
	entropy = 0.0
	
	if num_examples == 0:
		return entropy
	
	# For each value the label can take, get the ratio of examples with that value for their
	# label and use it to calculate the portion of the entropy for that the examples with 
	# that value.
	for val in label_vals:
		ratio = numLabelVals(examples, val) / num_examples
		if ratio > 0.0:
			entropy -= ratio*math.log(ratio, 2)
	return entropy


# Returns a subset of the examples where the attribute takes the value provided.
# examples: The superset of examples to be filtered.
# attr: The attribute in the examples to be filtered on.
# val: The desired value of the given attribute 
def exampleSubset(examples, attr, val):
	subset = []
	attr_index = attr_names.index(attr)
	for ex in examples:
		if ex[attr_index] == val:
			subset.append(ex)
	return subset


def attrSubset(attrs, attr):
	subset = []
	for a in attrs:
		if a != attr:
			subset.append(a)
	return subset


def commonValue(examples, attr):
	attr_index = attr_names.index(attr)
	vals = attr_vals[attr_index]
	highest_count = 0
	selected_val = ''
	for val in vals:
		count = 0
		for example in examples:
			if example[attr_index] == val:
				count += 1
		if count > highest_count:
			highest_count = count
			selected_val = val
	return selected_val


# This really needs to be tested somehow
def infoGain(examples, attr):
	if purity_measure == 'entropy':
		parent_entropy = entropy(examples, attr_vals[6])
		attr_index = attr_names.index(attr)
		values = attr_vals[attr_index]
		for val in values:
			# calculate sub entropy
			sub_examples = []
			for ex in examples:
				if ex[attr_index] ==  val:
					sub_examples.append(ex)
			sub_entropy = entropy(sub_examples, attr_vals[6])	
			parent_entropy -= (len(sub_examples)/len(examples))*sub_entropy
		return parent_entropy
	elif purity_measure == 'gini':
		attr_index = attr_names.index(attr)
		values = attr_vals[attr_index]
		parent_gini = giniIndex(examples, attr_names[6])
		for val in values:
			sub_examples = []
			for ex in examples:
				if ex[attr_index] == val:
					sub_examples.append(ex)
			sub_gini = giniIndex(sub_examples, attr_names[6])
			parent_gini -= (len(sub_examples)/len(examples))*sub_gini
		return parent_gini
	else:
		attr_index = attr_names.index(attr)
		values = attr_vals[attr_index]
		parent_error = majorityError(examples, attr_names[6])
		for val in values:
			sub_examples = []
			for ex in examples:
				if ex[attr_index] == val:
					sub_examples.append(ex)
			sub_error = majorityError(sub_examples, attr_names[6])
			parent_error -= (len(sub_examples)/len(examples))*sub_error
		return parent_error


# Calculates the error in the examples set if the common label were chosen
# for all examples.
# examples: The set of examples to calculate the majority error over.
# attr: The attribute to calculate majority error on
def majorityError(examples, attr):
	majority_label = commonValue(examples, attr)
	attr_index = attr_names.index(attr)
	num_examples = len(examples)
	
	if num_examples == 0:
		return 0.0

	count = 0
	for ex in examples:
		if ex[attr_index] != majority_label:
			count += 1
	return count / num_examples


def numVals(examples, attr, val):
	count = 0
	attr_index = attr_names.index(attr)
	for ex in examples:
		if ex[attr_index] == val:
			count += 1
	return count


def giniIndex(examples, attr):
	index = 1.0
	num_examples = len(examples)
	
	if num_examples == 0:
		return index

	attr_index = attr_names.index(attr)
	vals = attr_vals[attr_index]
	for val in vals:
		num_vals = numVals(examples, attr, val)
		ratio = num_vals / num_examples
		index -= pow(ratio, 2)
	return index


# Needs test
def pickBestAttrGain(examples, attrs):
	lowest_info_gain = 1000000.0
	selected_attr = ''
	for attr in attrs:
		gain = infoGain(examples, attr)
		if gain < lowest_info_gain:
			lowest_info_gain = gain
			selected_attr = attr
	return selected_attr


def id3(examples, attrs, label, depth):
	if len(examples) < 1:
		return Node("", {})

	if allSameLabels(examples):
		return Node(examples[0][6], {})

	selected_attr = pickBestAttrGain(examples, attrs)
	root = Node(selected_attr, {})
	attr_index = attr_names.index(selected_attr)
	vals = attr_vals[attr_index]
	for val in vals:
		sub_examples = exampleSubset(examples, selected_attr, val)
		sub_attrs = attrSubset(attrs, selected_attr)
		if len(sub_examples) == 0 or depth == max_depth - 1:
			root.children[val] = Node(commonValue(examples, label), {})
		else:
			root.children[val] = id3(sub_examples, sub_attrs, label, depth + 1)
	return root


def attrValsContains(attr, candidate):
	attr_index = attr_names.index(attr)
	vals = attr_vals[attr_index]
	if candidate in vals:
		return True
	else:
		return False


def evaluateExample(root, example):
	node = root
	while not attrValsContains('label', node.name):
		attr_index = attr_names.index(node.name)
		node = node.children[example[attr_index]]
	return node.name

