import numpy as np
import plotgraph

def train(train_data, test_data, num_elements, num_classes, epochs, messages, shuffle):
    '''
    Train multiclass perceptron algorithm
    
    :param   train_data
    :param   num_elements
    :param   num_classes
    :param   epochs
    :param   messages
    :return  w
    :return  b
    '''
    
    # Initialise weight and bias
    w = np.zeros(shape=(num_classes, num_elements))
    b = np.zeros(num_classes)
    
    # List to hold the accuracy per epoch
    train_per_epoch = [[0 for i in range(epochs)] for i in range(num_classes)]
    test_per_epoch = [[0 for i in range(epochs)] for i in range(num_classes)]
    
    for i in range(epochs):
        errors = [0 for c in range(num_classes)]
        for j in range(num_classes):
            if shuffle == True: np.random.shuffle(train_data[j]) # Shuffle train data at each epoch for each set
            for row in range(len(train_data[0])):
                X = train_data[j][row][1]
                y = train_data[j][row][0]
                a = np.dot(X, w[j]) + b[j]
                if(y * a) <= 0:
                    errors[j] += 1
                    w[j] = w[j] + (y * X)
                    b[j] = b[j] + y

        # Test perceptron
        classifier_accuracy, perceptron_accuracy = test(test_data, w, b, num_classes, False)
        
        # Append errors
        for c in range(num_classes):
            train_per_epoch[c][i] += 1 - (errors[c] / len(train_data[0]))     
            test_per_epoch[c][i] += classifier_accuracy[c]
        
        if messages == True:
            print("\n---- Epoch " + str(i) + " ----")
            print("Weights: " + str(w))
            print("Bias: " + str(b))
            print("Misclassified instances: " + str(errors))    
    
    # Calculate accuracies for each classifier over all epochs
    overall_accuracies = [(sum(train_per_epoch[i]) / epochs) * 100 for i in range(num_classes)]
    if messages == True:
        print("Classifier accuracies " + str(overall_accuracies))
        print("Overall accuracy: " + str((sum(overall_accuracies) / num_classes)))
    
    return w, b, train_per_epoch, test_per_epoch, overall_accuracies

def l2_train(train_data, test_data, num_elements, num_classes, lam, epochs, messages, shuffle):
    '''
    Train multiclass perceptron algorithm using l2 regularisation
    
    :param   train_data
    :param   num_elements
    :param   num_classes
    :param   lam
    :param   epoch
    :param   messages
    :return  w
    :return  b
    '''
    
    # Initialise weight and bias
    w = np.zeros(shape=(num_classes, num_elements))
    b = np.zeros(num_classes)
    
    # List to hold the accuracy per epoch
    train_per_epoch = [[0 for i in range(epochs)] for i in range(num_classes)]
    test_per_epoch = [[0 for i in range(epochs)] for i in range(num_classes)]
    
    for i in range(epochs):
        errors = [0 for c in range(num_classes)]
        for j in range(num_classes):
            if shuffle == True: np.random.shuffle(train_data[j]) # Shuffle train data at each epoch for each set
            for row in range(len(train_data[0])):
                X = train_data[j][row][1]
                y = train_data[j][row][0]
                a = np.dot(X, w[j]) + b[j]
                if(y * a) <= 0:
                    errors[j] += 1
                    w[j] = w[j] + (y * X) - (2 * lam * w[j])
                    b[j] = b[j] + y

        # Test perceptron
        classifier_accuracy, perceptron_accuracy = test(test_data, w, b, num_classes, False)

        # Append errors
        for c in range(num_classes):
            train_per_epoch[c][i] += 1 - (errors[c] / len(train_data[0]))     
            test_per_epoch[c][i] += classifier_accuracy[c]

        if messages == True:
            print("\n---- Epoch " + str(i) + " ----")
            print("Weights: " + str(w))
            print("Bias: " + str(b))
            print("Misclassified instances: " + str(errors))

    # Calculate accuracies for each classifier over all epochs
    overall_accuracies = [(sum(train_per_epoch[i]) / epochs) * 100 for i in range(num_classes)]
    if messages == True:
        print("Classifier accuracies " + str(overall_accuracies))
        print("Overall accuracy: " + str((sum(overall_accuracies) / num_classes)))
    
    return w, b, train_per_epoch, test_per_epoch, overall_accuracies

def test(test_data, w, b, num_classes, messages):
    '''
    Test the perceptron algorithm
    
    :param  test_data
    :param  w
    :param  b
    :return classes
    '''
    
    class_error = [0 for i in range(num_classes)]
    perceptron_error = 0
    
    for i in range(len(test_data[0])):
        predictions = []
        y = [0, 0, 0]
        for j in range(num_classes):
            X = test_data[j][i][1]
            y[j] = test_data[j][i][0]
            a = np.dot(X, w[j]) + b[j]
            predictions.append(a) # Append the class prediction to list
            # Check if there's an error
            if (y[j] * a) <= 0:
                class_error[j] += 1
        
        # Append our perceptrons prediction to list
        if messages == True: print("Predicted: " + str(np.argmax(predictions) + 1) + " Expected: " + str(np.argmax(y) + 1))
        if not (np.argmax(y) + 1) == (np.argmax(predictions) + 1):
            perceptron_error += 1

    # Calculate classifier accuracies
    class_error = [(class_error[i] / len(test_data[0])) for i in range(num_classes)]
    classifier_accuracy = [((1 - class_error[i]) * 100) for i in range(num_classes)]
    perceptron_accuracy = 1 - (perceptron_error / len(test_data[0]))
    
    if messages == True:
        print("Classifier accuracies: " + str(classifier_accuracy))
    return classifier_accuracy, perceptron_accuracy

def algorithm(test_data, train_data, num_elements, num_classes, epochs, runs, l2_multiclass, lam, messages, shuffle):
    '''
    Call the perceptron algorithm
    
    :param  test_data
    :param  w
    :param  b
    '''
    train_accuracy_per_run = [[0 for i in range(epochs)] for i in range(num_classes)]
    test_accuracy_per_run = [[0 for i in range(epochs)] for i in range(num_classes)]
    overall_train_accuracy = [0 for i in range(num_classes)]
    final_test_per_run = [0 for i in range(num_classes)]
    overall_test_accuracy = 0

    for run in range(runs):
        # Train multiclass perceptron, will use l2 regularisation if option set to true in main
        if l2_multiclass == True:
            w, b, accuracy_per_epoch, test_per_epoch, overall_accuracies = l2_train(train_data, test_data, num_elements, num_classes, lam, epochs, messages, shuffle)
        else:
            w, b, accuracy_per_epoch, test_per_epoch, overall_accuracies = train(train_data, test_data, num_elements, num_classes, epochs, messages, shuffle)

        # Test multiclass perceptron
        classifier_accuracy, perceptron_accuracy = test(test_data, w, b, num_classes, messages)
        
        # Append accuracy for this run
        for classifier in range(num_classes):
            final_test_per_run[classifier] += classifier_accuracy[classifier]
            overall_train_accuracy[classifier] += overall_accuracies[classifier]
            for epoch in range(epochs):
                train_accuracy_per_run[classifier][epoch] += accuracy_per_epoch[classifier][epoch]
                test_accuracy_per_run[classifier][epoch] += test_per_epoch[classifier][epoch]
        overall_test_accuracy += perceptron_accuracy
    
    # Normalise accuracy over n runs
    for classifier in range(num_classes):
        final_test_per_run[classifier] /= runs
        overall_train_accuracy[classifier] /= runs
        for epoch in range(epochs):
            train_accuracy_per_run[classifier][epoch] /= runs
            test_accuracy_per_run[classifier][epoch] /= runs
    overall_test_accuracy /= runs
    
    if l2_multiclass == True:
        print("Train accuracy")
        plotgraph.l2_multiperceptron_accuracy(train_accuracy_per_run, lam, 'train')
        print("Test accuracy")
        plotgraph.l2_multiperceptron_accuracy(test_accuracy_per_run, lam, 'test')
    else:
        print("Train accuracy")
        plotgraph.multiperceptron_accuracy(train_accuracy_per_run, 'train')
        print("Test accuracy")
        plotgraph.multiperceptron_accuracy(test_accuracy_per_run, 'test')
    print("Train accuracies per classifier: " + str(overall_train_accuracy))
    print("Perceptron train accuracy: " + str(sum(overall_train_accuracy) / num_classes))
    print("Test accuracies per classifier: " + str(final_test_per_run))
    print("Perceptron test accuracy: " + str(overall_test_accuracy * 100))
    