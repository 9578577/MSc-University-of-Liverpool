import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read CSV files for unigrams and bigrams
def readCSV(doc):
    df = pd.read_csv("../data/output/analysed/" + doc + '.csv', names=['Document', 'Citations', 'Link', 'Score', 'Subject Area', 'Count'], index_col=0)
    # Fill the "Count" column in with "1" to get a total count in each subject area
    df['Count'].fillna(1, inplace=True)
    # Basic statistics about the dataframe
    print(str(df.head(5)) + "\n")
    print(str(df.info()) + "\n")
    print(str(df.describe()) + "\n")
    return df

# Load the unigrams and bigrams CSV files
unigrams = readCSV("unigrams")
bigrams = readCSV("bigrams")

# Plot a graph of "Score" vs "Citations" for unigrams and bigrams
unigrams.plot(kind='scatter', x='Citations', y='Score', title='Citation Count vs Abstract Score (Unigrams)')
bigrams.plot(kind='scatter', x='Citations', y='Score', title='Citation Count vs Abstract Score (Bigrams)')

# Statistical metrics for bigrams/unigrams
print("[Unigrams] S/Ci Correlation: " + str(unigrams['Score'].corr(unigrams['Citations'])))
print("[Bigrams] S/Ci Correlation: " + str(bigrams['Score'].corr(bigrams['Citations'])))
print("[Unigrams] S/Ci Covariance: " + str(unigrams['Score'].cov(unigrams['Citations'])))
print("[Bigrams] S/Ci Covariance: " + str(bigrams['Score'].cov(bigrams['Citations'])))
print("[Unigrams] S/Co Correlation: " + str(unigrams['Score'].corr(unigrams['Count'])))
print("[Bigrams] S/Co Correlation: " + str(bigrams['Score'].corr(bigrams['Count'])))
print("[Unigrams] S/Co Covariance: " + str(unigrams['Score'].cov(unigrams['Count'])))
print("[Bigrams] S/Co Covariance: " + str(bigrams['Score'].cov(bigrams['Count'])))

# Take the top 100 papers and analyse their subject area
unigrams = unigrams.head(100)
bigrams = bigrams.head(100)

# Group by subject area and get the total number of papers in each subject area
unigram_subjects_sum = unigrams.groupby(['Subject Area']).sum()
unigram_subjects_sum = unigram_subjects_sum.drop(['Citations', 'Score'], axis=1)
bigram_subjects_sum = bigrams.groupby(['Subject Area']).sum()
bigram_subjects_sum = bigram_subjects_sum.drop(['Citations', 'Score'], axis=1)

# Plot count results in a bar graph
unigram_subjects_sum.plot(kind='bar', title='A comparison of the sum of papers per subject area (Unigrams)')
bigram_subjects_sum.plot(kind='bar', title='A comparison of the sum of papers per subject area (Bigrams)')

# Group by subject area and get the mean score of each subject area
unigram_subjects_mean = unigrams.groupby(['Subject Area']).mean()
unigram_subjects_mean = unigram_subjects_mean.drop(['Citations', 'Count'], axis=1)
bigram_subjects_mean = bigrams.groupby(['Subject Area']).mean()
bigram_subjects_mean = bigram_subjects_mean.drop(['Citations', 'Count'], axis=1)

# Plot count results in a bar graph
unigram_subjects_mean.plot(kind='bar', title='A comparison of the mean score of papers per subject area (Unigrams)')
bigram_subjects_mean.plot(kind='bar', title='A comparison of the mean score of papers per subject area (Bigrams)')

# Show all plots
plt.show()