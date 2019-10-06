import sys
import requests
import json

# Pull tweet from java request
tweet = sys.argv[1]

# Send request to flask server (ETHERNET - 192.168.56.1 WIRELESS - 10.24.182.251)
payload = json.dumps({"tweet": tweet})
request = requests.post("http://192.168.56.1:5050/api", data=payload)

# Receive output from server
if(request.status_code == 200):
    response = request.text
    print(response)
else:
    print("[ERROR] Invalid response code")