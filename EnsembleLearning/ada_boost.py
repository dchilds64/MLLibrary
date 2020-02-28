from dec_tree import *

bank_attr_names = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'y']

t = 50
ctr = 0
weights = []

while ctr < t:
  ctr += 1
