import requests

class userAccount:
    def __init__(self):
        self.platformName = "nerimity"
        self.token = ""
    
    def login(self, username: str, password: str, clientName: str):
        answer = requests.post("https://nerimity.com/api/users/login", json={"email":username ,"password": password})
        if answer.ok:
            answerJson = answer.json()
            self.token = answerJson["token"]
            return 0
        return 1
    
    def loginMFA(self, mfaCode: str):
        pass
    
    def resumeSession(self, token: str):
        pass