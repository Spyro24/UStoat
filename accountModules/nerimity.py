import requests
import baseModules
import json
import time

class userAccount:
    def __init__(self):
        self.platformName = "nerimity"
        self.token = ""
        self.websocket = None
        self.socketID = ""
        self.userID = ""
        self.readyPackage = {"type":"Ready",
                             "users":[],
                             "servers":[],
                             "channels": []}
        self.websocketPackage = []
    
    def login(self, username: str, password: str, clientName: str):
        answer = requests.post("https://nerimity.com/api/users/login", headers={"User-Agent": "UStoat"}, json={"email":username ,"password": password})
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
            print("Websocket is ready")
            self.websocket.send_data("40")
            wait = True
            while wait:
                if self.websocket.has_new_data():
                    for data in self.websocket.get_messages():
                        sid = json.loads(data[1:])
                        self.socketID = sid["sid"]
                        print("SID received")
                        wait = False
                        break
            time.sleep(0.2)
            self.websocket.send_data('42["user:authenticate",{"token":"' + self.token + '"}]')
            time.sleep(0.2)
            wait = True
            while wait:
                data = list(self.websocket.get_messages())
                if data != []:
                    print(str(data))
                for test in data:
                    test2 = json.loads(test[2:])
                    if test != None and test2.__contains__('user:authenticated'):
                        print("user authenticated")
                        packet = test2[1]
                        user = {}
                        self.userID = packet["user"]["id"]
                        user["_id"] = packet["user"]["id"]
                        user["username"] = packet["user"]["username"]
                        user["discriminator"] = packet["user"]["tag"]
                        if packet["user"]["avatar"] != None:
                            user["avatar"] = {}
                            user["avatar"]["_id"] = packet["user"]["avatar"]
                        self.readyPackage['users'].append(user)
                        for rawServer in packet["servers"]:
                            server = {}
                            server["_id"] = rawServer["id"]
                            server["name"] = rawServer["name"]
                            server["owner"] = "0"
                            server["channels"] = []
                            server["icon"] = {}
                            server["icon"]["_id"] = rawServer["avatar"]
                            self.readyPackage['servers'].append(server)
                        serverPos = []
                        for server in self.readyPackage["servers"]:
                            serverPos.append(server["_id"])
                        for rawChannel in packet["channels"]:
                            channel = {}
                            channel["channel_type"] = "TextChannel"
                            channel["_id"] = rawChannel["id"]
                            channel["name"] = rawChannel["name"]
                            if rawChannel["type"] == 1:
                                channel["server"] = rawChannel["serverId"]
                                self.readyPackage["servers"][serverPos.index(channel["server"])]["channels"].append(channel["_id"])
                            else:
                                channel["channel_type"] = "DirectMessage"
                                channel["recipients"] = []
                            self.readyPackage["channels"].append(channel)
                        wait = False
                        break
                    elif test != None:
                        print(test)
                time.sleep(0.2)
            print("login to websocket succesfull")
            return 0
        return 1
    
    def resumeSession(self, token: str):
        self.token = token
        return self.startSession()
    
    def logout(self):
        answer = requests.delete("https://nerimity.com/api/users/logout", headers={"Authorization": self.token})
        if answer.ok:
            return 0
        return 1
    
    def getReadyPackage(self):
        return self.readyPackage
    
    def pumpSocket(self):
        if self.websocket.has_new_data():
            for package in self.websocket.get_messages():
                if package == "2":
                    self.websocket.send_data("3")
                else:
                    packetFormated = {"type": ""}
                    data: list = json.loads(package[2:])
                    if data.__contains__("message:created"):
                        data = data[1]["message"]
                        packetFormated["type"] = "Message"
                        packetFormated["_id"] = data["id"]
                        packetFormated["channel"] = data["channelId"]
                        packetFormated["author"] = data["createdById"]
                        packetFormated["content"] = data["content"]
                    if packetFormated["type"] != "":
                        self.websocketPackage.append(packetFormated)
    
    def returnSocketData(self):
        socketData = self.websocketPackage
        self.websocketPackage = []
        return socketData
    
    def fetchUser(self, userID: str):
        answer = requests.get(f"https://nerimity.com/api/users/{userID}", headers={"Authorization": self.token})
        if answer.ok:
            userData = answer.json()["user"]
            user = {}
            user["_id"] = userData["id"]
            user["discriminator"] = userData["tag"]
            user["username"] = userData["username"]
            if userData["avatar"] != None:
                user["avatar"] = {}
                user["avatar"]["_id"] = userData["avatar"]
            return user
    
    def fetchServerIcon(self, iconID: str):
        return requests.get(f"https://cdn.nerimity.com/{iconID}")
    
    def fetchUserPicture(self, userID: str):
        return requests.get(f"https://cdn.nerimity.com/{userID}")
    
    def fetchMessages(self, channel: str, server: str, count=50):
        answer = requests.get(f"https://nerimity.com/api/channels/{channel}/messages?limit={count}", headers={"Authorization": self.token})
        messages = {"messages":[],"users":[],"members":[]}
        if answer.ok:
            json = answer.json()
            for rawMessage in json:
                message = {"_id": rawMessage["id"],
                           "channel": rawMessage["channelId"],
                           "author": rawMessage["createdById"],
                           "content": rawMessage["content"]}
                messages["messages"].append(message)
            messages["messages"].reverse()
        return messages
    
    def sendMessage(self, message: str, channel: str, server: str, masqData: dict):
        answer = requests.post(f"https://nerimity.com/api/channels/{channel}/messages", headers={"Authorization": self.token}, data={})
    
    def returnSaveInfo(self):
        return {"token": self.token, "service": self.platformName}
