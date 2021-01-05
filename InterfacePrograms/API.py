# Requests allows a python program to esseentially type in URL requests
import requests
import json
from testData import InterfaceTestData


# The base URL to access the server
BASE = "http://192.168.1.73:5000/"

# User name
username = "Emily"

response = requests.post(BASE + "postInterfaceData/username", json=InterfaceTestData.arrangementA, headers={'Content-Type': 'application/json'})
print(response.text)
