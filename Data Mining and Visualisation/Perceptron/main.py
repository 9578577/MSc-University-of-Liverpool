import data
import binaryperceptron
import multiperceptron

# Set paths to test and train data files
test_path = "./data/test.data"
train_path = "./data/train.data"

### DATA ###
class_element = 4
number_features = 4 # The number of features per X
number_classes = 3 # Number of classes

### BINARY DATA SETTINGS ###
class_remove = "3" # The class to drop for 1vs1
positive_class = "1" # Which class will be +ve in 1vs1

### PERCEPTRON ALGORITHM ###
binary_perceptron = False # True for binary classifier, false for multiclass classifier
l2_multiclass = True # True to use l2 regularisation on the multiclass classifier

### PERCEPTRON SETTINGS ###
lam = 100 # Lambda coefficient for l2 regularisation
runs = 500 # How many times should we run the perceptron to calculate average accuracy?
epoch = 20 # Number of epochs the algorithm should run for
messages = False # Set to True to display the weights, bias and error for each epoch
shuffle = False # Set to True to shuffle the training data at the start of each epoch

### MAIN ###
if binary_perceptron == True:
    print("\nTraining and testing binary perceptron algorithm")
    
    # Read test and train files
    test_raw, train_raw = data.read(test_path, train_path)
    
    # Preprocess data
    test_data, train_data = data.binary_preprocess(test_raw, train_raw, class_element, class_remove, positive_class)
    
    # Call perceptron algorithm
    binaryperceptron.algorithm(test_data, train_data, number_features, epoch, runs, class_remove, number_classes, messages, shuffle)
    
else:
    print("\nTraining and testing multiclass perceptron algorithm")
    if(l2_multiclass) == True: print("Using lambda = " + str(lam))
    
    # Read test and train files
    test_raw, train_raw = data.read(test_path, train_path)
    
    # Preprocess data
    test_data, train_data = data.multi_preprocess(test_raw, train_raw, class_element, number_classes)
    
    # Call perceptron algorithm
    multiperceptron.algorithm(test_data, train_data, number_features, number_classes, epoch, runs, l2_multiclass, lam, messages, shuffle)