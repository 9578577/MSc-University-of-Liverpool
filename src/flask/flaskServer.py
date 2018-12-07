from flask import Flask, request, jsonify
from googletrans import Translator
import csv
import re

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])

def twitter_analysis():
   # Pull tweet from the post request
   tweet = request.args.get('tweet')

   # Clean the incoming tweet before language detection
   tweet = re.sub('[^0-9A-Za-z\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc ]+', ' ', tweet)

   # Initialise the translator
   translator = Translator()
   
   # Detect language of tweet
   lang = translator.detect(tweet).lang

   if(lang == "en"):
      originalTweet = tweet
      translatedTweet = None
   elif(lang == "ar"):
      originalTweet = tweet
      translatedTweet = translator.translate(tweet, dest="en").text
   else:
      print("[ERROR] Unable to detect language of tweet")

   # Classify tweet to determine relevance
   relevance = 0

   # Classify tweet to determine candidate
   # 0 - Gadaffi, 2 - Haftar
   candidate = 0

   # Determine sentiment of the tweet
   sentiment = 0

   output = {
      'OriginalTweet': originalTweet,
      'TranslatedTweet': translatedTweet,
      'Language': lang, 
      'Relevance': 0, 
      'Candidate': candidate, 
      'Sentiment': sentiment
      }
   print(output)

   # Append results to CSV file
   fields=[tweet, lang, relevance, candidate, sentiment]
   with open(r'classifiedTweets.csv', 'a', newline='\n', encoding='utf-8') as f:
      writer = csv.writer(f)
      writer.writerow(fields)

   return jsonify(results=output)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050, debug=True)