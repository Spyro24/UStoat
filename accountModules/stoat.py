import requests
import json
import baseModules

class userAccount:
    def __init__(self):
        self.platformName = "stoat"
        self.userID = ""
        self.token = ""
        self.mfaTicket = ""
        self.websocketPackage = []
        self.clientName = ""
        self.websocket = None
        self.readyPackage = {}
    
    def login(self, username: str, password: str, clientName: str):
        self.clientName = clientName
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"email": username, "password": password, "friendly_name": clientName})
        if answer.ok:
            answerJson = answer.json()
            if answerJson["result"] == "MFA":
                self.mfaTicket = answerJson["ticket"]
                return 2
            elif answerJson["result"] == "Success":
                self.token = answerJson["token"]
                self.userID = answerJson["user_id"]
                return 0
        return 1
    
    def loginMFA(self, mfaCode: str):
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"mfa_response":{"totp_code":mfaCode},"mfa_ticket": self.mfaTicket,"friendly_name": self.clientName})
        if answer.ok:
            answerJson = answer.json()
            self.userID = answerJson["user_id"]
            self.token = answerJson["token"]
            return 0
        return 1
    
    def resumeSession(self, token: str):
        self.token = token
        return self.startSession()
    
    def startSession(self):
        self.websocket = baseModules.WSSClient.WSSClient(f"wss://stoat.chat/events?version=1&format=json&token={self.token}")
        if self.websocket.wait_until_ready(timeout=30):
            userInfo = requests.get("https://stoat.chat/api/users/@me", headers={"X-Session-Token": self.token})
            if not userInfo.ok:
                return 1
            userInfo = userInfo.json()
            self.userID = userInfo["_id"]
            wait = True
            while wait:
                if self.websocket.has_new_data():
                    for packet in self.websocket.get_messages():
                        packet = json.loads(packet)
                        if packet["type"] == "Ready":
                            self.readyPackage = packet
                            wait = False
                            break
            return 0
        return 1
    
    def getReadyPackage(self):
        return self.readyPackage
    
    def pumpSocket(self):
        pass
    
    def returnSocketData(self):
        data = []
        if self.websocket.has_new_data():
            for packet in self.websocket.get_messages():
                data.append(json.loads(packet))
        return data
    
    def sendAtachments(self, filePaths: list):
        pass
    
    def sendMessage(self, message: str, channel: str, server: str, masqData: dict):
        requests.post(f"https://stoat.chat/api/channels/{channel}/messages", headers={"X-Session-Token": self.token}, json={"content": message})
    
    def setupForUsing(self):
        pass
    
    def fetchServerIcon(self, iconID: str):
        return requests.get(f"https://cdn.stoatusercontent.com/icons/{iconID}")
    
    def fetchMessages(self, channel: str, server: str, count=50):
        try:
            messages = requests.get(f"https://stoat.chat/api/channels/{channel}/messages", headers={"X-Session-Token": self.token})
            if not messages.ok: raise BaseException
            messages = messages.json()
            if type(messages) == list:
                return {"messages": messages,"users":[],"members":[]}
            else:
                return messages
        except:
            return {"messages":[],"users":[],"members":[]}
    
    def fetchUserPicture(self, userPictureID: str):
        return requests.get(f"https://cdn.stoatusercontent.com/avatars/{userPictureID}", headers={"X-Session-Token": self.token})
    
    def fetchUser(self, userID: str):
        return requests.get(f"https://stoat.chat/api/users/{userID}", headers={"X-Session-Token": self.token}).json()
    
    def fetchChannelMembers(self, server: str, channel: str):
        return requests.get(f"https://stoat.chat/api/channels/{channel}/members", headers={"X-Session-Token": self.token}).json()
    
    def fetchServerMembers(self, server: str, channel: str):
        return requests.get(f"https://stoat.chat/api/servers/{server}/members?exclude_offline=true", headers={"X-Session-Token": self.token, "content-type": "application/json"}).json()
    
    def returnSaveInfo(self):
        return {"token": self.token, "service": self.platformName}
    
    def getBadgeData(self):
        answer = requests.get("https://raw.githubusercontent.com/Spyro24/UStoatBadgeSystem/refs/heads/main/stoat.json")
        if answer.ok:
            return answer.json()