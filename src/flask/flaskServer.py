import re
import csv
import requests
import json
import numpy as np
from joblib import load
from flask import Flask, request, jsonify
from googletrans import Translator
from stop_words import get_stop_words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
@app.route('/api', methods=['GET', 'POST'])

# An error code of 1 will be returned if either:
# - The language cannot be detected
# - The tweet is irrelevant to the analysis
# - The tweet contains both candidates both candidates names
def twitter_analysis():
   # Pull tweet from the post request
   tweet = request.args.get('tweet')

   # Clean the incoming tweet before language detection
   tweet = re.sub('[^0-9A-Za-z\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', tweet)

   # Initialise the translator
   translator = Translator()

   # Load classifiers
   relevance_clf = load('./classifiers/relevance_classifier.joblib') 
   relevance_count_vect = load('./classifiers/relevance_count_vectorizer.joblib')
   candidate_clf = load('./classifiers/candidate_classifier.joblib') 
   candidate_count_vect = load('./classifiers/candidate_count_vectorizer.joblib')
   
   # Detect language of tweet
   lang = translator.detect(tweet).lang

   if(lang=="en" or lang=="ar"):
      if(lang=="en"):
         originalTweet = "None"
         tweet = re.sub('[^A-Za-z]+', ' ', tweet)
         classifiedTweet = tweet.lower()
      elif(lang=="ar"):
         originalTweet = tweet
         tweet = re.sub('[^\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', tweet)
         classifiedTweet = translator.translate(tweet, dest="en").text
         classifiedTweet = classifiedTweet.lower()
      # Remove stopwords from tweet
      stop_words = list(get_stop_words('en'))
      nltk_stopwords = list(stopwords.words('english'))
      stop_words.extend(nltk_stopwords)
      words = classifiedTweet.split(' ')
      classifiedTweet = [w for w in words if not w in stop_words]
      classifiedTweet = " ".join(classifiedTweet)

      # Classify tweet to determine relevance
      relevance = relevance_clf.predict(relevance_count_vect.transform([classifiedTweet]))
      relevance = np.asscalar(relevance[0])

      if(relevance == 1):
         # Determine if the tweet is a retweet
         if("rt" in originalTweet or "RT" in originalTweet or "rt" in classifiedTweet or "RT" in originalTweet):
            retweet = 1
         else:
            retweet = 0

         # Check if the tweet contains both Gaddafis and Haftars names
         # If it does, we will not calculate sentiment
         # This list could be made a lot more extensive to improve accuracy
         if("gaddafi" in tweet and "haftar" in tweet):
            err = "Tweet contains both candidates names"
            # Append results to CSV file
            fields=[err, classifiedTweet]
            with open(r'./errors.csv', 'a', newline='\n', encoding='utf-8') as f:
               writer = csv.writer(f)
               writer.writerow(fields)
            output = {
               'Error': 1,
               'errMessage': err
            }
            return jsonify(results=output)
         else:
            # Classify tweet to determine candidate
            # 0 - Gadaffi, 1 - Haftar
            candidate = candidate_clf.predict(candidate_count_vect.transform([classifiedTweet]))
            candidate = np.asscalar(candidate[0])

            # Determine sentiment of the tweet - uses text-processing.com API
            payload = {"text": classifiedTweet} # Payload to send to API
            try:
               req = requests.post("http://text-processing.com/api/sentiment/", data=payload)
            except requests.exceptions.RequestException as e:
               print("[EXCEPTION] " + e)

            # Check that the response code is valid
            if(req.status_code == 200):
                # Pull the reponse from the request
               resp = req.json()

               # Assign a numerical value to sentiment
               if(resp['label'] == "pos"):
                  sentiment = 1
               elif(resp['label'] == "neutral"):
                  sentiment = 0
               elif(resp['label'] == "neg"):
                  sentiment = -1

               # Append results to CSV file
               fields=[originalTweet, classifiedTweet, lang, retweet, relevance, candidate, sentiment]
               with open(r'./outputs/classifiedTweets.csv', 'a', newline='\n', encoding='utf-8') as f:
                  writer = csv.writer(f)
                  writer.writerow(fields)

               # Create array to output back to Storm server
               output = {
                  'ClassifiedTweet': classifiedTweet,
                  'Language': lang,
                  'Retweet': retweet,
                  'Relevance': relevance, 
                  'Candidate': candidate, 
                  'Sentiment': sentiment,
                  'Error': 0
                  }
               return jsonify(results=output)
            else:
               err = "Error code " + str(request.status_code)
               # Append results to CSV file
               fields=[err, classifiedTweet]
               with open(r'./errors.csv', 'a', newline='\n', encoding='utf-8') as f:
                  writer = csv.writer(f)
                  writer.writerow(fields)
               output = {
                  'Error': 1,
                  'errMessage': err
               }
               return jsonify(results=output)
      else:
         err = "Tweet is irrelevant"
         # Append results to CSV file
         fields=[err, classifiedTweet]
         with open(r'./errors.csv', 'a', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
         output = {
            'Error': 1,
            'errMessage': err
         }
         return jsonify(results=output)
   else:
      err = "Unable to detect language of tweet"
      # Append results to CSV file
      fields=[err, originalTweet]
      with open(r'./errors.csv', 'a', newline='\n', encoding='utf-8') as f:
         writer = csv.writer(f)
         writer.writerow(fields)
      output = {
         'Error': 1,
         'errMessage': err
      }
      return jsonify(results=output)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050, debug=True)