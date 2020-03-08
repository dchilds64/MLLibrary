import random

r = 0.1
label_index = 4
max_epochs = 10
weights = [0.00001, 0.00001, 0.00001, 0.00001]

# Reads in the examples from a .csv file and puts them into the examples array
# file_name: The file where the examples are located
def populate_examples(file_name):
    examples = []
    with open(file_name, 'r') as f:
        for line in f:
            terms = line.strip().split(',')
            examples.append(terms)
    return examples


def make_prediction(ex):
    prediction = 0
    for i in range(0, label_index):
        prediction += weights[i] * float(ex[i])
    return prediction


def is_error(prediction, ex):
    return prediction * get_label(ex) < 0


def update_weights(ex):
    for i in range(0, label_index):
        weights[i] = weights[i] + r * (get_label(ex) * float(ex[i]))


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


def perceptron(examples):
    for ex in examples:
        prediction = make_prediction(ex)
        # Update the weights
        if is_error(prediction, ex):
            update_weights(ex)


def standard_perceptron(examples):
    for epoch in range(0, max_epochs):
        random.shuffle(examples)
        perceptron(examples)


def get_label(ex):
    return (int(ex[label_index]) * 2) - 1


examples = populate_examples('bank-note/train.csv')
standard_perceptron(examples)

evaluate_examples(examples, 'EVALUATING TRAINING EXAMPLES')
test_examples = populate_examples('bank-note/test.csv')
evaluate_examples(test_examples, 'EVALUATING TEST EXAMPLES')
