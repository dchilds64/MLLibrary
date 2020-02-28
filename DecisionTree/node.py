# A class representing nodes in a decision tree.
# name: The name of the node. If the node is a leaf node, the name is a value 
# 	of the label for the training data.
# children: A dictionary where the key is a value the attribute named by name can take,
#		and the value is a node, representing another attribute.
class Node:
  def __init__(self, name, children):
    self.name = name
    self.children = children
