import re
import csv
import numpy as np
from joblib import load
from flask import Flask, request, jsonify
from googletrans import Translator
from stop_words import get_stop_words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])

def twitter_analysis():
   # Pull tweet from the post request
   tweet = request.args.get('tweet')

   # Clean the incoming tweet before language detection
   tweet = re.sub('[^0-9A-Za-z\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', tweet)

   # Initialise the translator
   translator = Translator()

   # Load classifiers
   relevance_clf = load('./classifiers/relevance_classifier.joblib') 
   candidate_clf = None
   count_vect = load('./classifiers/count_vectorizer.joblib')
   
   # Detect language of tweet
   lang = translator.detect(tweet).lang

   if(lang=="en"):
      originalTweet = None
      tweet = re.sub('[^A-Za-z]+', ' ', tweet)
      classifiedTweet = tweet.lower()
   elif(lang=="ar"):
      originalTweet = tweet
      tweet = re.sub('[^\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', tweet)
      classifiedTweet = translator.translate(tweet, dest="en").text
      classifiedTweet = classifiedTweet.lower()
   else:
      print("[ERROR] Unable to detect language of tweet")
      originalTweet = None
      classifiedTweet = None
      lang = None


   # Remove stopwords from tweet
   stop_words = list(get_stop_words('en'))
   nltk_stopwords = list(stopwords.words('english'))
   stop_words.extend(nltk_stopwords)
   words = classifiedTweet.split(' ')
   classifiedTweet = [w for w in words if not w in stop_words]
   classifiedTweet = " ".join(classifiedTweet)

   # Classify tweet to determine relevance
   relevance = relevance_clf.predict(count_vect.transform([classifiedTweet]))
   relevance = np.asscalar(relevance[0])

   if(relevance == 1):
      # Determine if the tweet is a retweet
      if("rt" in originalTweet or "RT" in originalTweet or "rt" in classifiedTweet or "RT" in originalTweet):
         retweet = 1
      else:
         retweet = 0

      # Classify tweet to determine candidate
      # 0 - Gadaffi, 1 - Haftar       DETERMINE IF TWEET CONTAINS BOTH CANDIDATES NAMES, IF IT DOESNT DONT CALC SENTIMENT/CANDIDATE
      candidate = 0

      # Determine sentiment of the tweet - uses text-processing.com API
      sentiment = 0

      # Create array to output back to Storm server
      output = {
         'OriginalTweet': originalTweet,
         'ClassifiedTweet': classifiedTweet,
         'Language': lang,
         'Retweet': retweet,
         'Relevance': relevance, 
         'Candidate': candidate, 
         'Sentiment': sentiment
         }
      print(output)

      # Append results to CSV file
      fields=[originalTweet, classifiedTweet, lang, retweet, relevance, candidate, sentiment]
      with open(r'./outputs/classifiedTweets.csv', 'a', newline='\n', encoding='utf-8') as f:
         writer = csv.writer(f)
         writer.writerow(fields)

      return jsonify(results=output)
   else:
      output = {
         'Relevance': relevance,
         'Tweet': classifiedTweet
      }
      return jsonify(results=output)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050, debug=True)