# Import packages
import os
import re
import pandas as pd
import random
from pathlib import Path
from stop_words import get_stop_words
from nltk.corpus import stopwords

# Import documents for preprocessing
init_file = open("../data/industrial-strategy-white-paper-web-ready-version.txt", encoding="utf-8").read()
abs_df = pd.read_csv("../data/markov-chain-monte-carlo.csv", engine="python", names=['Citations', 'DOI', 'Link', 'Abstract'])

print(abs_df.head())

## Splitting government initiative into chapters for TF-IDF analysis
init_file = re.sub(r'[^A-Za-z0-9]+', ' ', init_file)

# Define each "chapter" to split
chapters = [
    '240 Industrial Strategy White Paper',
    'References 1',
    '240 Britain and the world',
    'Places 214',
    'Business Environment 162',
    'Infrastructure 126',
    'People 92',
    'Ideas 56',
    'Grand Challenges 30',
    'Introduction 8',
    'Foreword from the Prime Minister'
]
init_dict = []
for chapter in chapters:
    # Remove all content before "Indusrtial Strategy White Paper"
    if chapter == "240 Industrial Strategy White Paper":
        init_file = init_file.split(chapter)[1]
    # Remove all content after "References"
    elif chapter == "References 1":
        init_file = init_file.split(chapter)[0]
    # Add each chapter to the dicationary x
    else:
        init_dict.append({'Chapter': chapter, 'Content': init_file.split(chapter)[1]})
        init_file = init_file.split(chapter)[0]

init_df = pd.DataFrame(init_dict)

# Define symbols to remove from text and set stop words
symbols = ['!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '/', '\\', '<', '>', '\'', '@', '~', '\#', '.', '¸', ',', '?', '|', '-', '_', ':', ';']
stop_words = list(get_stop_words('en'))
nltk_stopwords = list(stopwords.words('english'))
stop_words.extend(nltk_stopwords)

# Remove numbers from "Chapters" column
init_df['Chapter'] = init_df['Chapter'].str.replace(' \d+', '')
init_df['Chapter'] = init_df['Chapter'].str.replace('\d+ ', '')

# Clean text
for symbol in symbols:
    init_df['Content'] = init_df['Content'].str.replace(symbol, ' ')
init_df['Content'] = init_df['Content'].str.replace('\d+', ' ')
init_df['Content'] = init_df['Content'].str.lower()

# Remove stop words
init_df['Content'] = init_df['Content'].apply(lambda x: ' '.join([w for w in x.split() if w not in stop_words]))

## CLEANING ABSTRACT CSV
# Clean text
for symbol in symbols:
    abs_df['Abstract'] = abs_df['Abstract'].str.replace(symbol, ' ')
abs_df['Abstract'] = abs_df['Abstract'].str.replace('\d+', ' ')
abs_df['Abstract'] = abs_df['Abstract'].str.lower()

# Remove stop words from Abstract
abs_df['Abstract'] = abs_df['Abstract'].apply(lambda x: ' '.join([w for w in x.split() if w not in stop_words]))

# Remove spaces from DOI column
abs_df['DOI'] = abs_df['DOI'].str.replace(' ', '')

# Replace blank fields with a relevant value
abs_df['Citations'].fillna('0', inplace=True)
abs_df['Link'].fillna('NONE', inplace=True)
abs_df['DOI'].fillna('EMPTY', inplace=True)

# Replace the "EMPTY" values in the DOI column with a random number so we can identify them separately
abs_df['DOI'] = abs_df['DOI'].apply(lambda x: random.random() * 1000 if (x == 'EMPTY') else x)

# Merge the DOI, Link and Citation fields together so we only pass two columns to the mapreduce
abs_df['DOI'] = abs_df['DOI'].map(str) + ' ' + abs_df['Link'] + ' ' + abs_df['Citations']
abs_df = abs_df.drop(columns=['Link'], axis=1)
abs_df = abs_df.drop(columns=['Citations'], axis=1)

# Set indexes for exporting
init_df.set_index('Chapter', inplace=True)
abs_df.set_index('DOI', inplace=True)

print(abs_df.head())

# Save outputs
save_path = "../data/output/preprocessing/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
init_df.to_csv(save_path + "initiative_clean.csv")
abs_df.to_csv(save_path + "abstract_clean.csv")
