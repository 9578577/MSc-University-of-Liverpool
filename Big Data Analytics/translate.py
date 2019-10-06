# coding=utf-8
import os
import re
import emoji
import pandas as pd
from googletrans import Translator

# Set root path
root_path = "../../"

# Initiate the translator
translator = Translator()

# Read in the tweet CSV
tweets = pd.read_csv(root_path + "tweets.csv", engine="python", names=['ID', 'Tweet'], index_col=0)

# Function to remove emojis from tweet - https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
def clean_emojis(tweet):
    allchars = [str for str in tweet.decode('utf-8')]
    emojiList = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    cleanText = ' '.join([str for str in tweet.decode('utf-8').split() if not any(i in str for i in emojiList)])
    return cleanText

# Characters and symbols to remove from tweets
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbols = ['!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '/', '\\', '<', '>', '\'', '@', '~', '\#', '.', '¸', ',', '?', '|', '-', '_', ':', ';']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

for symbol in symbols:
    tweets['Tweet'] = tweets['Tweet'].str.replace(symbol, "")

for number in numbers:
    tweets['Tweet'] = tweets['Tweet'].str.replace(number, "")

tweets['Tweet'] = tweets['Tweet'].str.replace('\s\s+', ' ')
tweets['Tweet'] = tweets['Tweet'].str.replace('\t', ' ')

# Detect language, if English append to translatedTweets otherwise translate then append
translatedTweets = []
i = 0
for index, row in tweets.iterrows():
    # Remove emojis from tweet
    row['Tweet'] = clean_emojis(row['Tweet'].encode('utf8'))
    # Detect language
    if (translator.detect(row['Tweet']).lang) == "en":
        # Remove hyperlinks from English tweet, no need to do this for Arabic as we remove English letters/chars
        # https://stackoverflow.com/questions/24399820/expression-to-remove-url-links-from-twitter-tweet/24399874
        tweet = re.sub(r"http\S+", "", row['Tweet'])
        translatedTweets.append({'ID': i, 'Tweet': tweet})
        i += 1
    else:
        for letter in letters:
            row['Tweet'] = row['Tweet'].replace(letter, "")
        translatedTweet = translator.translate(row['Tweet'], dest="en")
        translatedTweets.append({'ID': i, 'Tweet': translatedTweet.text})
        i += 1
    
# Create a dataframe from translatedTweets
tweets = pd.DataFrame(translatedTweets)

# Remove symbols from tweets
symbols = ['!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '/', '\\', '<', '>', '\'', '@', '~', '\#', '.', '¸', ',', '?', '|', '-', '_', ':', ';']
for symbol in symbols:
    tweets['Tweet'] = tweets['Tweet'].str.replace(symbol, "")

# Remove numbers from tweets
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for number in numbers:
    tweets['Tweet'] = tweets['Tweet'].str.replace(number, "")

# Regex to ensure all chars are removed and remove multiple spaces 
tweets['Tweet'] = tweets['Tweet'].str.replace(' +', ' ')
tweets['Tweet'] = tweets['Tweet'].str.replace(r'[^A-Za-z0-9]+', '')

# Convert tweets to lower case
tweets['Tweet'] = tweets['Tweet'].str.lower()

# Set index and save to csv file
tweets.set_index('ID', inplace=True)
tweets.to_csv(root_path + "tweets_clean.csv", header="False")