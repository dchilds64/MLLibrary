test_variable = True

def testFunc():
  global test_variable
  test_variable = False
  otherFunc()


def otherFunc():
  print(test_variable)


testFunc()