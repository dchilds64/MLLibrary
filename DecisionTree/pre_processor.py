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
