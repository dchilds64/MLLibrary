test_variable = True


def testFunc():
    global test_variable
    test_variable = False
    otherFunc()


def otherFunc():
    print(test_variable)


print(int(11 / 2))
print(int(10 / 2))
print(int(10 / 2) - 1)
