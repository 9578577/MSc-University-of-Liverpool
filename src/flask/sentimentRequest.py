import requests
import json

tweet = "I hate everything about you, and your point of view and your stupid selfish attitude"

# Payload to send to the sentiment API
payload = {"text": tweet}

# Send request to API
try:
    request = requests.post("http://text-processing.com/api/sentiment/", data=payload)
except requests.exceptions.RequestException as e:
    print("[EXCEPTION] " + e)

# Check that the response code is valid
if(request.status_code == 200):
    # Pull the reponse from the request
    response = request.json()
    # Assign a numerical value to sentiment
    if(response['label'] == "pos"):
        sentiment = 1
    elif(response['label'] == "neutral"):
        sentiment = 0
    elif(response['label'] == "neg"):
        sentiment = -1
    print(sentiment)
else:
    print(request.status_code)