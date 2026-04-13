import requests

class userAccount:
    def __init__(self):
        self.platformName = "stoat"
        self.userID = ""
        self.token = ""
        self.mfaTicket = ""
    
    def login(self, username: str, password: str, clientName: str):
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"email": username, "password": password, "friendly_name": clientName})
        if answer.ok:
            answerJson = answer.json()
            if answerJson["result"] == "MFA":
                self.mfaTicket = answerJson["ticket"]
                return 2
            elif answer["result"] == "Success":
                self.token = answer["token"]
                self.userID = answer["user_id"]
                return 0
        return 1
    
    def loginMFA(self, mfaCode: str):
        pass
    
    def resumeSession(self, token: str):
        pass
    
    def sendAtachments(self, filePaths: list):
        pass
    
    def sendMessage(self, message: str, channel: str, server: str, masqData: str):
        pass
    
    def setupForUsing(self):
        pass