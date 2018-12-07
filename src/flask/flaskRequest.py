import sys
import requests
import json

# Pull tweet from java request
tweet = sys.argv[1]

# Add tweet to parameters
content = {"tweet":tweet}

# Send request to flask server (ETHERNET - 192.168.56.1 WIRELESS - 10.24.182.251)
request = requests.get("http://192.168.56.1:5050/api", params=content)

# Receive output from server
print(request.text)