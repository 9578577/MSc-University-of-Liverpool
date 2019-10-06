import data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Set paths to test and train data files
test_path = "../data/test.data"
train_path = "../data/train.data"

### DATA ###
class_element = 4
number_features = 4 # The number of features per X
number_classes = 3 # Number of classes

### BINARY DATA SETTINGS ###
class_remove = "1" # The class to drop for 1vs1
positive_class = "2" # Which class will be +ve in 1vs1

### PERCEPTRON SETTINGS ###
runs = 500 # How many times should we run the perceptron to calculate average accuracy?
epochs = 1000 # Number of epochs the algorithm should run for
learning_rate = 0.01 # Set the learning rate for the classifier

def plot(accuracy_per_epoch, class_remove, number_classes, type):
    classes = [(i+1) for i in range(number_classes)]
    classes = [y for y in classes if y != int(class_remove)]
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.plot(range(len(accuracy_per_epoch)), accuracy_per_epoch, label=(str(classes[0]) + " vs " + str(classes[1])))
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right", prop={'size': 10})
    if type == "train":
        plt.savefig("charts/train_" + str(classes[0]) + " vs " + str(classes[1]))
    else:
        plt.savefig("charts/test_" + str(classes[0]) + " vs " + str(classes[1]))
    plt.show()
    return

def train(train_data, test_data, epochs, learning_rate, num_elements):
    train_per_epoch = [0 for epoch in range(epochs)]
    test_per_epoch = [0 for epoch in range(epochs)]
    
    w = np.zeros(num_elements)
    for epoch in range(epochs):
        errors = 0
        for row in train_data:
            X = row[1] # Isolate features
            t = row[0] # Isolate class
            
            # Sigmoid activation function
            # y = 1 / (1 + np.exp(-np.dot(X, w)))
            y = np.dot(X, w)

            if y > 0:
                y = 1
            else:
                y = -1
                
            if not y == t:
                errors += 1
                w = w - (learning_rate * (y - t) * X)
        
        # Append epoch errors
        train_per_epoch[epoch] += (1 - (errors / len(train_data)))
        test_per_epoch[epoch] += test(test_data, w)
                
    return w, train_per_epoch, test_per_epoch

def test(test_data, w):
    error = 0
    for row in test_data:
        X = row[1]
        t = row[0]
        
        # Classify features
        # y = 1 / (1 + np.exp(-np.dot(X, w)))
        y = np.dot(X, w)

        if y > 0:
            y = 1
        else:
            y = -1
            
        if not y == t:
            # print("Test error, expected " + str(t) + ", predicted " + str(np.sign(y).astype(int)))
            error += 1
    
    accuracy = (1 - (error / len(test_data)))
    # print("Accuracy " + str(accuracy))
    
    return accuracy

if __name__ == "__main__":
    ### MAIN ###
    print("\nTraining and testing logistic regression algorithm")
    
    # Read test and train files
    test_raw, train_raw = data.read(test_path, train_path)
    
    # Preprocess data
    test_data, train_data = data.binary_preprocess(test_raw, train_raw, class_element, class_remove, positive_class)
    
    # Hold errors over n runs
    train_accuracy_per_epoch = [0 for i in range(epochs)]
    test_accuracy_per_epoch = [0 for i in range(epochs)]

    for run in range(runs):
        # Train binary perceptron
        w, train_per_epoch, test_per_epoch = train(train_data, test_data, epochs, learning_rate, number_features)
                
        # Append the accuracies for this run
        for epoch in range(epochs):
            train_accuracy_per_epoch[epoch] += (train_per_epoch[epoch] * 100)
            test_accuracy_per_epoch[epoch] += (test_per_epoch[epoch] * 100)

    # Normalise accuracy over n runs
    for epoch in range(epochs):
        train_accuracy_per_epoch[epoch] /= runs
        test_accuracy_per_epoch[epoch] /= runs
    
    # Increment epoch accuracy and run accuracy
    print("Train accuracy per epoch")
    plot(train_accuracy_per_epoch, class_remove, number_classes, "train")
    print("Test accuracy per epoch")
    plot(test_accuracy_per_epoch, class_remove, number_classes, "test")

