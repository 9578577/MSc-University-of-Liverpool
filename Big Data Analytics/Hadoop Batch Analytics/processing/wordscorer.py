import os
import re
import pandas as pd
import numpy as np
from pathlib import Path

# Load the unigram and bigram score CSV files
def loadScore(dir, csv):
    print("Loading CSV file...")
    df = pd.read_csv(dir + csv + ".csv", names=['Word', 'Score'], index_col=0)
    return df

def readTokens(file):
    print("Creating dataframe of documents and tokens...")
    file = open('../data/output/mapreduce/' + file + '.txt', 'r', encoding='utf-8')
    df = []
    for line in file:
        word, count = line.split('\t')
        doc = word.split('~')[0]
        word = word.split('~')[1]
        DOI = doc.split(' ')[0]
        link = doc.split(' ')[1]
        citations = doc.split(' ')[2]
        df.append({'Document': DOI, 'Link': link, 'Word': word.strip(), 'Count': count.strip(), 'Citations': citations})
    df = pd.DataFrame(df)
    df = df.set_index('Document')
    df['Score'] = 0
    return df

def scoreWords(ngrams, scores):
    scored_words = []
    for index, rows in ngrams.iterrows():
        word = rows['Word']
        count = rows['Count']
        link = rows['Link']
        citations = rows['Citations']
        if word in scores.index:
            tfidf = scores.loc[word, 'Score']
            score = float(tfidf) * float(count)
            scored_words.append({'Document': index, 'Link': link, 'Score': score, 'Citations': citations})
        else:
            scored_words.append({'Document': index, 'Link': link, 'Score': 0, 'Citations': citations})
    scored_words = pd.DataFrame(scored_words)
    scored_words = scored_words.groupby(['Document', 'Citations', 'Link']).sum()
    return scored_words

# Score unigrams
unigram_scores = loadScore("../data/output/wordscores/", "unigram_score")
unigram_df = readTokens("abstract_unigram")
unigram_df = scoreWords(unigram_df, unigram_scores)

# Score bigrams
bigram_scores = loadScore("../data/output/wordscores/", "bigram_score")
bigram_df = readTokens("abstract_bigram")
bigram_df = scoreWords(bigram_df, bigram_scores)

# Sort dataframe by score in descending order
unigram_df = bigram_df.sort_values(by=['Score'], ascending=False)
bigram_df = bigram_df.sort_values(by=['Score'], ascending=False)

# Save outputs
save_path = "../data/output/abstractscores/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
unigram_df.to_csv(save_path + "unigrams.csv")
bigram_df.to_csv(save_path + "bigrams.csv")
