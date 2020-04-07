import random

initial_rate = 0.1
d = 0.1
rate = 0.0
C = 700/873
label_index = 4
max_epochs = 100
weights = [0, 0, 0, 0, 0]


def populate_examples(file_name):
    examples = []
    with open(file_name, 'r') as f:
        for line in f:
            terms = line.strip().split(',')
            examples.append(terms)
    return examples


def get_label(ex):
    return (int(ex[label_index]) * 2) - 1


def make_prediction(ex):
    prediction = 0
    for i in range(0, label_index):
        prediction += weights[i] * float(ex[i])
    return prediction * get_label(ex)


def update_weights(ex):
    if make_prediction(ex) <= 1:
        label = get_label(ex)
        for i in range(0, len(weights)):
            weights[i] = (1 - rate) * weights[i] + rate * C * label * float(ex[i])
    else:
        for i in range(0, len(weights)):
            weights[i] = (1 - rate) * weights[i]


def update_rate(curr_epoch):
    global rate
    # rate = initial_rate / (1 + ((initial_rate * curr_epoch) / C))
    rate = initial_rate / (1 + curr_epoch)


def make_prediction(ex):
    prediction = 0
    for i in range(0, label_index):
        prediction += weights[i] * float(ex[i])
    return prediction


def is_error(prediction, ex):
    return prediction * get_label(ex) < 0


def evaluate_examples(examples, header):
    print(header)

    incorrect = 0
    total = len(examples)
    for ex in examples:
        prediction = make_prediction(ex)
        if is_error(prediction, ex):
            incorrect += 1
    print('Evaluated', total, 'examples')
    print('Got', incorrect, 'examples wrong')
    print('Error percentage: ', round((incorrect / total) * 100, 3), '%', sep='')
    print()


def subgradient_descent(examples, test_examples):
    for epoch in range(0, max_epochs):
        update_rate(epoch)
        random.shuffle(examples)
        for ex in examples:
            update_weights(ex)
    print('Learned weights vector:', weights)
    evaluate_examples(examples, 'EVALUATING TRAINING EXAMPLES')
    evaluate_examples(test_examples, 'EVALUATING TEST EXAMPLES')


train_examples = populate_examples('bank-note/train.csv')
test_examples = populate_examples('bank-note/test.csv')
subgradient_descent(train_examples, test_examples)
print(weights)
