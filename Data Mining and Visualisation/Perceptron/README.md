# COMP526 Assignment 1 Perceptron

This assignment aims to implement a binary and multiclass perceptron.

## Prerequisites

Python must be installed on the machine to run this code. The required packages are listed below.

### Packages

All packages used are available through pip

* Matplotlib
* Numpy

## Running

The program is divided up into separate modules for data handling, perceptron implementations and graph plotting. To run the program you will need to execute main.py; you can modify the environment variables in main.py to run the different perceptron implementations. Each section of variables is discussed below.

### Data Settings
#### General
* *class_element* What is the index of the class in each row of the dataset?
* *num_classes* How many classes are in the dataset? 
* *num_features* How many features in each row of the dataset?

#### Binary Perceptron
* *class_remove* which class should we remove from the train/test sets?
* *positive_class* Which class should be positive?

### Perceptron Variables
* *binary_perceptron* Set to True to use the binary perceptron or False to use multiclass perceptron
* *l2_multiclass* Set to True to use l2 regularisation with the multiclass perceptron or False to turn it off

### Perceptron Settings
* *lam* The value of lambda for l2 regularisation
* *epoch* How many epochs should we train the perceptron for
* *runs* How many times should we run the algorithm to calculate average accuracy
* *messages* Report perceptron performance at each epoch, set to True to turn on
* *shuffle* Shuffle data at the start of each epoch, set to True to enable