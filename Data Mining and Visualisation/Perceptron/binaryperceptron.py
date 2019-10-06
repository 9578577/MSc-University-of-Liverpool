import numpy as np
import plotgraph

def train(train_data, test_data, num_elements, epoch, messages, shuffle):
    '''
    Train the perceptron algorithm
    
    :param  train_data
    :param  num_elements  the number of features in the dataset 
    :param  epoch
    :param  messages      print weights and bias at each iteration, turned on by default (1 = on, 0 = off)
    :return weight
    :return bias
    '''
    
    # Initialise the weights and bias
    w = np.zeros(num_elements)
    b = 0
    
    # List to hold the accuracy per epoch
    train_per_epoch = [0 for i in range(epoch)]
    test_per_epoch = [0 for i in range(epoch)]
    
    for i in range(epoch):
        if shuffle == True: np.random.shuffle(train_data) # Shuffle data at the start of each epoch
        errors = 0
        for row in train_data:
            X = row[1]
            y = row[0]
            a = np.dot(X, w) + b
            if (y * a) <= 0:
                errors += 1
                w = w + (y * X)
                b = b + y
        train_per_epoch[i] += 1 - (errors / len(train_data))
        test_per_epoch[i] += (test(test_data, w, b, False))

        if messages == True:
            print("\n---- Epoch " + str(i) + " ----")
            print("Weights: " + str(w))
            print("Bias: " + str(b))
            print("Errors: " + str(errors))
            print("Accuracy: " + str((1 - (errors / len(train_data))) * 100))
    if messages == True: print("Overall accuracy: " + str((sum(train_per_epoch) / epoch) * 100))

    return w, b, train_per_epoch, test_per_epoch

def test(test_data, w, b, messages):
    '''
    Test the perceptron algorithm
    
    :param  test_data
    :param  w
    :param  b
    :return test
    '''
    
    errors = 0
    
    for row in test_data:
        X = row[1]
        y = row[0]
        a = np.dot(w, X) + b
        if messages == True: print("Predicted: " + str(np.sign(a).astype(int)) + " Expected: " + str(int(y)))
        if (y * a) <= 0:
            errors += 1
            if messages == True: print("Encountered error when classifying, total errors: " + str(errors))
    
    accuracy = 1 - (errors / len(test_data))
   
    return accuracy

def algorithm(test_data, train_data, number_elements, epochs, runs, class_remove, number_classes, messages, shuffle):
    '''
    Call the perceptron algorithm
    
    :param  test_data
    :param  w
    :param  b
    '''
    
    train_accuracy_per_epoch = [0 for i in range(epochs)]
    test_accuracy_per_epoch = [0 for i in range(epochs)]
    accuracy = 0

    for run in range(runs):
        # Train binary perceptron
        w, b, train_per_epoch, test_per_epoch = train(train_data, test_data, number_elements, epochs, messages, shuffle)
        
        # Test binary perceptron
        total_accuracy = test(test_data, w, b, messages)
        
        # SORT
        for epoch in range(epochs):
            train_accuracy_per_epoch[epoch] += (train_per_epoch[epoch] * 100)
            test_accuracy_per_epoch[epoch] += (test_per_epoch[epoch] * 100)
        accuracy += total_accuracy

    # Normalise accuracy over n runs
    for epoch in range(epochs):
        train_accuracy_per_epoch[epoch] /= runs
        test_accuracy_per_epoch[epoch] /= runs
    accuracy /= runs
    
    # Increment epoch accuracy and run accuracy
    print("Train accuracy per epoch")
    plotgraph.perceptron_accuracy(train_accuracy_per_epoch, class_remove, number_classes, "train")
    print("Test accuracy per epoch")
    plotgraph.perceptron_accuracy(test_accuracy_per_epoch, class_remove, number_classes, "test")
    print("Train accuracy: " + str((sum(train_accuracy_per_epoch) / epochs)))
    print("Test accuracy: " + str(accuracy * 100))
    

    