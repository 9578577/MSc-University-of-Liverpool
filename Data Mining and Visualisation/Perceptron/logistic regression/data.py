import re
import numpy as np

def read(test_path, train_path):
    '''
    Read the test and train data
    
    :param  test_path    path to the test data file
    :param  train_path   path to the train data file
    :return test_raw     variable containing raw test data
    :return train_raw    variable containing raw train data
    '''
    
    test_raw = open(test_path, "r")
    train_raw = open(train_path, "r")
    
    return test_raw, train_raw

def binary_preprocess(test_raw, train_raw, class_element, class_remove, positive_class):
    '''
    Preprocess the data before training the binary perceptron algorithm,
    returns test and train data in the form [class, array(features)]
    
    :param   test_raw        variable containing the raw test data
    :param   train_raw       variable containing the raw training data
    :param   class_element   position of element relating to the class
    :param   class_remove    class to remove from the data
    :param   positive_class  the class that will be labeled as positive  
    :return  test_data       variable containing processed test data
    :return  train_data      variable containing processed train data
    '''
    
    test_data = []
    train_data = []
    
    # Iterate through the test data
    for row in test_raw:
        temp = row.split(",")
        y = temp[class_element] # Isolate the class element
        del temp[class_element] # Remove the class element from the list
        y = re.sub("\D", "", y) # Remove all characters but numbers
        if not(class_remove) in y:
            if positive_class in y:
                y = 1
            else:
                y = -1
            test_data.append([y, np.array(temp).astype(np.float)])    
    
    # Iterate through the train data
    for row in train_raw:
        temp = row.split(",")
        y = temp[class_element] # Isolate the class element
        del temp[class_element] # Remove the class element from the list
        y = re.sub("\D", "", y) # Remove all characters but numbers
        if not(class_remove) in y:
            if positive_class in y:
                y = 1
            else:
                y = -1
            train_data.append([y, np.array(temp).astype(np.float)])
    
    print("\nRemoved class " + str(class_remove) + ". Class " + str(positive_class) + " set equal to 1.")
    print("Test set consists of " + str(len(test_data)) + " features and train set consists of " + str(len(train_data)))
    return test_data, train_data

def multi_preprocess(test_raw, train_raw, class_element, number_classes):
    '''
    Preprocess the data before training the multiclass perceptron algorithm
    returns rest and train data in the form [class, array(features)]
    
    :param   test_raw
    :param   target_raw
    :param   target_element
    :param   number_classes
    :return  test_data
    :return  train_data
    '''
    
    test_raw = [line for line in test_raw]
    train_raw = [line for line in train_raw] 
    test_data = [[] for i in range(number_classes)]
    train_data = [[] for i in range(number_classes)]
        
    # Iterate through the test data
    for j in range(number_classes):
        for row in test_raw:
            temp = row.split(",")
            y = temp[class_element] # Isolate the class element
            del temp[class_element] # Remove the class element from the list
            y = re.sub("\D", "", y) # Remove all characters but numbers
            if str(j + 1) in y:
                y = 1
            else:
                y = -1
            test_data[j].append([y, np.array(temp).astype(np.float)])     
    
    # Iterate through the train data
    for j in range(number_classes):
        for row in train_raw:
            temp = row.split(",")
            y = temp[class_element] # Isolate the class element
            del temp[class_element] # Remove the class element from the list
            y = re.sub("\D", "", y) # Remove all characters but numbers
            if str(j + 1) in y:
                y = 1
            else:
                y = -1
            train_data[j].append([y, np.array(temp).astype(np.float)])   
            
    return test_data, train_data