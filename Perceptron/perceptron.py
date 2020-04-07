import random

r = 0.1
label_index = 5
max_epochs = 10
weights = [0.00001, 0.00001, 0.00001, 0.00001, 0.00001]
weights_set = []
weights_total = [0, 0, 0, 0, 0]
counts = []
count = 1


# Reads in the examples from a .csv file and puts them into the examples array
# file_name: The file where the examples are located
def populate_examples(file_name):
    examples = []
    with open(file_name, 'r') as f:
        for line in f:
            terms = line.strip().split(',')
            examples.append(terms)
    add_biases(examples)
    return examples


def add_biases(examples):
    for ex in examples:
        ex.insert(label_index - 1, 1)


# Prediction functions

def make_prediction(ex):
    prediction = 0
    for i in range(0, label_index):
        prediction += weights[i] * float(ex[i])
    return prediction


def make_voted_prediction(ex):
    prediction = 0
    for i in range(0, len(weights_set)):
        sub_prediction = 0
        for j in range(0, len(weights_set[i])):
            sub_prediction += weights_set[i][j] * float(ex[j])
        prediction += counts[i] * sub_prediction
    return prediction


def make_averaged_prediction(ex):
    prediction = 0
    for i in range(0, label_index):
        prediction += weights_total[i] * float(ex[i])
    return prediction


def is_error(prediction, ex):
    return prediction * get_label(ex) < 0


def update_weights(ex):
    for i in range(0, label_index):
        weights[i] = weights[i] + r * (get_label(ex) * float(ex[i]))


def update_weights_total():
    for i in range(0, label_index):
        weights_total[i] += weights[i]


# Example evaluation functions

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


def evaluate_voted_examples(examples, header):
    print(header)
    incorrect = 0
    total = len(examples)
    for ex in examples:
        prediction = make_voted_prediction(ex)
        if is_error(prediction, ex):
            incorrect += 1
    print('Evaluated', total, 'examples')
    print('Got', incorrect, 'examples wrong')
    print('Error percentage: ', round((incorrect / total) * 100, 3), '%', sep='')
    print()


def evaluate_averaged_examples(examples, header):
    print(header)
    incorrect = 0
    total = len(examples)
    for ex in examples:
        prediction = make_averaged_prediction(ex)
        if is_error(prediction, ex):
            incorrect += 1
    print('Evaluated', total, 'examples')
    print('Got', incorrect, 'examples wrong')
    print('Error percentage: ', round((incorrect / total) * 100, 3), '%', sep='')
    print()


# Perceptron Algorithm Variants

def standard_perceptron(examples, test_examples):
    for epoch in range(0, max_epochs):
        random.shuffle(examples)
        for ex in examples:
            prediction = make_prediction(ex)
            # Update the weights
            if is_error(prediction, ex):
                update_weights(ex)
    print('Learned weights vector:', weights)
    evaluate_examples(examples, 'EVALUATING TRAINING EXAMPLES')
    evaluate_examples(test_examples, 'EVALUATING TEST EXAMPLES')


def voted_perceptron(examples, test_examples):
    global count
    for epoch in range(0, max_epochs):
        random.shuffle(examples)
        for ex in examples:
            prediction = make_prediction(ex)
            if is_error(prediction, ex):
                weights_set.append(weights.copy())
                counts.append(count)
                # print(round(weights[0], 2), '&', round(weights[1], 2), '&', round(weights[2], 2), '&', round(weights[3], 2), '&', round(weights[4], 2), '&', count, '\\\\ ', '\hline', sep='')
                update_weights(ex)
                count = 1
            else:
                count += 1
    evaluate_voted_examples(examples, 'EVALUATING TRAINING EXAMPLES')
    evaluate_voted_examples(test_examples, 'EVALUATE TEST EXAMPLES')


def averaged_perceptron(examples, test_examples):
    global weights_total
    for epoch in range(0, max_epochs):
        random.shuffle(examples)
        for ex in examples:
            prediction = make_prediction(ex)
            if is_error(prediction, ex):
                update_weights(ex)
            update_weights_total()
    evaluate_averaged_examples(examples, 'EVALUATING TRAINING EXAMPLES')
    evaluate_averaged_examples(test_examples, 'EVALUATE TEST EXAMPLES')


def get_label(ex):
    return (int(ex[label_index]) * 2) - 1


examples = populate_examples('bank-note/train.csv')
test_examples = populate_examples('bank-note/test.csv')
standard_perceptron(examples, test_examples)
