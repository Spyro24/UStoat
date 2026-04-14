import requests
import baseModules
import json

class userAccount:
    def __init__(self):
        self.platformName = "nerimity"
        self.token = ""
        self.websocket = None
        self.socketID = ""
    
    def login(self, username: str, password: str, clientName: str):
        answer = requests.post("https://nerimity.com/api/users/login", json={"email":username ,"password": password})
        if answer.ok:
            answerJson = answer.json()
            self.token = answerJson["token"]
            return 0
        return 1
    
    def loginMFA(self, mfaCode: str):
        pass
    
    def startSession(self):
        self.websocket = baseModules.WSSClient.WSSClient("wss://nerimity.com/socket.io/?EIO=4&transport=websocket")
        if self.websocket.wait_until_ready():
            self.websocket.send_data("40")
            wait = True
            while wait:
                if self.websocket.has_new_data():
                    for data in self.websocket.get_messages():
                        print(data)
                        sid = json.loads(data[1:])
                        self.socketID = sid["sid"]
                        wait = False
                        break
            self.websocket.send_data('42["user:authenticate",{"token":"' + self.token + '"}]')
            wait = True
            while wait:
                print(self.websocket.get_messages())
            while wait:
                data = list(self.websocket.get_messages())
                for test in data:
                    test2 = json.loads(test[2:])
                    if test != None and test2.__contains__('user:authenticated'):
                        print(test2)
                        wait = False
                        break
            return 0
        return 1
    
    def resumeSession(self, token: str):
        pass

test = userAccount()
test.startSession()