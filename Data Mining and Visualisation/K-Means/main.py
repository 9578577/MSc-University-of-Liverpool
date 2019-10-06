# LOOK AT: K-means ++
import data
import kmeans
import graphs
import pathlib
import numpy as np

######################
# PROGRAM PARAMETERS #
######################

# A list to contain the names of all data files
data_files = ['animals', 'countries', 'fruits', 'veggies']
l2_normalisation = False # Set to true to normalise our data
distance_measure = "eucledian" # Set to either eucledian, manhattan or cosine
k_limit = 4 # Upper limit for k, we will test all k's from 0 to this value
n_runs = 1 # How many times should we run our k-means algorithm to get an avg accuracy


########################
# MAIN ALGORITHM BELOW #
########################
    
### Read in data and call the k-means algorithm ###
train_data, classes = data.read_data(data_files, 0, l2_normalisation)

# Instantiate list to hold evaluation metrics over different values of k
precision = []
max_precision = []
min_precision = []
std_precision = []
recall = []
max_recall = []
min_recall = []
std_recall = []
fscore = []
max_fscore = []
min_fscore = []
std_fscore = []
RI = []
max_RI = []
min_RI = []
std_RI = []
epoch = []
max_epoch = []
min_epoch = []

# Train our classifier for all values of k

print("Running algorithm with k = " + str(k) + "\n")

# Run k-Means algorithm
precisions, recalls, fscores, ris, epochs = kmeans.run(train_data, classes, 4, n_runs, distance_measure)
