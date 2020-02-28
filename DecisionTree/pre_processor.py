from dec_tree import *


# Goes through the examples provided and pulls the possible values of each of the attributes.
def learnDataFormat(examples):
    attr_vals = []

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
    return attr_vals


# Goes through the examples provided and finds the common values for each of the attributes.
def findCommonAttrVals(examples, attrs, attr_vals):
    common_vals = []
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
    return common_vals


def remove_unknown(examples, test_examples, attr_vals):
    common_vals = findCommonAttrVals(examples)
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
