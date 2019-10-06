import os
import re
import pandas as pd
import numpy as np
from pathlib import Path

# A function to create pivot tables from the Govt. Initiative mapreduce
def makePivotTable(file):
    print("Creating pivot table...")
    file = open('../data/output/mapreduce/' + file + '.txt', 'r', encoding='utf-8')
    df = []
    for line in file:
        word, count = line.strip().split('\t')
        doc = word.split('~')[0]
        word = word.split('~')[1]
        df.append({'Document': doc, 'Word' : word.strip(), 'Count' : count.strip()})
    df = pd.DataFrame(df)
    df = df.groupby(['Word', 'Document']).sum().reset_index()
    df = df.pivot(index='Word', columns='Document')
    df.fillna(0, inplace=True)
    return df

# Functions to calculate tf-idf for unigrams and bigrams
# Calculate term frequency
def calcTF(dataframe):
    print("Calculating term frequencies...")
    df = dataframe
    for col in df:
        df[col] = pd.to_numeric(df[col])
        col_sum = df[col].sum()
        df[col] = df[col] / col_sum
    return df

# Calculate inverse document frequency and TF-IDF
def calcTFIDF(dataframe):
    print("Calculating inverse term frequency and TF-IDF...")
    df = dataframe
    for index, row in df.iterrows():
        row_count = row.count() # Count the total number of columns in each row
        word_count = 0 # Count how many columns the word occurs in
        for col in row:
            if col > 0:
                word_count = word_count + 1
        idf = np.log(row_count / word_count)
        # Times the TF of each row by IDF
        df.loc[index, :] = row * idf
    return df

# Take the average of each rows TF-IDF values to compute a word score
def scoreWords(dataframe):
    print("Calculating word scores...")
    df = dataframe
    word_score = []
    for index, row in df.iterrows():
        row_sum = row.sum()
        row_count = row.count()
        score = row_sum / row_count
        word_score.append({'Word': index, 'Score' : score})
    word_score = pd.DataFrame(word_score)
    word_score.set_index('Word', inplace=True)
    return word_score

# Call functions to calculate tf-idf of bigrams and unigrams
unigram_df = makePivotTable('init_unigram')
unigram_df = calcTF(unigram_df)
unigram_df = calcTFIDF(unigram_df)
bigram_df = makePivotTable('init_bigram')
bigram_df = calcTF(bigram_df)
bigram_df = calcTFIDF(bigram_df)
unigram_score = scoreWords(unigram_df)
bigram_score = scoreWords(bigram_df)

# Save outputs
save_path = "../data/output/postprocessing/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
unigram_df.to_csv(save_path + "unigram_tfidf.csv")
bigram_df.to_csv(save_path + "bigram_tfidf.csv")

save_path = "../data/output/wordscores/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
unigram_score.to_csv(save_path + "unigram_score.csv", header="False")
bigram_score.to_csv(save_path + "bigram_score.csv", header="False")
