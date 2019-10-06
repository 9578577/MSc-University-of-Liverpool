import re
import numpy as np

def l2_normalisation(data, check_norms=False):
    n = len(data)
    for i in range(0,n):
        norm = np.sqrt(np.sum(data[i,:] * data[i,:]))
        data[i,:] = data[i,:] / norm
    
    if check_norms == True:
        for i in range(0,len(data)):
            print(i, np.sqrt(np.sum(data[i,:] * data[i,:])))
        
    return data

def read_data(data_files, class_element, l2_norm=False):
    data = []
    classes = []
  
    # Loop through all files
    for i, file in enumerate(data_files):
        # Open the file
        read_data = open("./data/" + str(file), "r")
        
        # Loop through each line in the data file
        for line in read_data:
            temp = line.split() # Split into tokens
            del temp[class_element] # Delete the class element from our list
            temp = [re.sub("\D-", "", temp[i]) for i in range(len(temp))] # Remove spaces from elements
            data.append(temp)
            classes.append(i)
    
    # Convert our data list to a numpy array and return
    data = np.array(data).astype(np.float)
    classes = np.array(classes).astype(np.int)
    
    # We will l2 normalise the dataset if set to true
    if l2_norm == True:
        data = l2_normalisation(data)
    
    return data, classes