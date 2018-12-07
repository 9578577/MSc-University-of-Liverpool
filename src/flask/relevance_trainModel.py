import re
import pandas as pd
import numpy as np
from sklearn import svm
from stop_words import get_stop_words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
import random
# Define root
root_path = "./"

# Read tweet CSV
df = pd.read_csv(root_path + "tweets.csv", names=['ID', 'Tweet', 'Relevance'], index_col=0)
df = df.head(10)

print(df)

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
X = df['Tweet']
y = df['Relevance']

# Transform tweets into a numerical value using Count/TF
count_vect = CountVectorizer()
X = count_vect.fit_transform(X)
tfidf_transformer = TfidfTransformer()
X = tfidf_transformer.fit_transform(X)

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Train classifier
clf = svm.SVC(gamma='scale')
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
print(confidence)

pred = "I love Mr Gadaffi"
pred = count_vect.fit_transform(pred)
pred = tfidf_transformer.fit_transform(pred)
print(str(clf.predict(pred)))

for index, row in df.iterrows():
    print(row['Tweet'])