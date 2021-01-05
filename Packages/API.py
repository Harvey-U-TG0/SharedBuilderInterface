class InterfaceAPI:
    # Requests allows a python program to esseentially type in URL requests
    import requests
    import json

    def __init__(self, serverURL = 'http://192.168.1.73:5000/', username = 'Emily'): 
        self.serverURL = serverURL 
        self.username = username

    # Input a brick arrangmenet and send to the server
    def postData(self, brickArrangement):    
        response = self.requests.post(self.serverURL + 'postInterfaceData/' + self.username, json=brickArrangement, headers={'Content-Type': 'application/json'})
        print(response.text)
