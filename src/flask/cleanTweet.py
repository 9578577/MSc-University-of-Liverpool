# coding=utf-8
import os
import re
import csv
import pandas as pd
from googletrans import Translator
from time import sleep

# Set root path
root_path = "../../"

# Import CSV
df = pd.read_csv(root_path + "tweets.csv", names=['ID', 'Tweet'], index_col=0)

# Compile emoji REGEX
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

# Initialise the Translator
translator = Translator()

# Loop through dataframe
i = 0
for index, row in df.iterrows():
    try:
        tweet = re.sub('[^0-9A-Za-z\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', row['Tweet']) # Remove special characters from tweet
        tweet = emoji_pattern.sub(r'', tweet) # Remove emojis from tweet
        print("["+str(i)+"] Tweet: " + tweet)
        lang = translator.detect(tweet).lang # Determine the language of the tweet
        if(lang == "ar"): # If the language is Arabic, remove English characters and translate
            tweet = re.sub('[^\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', tweet)
            tweet = translator.translate(tweet, dest="en").text
            print("[Arabic] " + tweet)
        elif(lang == "en"): # If the language is English, save in output file
            tweet = re.sub('[^A-Za-z]+', ' ', tweet)
            print("[English] " + tweet)
        else:
            print("[ERROR] Unable to detect language")
        # Convert capitals to lower and save tweet to a CSV file ready to train the relevance model
        tweet = tweet.lower()
        fields=[i, tweet]
        with open(r'./outputs/cleanTweets.csv', 'a', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        i+=1
        print("Sleeping for 10 seconds")
        sleep(10) # Sleep after every translation so we don't overload the API and get blocked
    except JSONDecodeError as e: # Catch JSON errors
        print("[ERROR] " + str(e))
        print("Sleeping for 10 seconds")
        sleep(10)
    except Exception as e: # Catch Exception errors
        print("[ERROR] " + str(e))
        print("Sleeping for 10 seconds")
        sleep(10)
    except: # Catch all other errors
        print("[ERROR] Error uncaught exception")
        print("Sleeping for 10 seconds")
        sleep(10)
        continue
