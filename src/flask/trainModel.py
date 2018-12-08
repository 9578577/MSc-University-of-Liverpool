import re
import pandas as pd
import numpy as np
from joblib import dump
from sklearn.naive_bayes import MultinomialNB
from stop_words import get_stop_words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split

# Define root
root_path = "./outputs/"

# Read tweet CSV
df = pd.read_csv(root_path + "relevantTweets.csv", names=['Tweet', 'Candidate'])

# Compile emoji REGEX
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

# Clean data
df['Tweet'] = df['Tweet'].str.replace('/(^\w+:|^)\/\//', '') # Remove links
df['Tweet'] = df['Tweet'].str.replace('[^0-9A-Za-z ]+', '') # Remove special characters
df['Tweet'] = df['Tweet'].str.replace(emoji_pattern, '') # Remove emojis
df['Tweet'] = df['Tweet'].str.lower() # Convert to lower case

# Remove stopwords
stop_words = list(get_stop_words('en'))
nltk_stopwords = list(stopwords.words('english'))
stop_words.extend(nltk_stopwords)
df['Tweet'] = df['Tweet'].apply(lambda x: ' '.join([w for w in x.split() if w not in stop_words]))

# Define features and labels for model
X_train, X_test, y_train, y_test = train_test_split(df['Tweet'], df['Relevance'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Train classifier
clf = MultinomialNB().fit(X_train_tfidf, y_train)
print(clf.predict(count_vect.transform(["rt evanalomma gaddafi constructed largest irrigation system world providing million cubic meters fre"])))

# Save classifier
dump(clf, 'candidate_classifier.joblib') 
dump(count_vect, 'count_vectorizer.joblib')