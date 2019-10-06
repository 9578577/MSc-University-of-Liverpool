import time
import evaluation
import numpy as np
from copy import deepcopy

def eucledian_distance(a, b):
    return np.sqrt(np.sum((a - b) * (a - b)))

def manhattan_distance(a, b):
    return np.sum(np.absolute(a - b))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.sqrt(np.dot(a, a)) * np.sqrt(np.dot(b, b)))
    
def algorithm(X, k, dist_measure, n_converged):
    n = len(X) # Determine the length of our dataset
    centroids = np.zeros([k, len(X[0])]) # Matrix to hold the centroids
    distances = np.zeros([n, k]) # Matrix to hold distances between all features and centroids
    clusters = np.zeros([n]) # Vector to hold the cluster that each feature is assigned to

    # Initialise clusters
    centroids = [X[np.random.randint(len(X[0]))] for i in range(k)]

    # Variables to hold number of epochs and a tally of how many
    # epochs the algorithm converged for
    epoch = 0
    converged = 0

    # We check for convergence by determining if the clusters that each data point is assign to
    # has changed at all. If they haven't for n epochs, we terminate our algorithm.    
    while converged < n_converged:
        epoch += 1
        
        
        # Take the previous clusters
        prev_clusters = deepcopy(clusters)
        
        # Calculate distances and update classifications
        for i in range(n):
            # Calculate distances between all centroids
            for j in range(k):
                # Check which distance measure is set and use that
                if dist_measure == "manhattan":
                    distances[i, j] = manhattan_distance(X[i], centroids[j])
                elif dist_measure == "cosine":
                    distances[i, j] = cosine_similarity(X[i], centroids[j])
                else:
                    distances[i, j] = eucledian_distance(X[i], centroids[j])
            
            # Update the class of this data
            if dist_measure == "cosine":
                clusters[i] = np.argmax(distances[i, :])
            else:
                clusters[i] = np.argmin(distances[i, :])
        
        # Update the centroids
        for i in range(k):
            if(len(X[clusters == i]) > 0):
                points = X[clusters == i]
                centroids[i] = np.mean(points, 0)
        
        # Check for convergence
        if np.array_equal(clusters, prev_clusters):
            converged += 1
        else:
            converged == 0
            
        print("[", end="")
        for i in range(k):
            count = 0
            for j in range(len(clusters)):
                if i == clusters[j]:
                    count += 1
            if i < k-1:
                print(count, end=" ")
            else:
                print(count, end="")
                
        print("]")
        time.sleep(1)
    
    print("[k = "+str(k)+"] Converged after " + str(epoch-converged) + " epochs")
    epoch_converged = epoch - converged
    return clusters, epoch_converged

def run(X, classes, k, runs, distance_measure, n_converged=5):
    
    precisions = []
    recalls = []
    fscores = []
    ris = []
    epochs = []
    
    for run in range(runs):
        # Run k-Means algorithm
        clusters, epoch = algorithm(X, k, distance_measure, n_converged)
        
        # Evaluate our classifier
        p, r, f, ri = evaluation.run(classes, clusters)
        
        # Append metrics for this run
        precisions.append(p)
        recalls.append(r)
        fscores.append(f)
        ris.append(ri)
        epochs.append(epoch)
    
    
    return precisions, recalls, fscores, ris, epochs