import numpy as np

def confusionMatrix(classes, clusters):
    n = len(classes) # Take length of our data
    
    # Instantiate variables to hold counts
    true_positive = false_positive = true_negative = false_negative = 0
    
    # Loop through all pairs within our classes and clusters
    for i in range(n):
        for j in range(i, n):
            if classes[i] == classes[j] and clusters[i] == clusters[j]:
                true_positive += 1
            elif classes[i] != classes[j] and clusters[i] == clusters[j]:
                false_positive += 1
            elif classes[i] != classes[j] and clusters[i] != clusters[j]:
                true_negative += 1
            elif classes[i] == classes[j] and clusters[i] != clusters[j]:
                false_negative += 1
        
    return [true_positive, false_positive, true_negative, false_negative]

def precision(confusion_matrix):
    return confusion_matrix[0] / (confusion_matrix[0] + confusion_matrix[1])

def recall(confusion_matrix):
    return confusion_matrix[0] / (confusion_matrix[0] + confusion_matrix[3])

def fscore(confusion_matrix):
    return (2 * precision(confusion_matrix) * recall(confusion_matrix)) / (precision(confusion_matrix) + recall(confusion_matrix))

def RI(confusion_matrix):
    return (confusion_matrix[0] + confusion_matrix[2]) / (np.sum(confusion_matrix))

def run(classes, clusters):
    confusion_matrix = confusionMatrix(classes, clusters)
    p = precision(confusion_matrix)
    r = recall(confusion_matrix)
    f = fscore(confusion_matrix)
    ri = RI(confusion_matrix)
    return p, r, f, ri