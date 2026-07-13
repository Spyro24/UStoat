import requests
import json
import baseModules
import socket

class userAccount:
    def __init__(self, logger=None):
        self.logger = logger
        self.platformName = "stoat"
        self.userID = ""
        self.token = ""
        self.mfaTicket = ""
        self.websocketPackage = []
        self.clientName = ""
        self.websocket = None
        self.readyPackage = {}
        self.badgeIndexURL = "https://raw.githubusercontent.com/Spyro24/UStoatBadgeSystem/refs/heads/main/stoat.json"
        self.badgeDataURL = "https://raw.githubusercontent.com/Spyro24/UStoatBadgeSystem/refs/heads/main/badges"
    
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
        if self.logger:
            self.logger.log("Stoat", "Trying to resume session...")
        self.token = token
        return self.startSession()
    
    def startSession(self):
        if self.logger:
            self.logger.log("Stoat", "Trying to start session...")
        try:
            userInfo = requests.get("https://stoat.chat/api/users/@me", headers={"X-Session-Token": self.token})
        except requests.exceptions.ConnectionError:
            if self.logger:
                self.logger.log("Stoat", "Connection Error")
            return 2
        if not userInfo.ok:
            if self.logger:
                self.logger.log("Stoat", "Invalid Token or user endpoint not reachable")
            return 1
        self.websocket = baseModules.WSSClient.WSSClient(f"wss://stoat.chat/events?version=1&format=json&token={self.token}")
        if self.websocket.wait_until_ready(timeout=30):
            if self.logger:
                self.logger.log("Stoat", "Websocket connection succesfull")
            userInfo = userInfo.json()
            self.userID = userInfo["_id"]
            wait = True
            while wait:
                if self.websocket.has_new_data():
                    for packet in self.websocket.get_messages():
                        packet = json.loads(packet)
                        if packet["type"] == "Ready":
                            if self.logger:
                                self.logger.log("Stoat", "Ready package received")
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
        answer = requests.get(self.badgeIndexURL)
        if answer.ok:
            return answer.json()
    
    def getBadge(self, rgistrarID: str, badgeID: str):
        answer = requests.get(f"{self.badgeDataURL}/{rgistrarID}/{badgeID}.png")
        if answer.ok:
            return answer.json()
    
    def deleteMessage(self, messageID):
        pass
    
    def editMessage(self, channel: str, messageID: str, editedMessage: str):
        requests.patch(f"https://stoat.chat/api/channels/{channel}/messages/{messageID}", headers={"X-Session-Token": self.token}, json={"content": editedMessage})