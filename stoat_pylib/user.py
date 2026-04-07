import requests
import websocket
import threading

class WSSClient:
    def __init__(self, url):
        self.url = url
        self.messages = []
        self.lock = threading.Lock()
        self.thread = None
        self.start()
    
    def start(self):
        def worker():
            def on_message(ws, msg):
                with self.lock:
                    self.messages.append(msg)
            
            ws = websocket.WebSocketApp(self.url, on_message=on_message)
            ws.run_forever()
        
        self.thread = threading.Thread(target=worker, daemon=True)
        self.thread.start()
    
    def get_messages(self):
        with self.lock:
            msgs = self.messages.copy()
            self.messages.clear()
            return msgs
    
    def has_new_data(self):
        with self.lock:
            return len(self.messages) > 0


class Account:
    def __init__(self):
        self.curentLoginStatus: str = "login"
        self.userName: str = ""
        self.clientName: str = "stoat_pylib"
        self.sessionToken = ""
        self.mfa_ticket = ""
        self._id = ""
        self.user_id = ""
        self.apiSuscription = None
        self.socketHandler = None
        
    def login(self, email: str, password: str):
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"email":f"{email}","password":f"{password}","friendly_name": f"{self.clientName}"}).json()
        self.curentLoginStatus = answer["result"]
        if self.curentLoginStatus == "MFA":
            self.mfa_ticket = answer["ticket"]
    
    def authMFA(self, code: str):
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"mfa_response":{"totp_code":f"{code}"},"mfa_ticket": self.mfa_ticket,"friendly_name": self.clientName}).json()
        print(answer)
        self._id = answer["_id"]
        self.user_id = answer["user_id"]
        self.sessionToken = answer["token"]
        
    def subToAPI(self):
        self.apiSuscription = WSSClient(f"wss://stoat.chat/events?version=1&format=json&token={self.sessionToken}")
        
    def sendMessage(self, msg: str, channel: str):
        answer = requests.post(f"https://stoat.chat/api/channels/{channel}/messages?", headers={"X-Session-Token": self.sessionToken}, json={"content": msg})
    
    def saveAccount(self) -> dict:
        return {"_id": self._id, "userId": self.user_id, "session": self.sessionToken}
    
    def loadAccount(self, data: dict):
        try:
            self._id = data["_id"]
            self.user_id = data["userId"]
            self.sessionToken = data["session"]
            self.curentLoginStatus = "sucess"
            return False
        except:
            return True

class users:
    def __init__(self):
        self.userInfo = {}
        self.userToken = ""
    
    def getUser(self, userId: str):
        try:
            return self.userInfo[userId]
        except KeyError:
            answer = requests.get(f"https://stoat.chat/api/users/{userId}", headers={"X-Session-Token": self.userToken}).json()
            self.addUser(answer)
        return self.userInfo[userId]
    
    def addUser(self, json):
        userid = json["_id"]
        self.userInfo[userid] = {}
        self.userInfo[userid]["name"] = json["username"]
        try:
            self.userInfo[userid]["display_name"] = json["display_name"]
        except KeyError:
            self.userInfo[userid]["display_name"] = json["username"]
        self.userInfo[userid]["discriminator"] = json["discriminator"]
        try:
            self.userInfo[userid]["avatarId"] = json["avatar"]["_id"]
        except KeyError:
            self.userInfo[userid]["avatarId"] = ""

class user:
    def __init__(self, app):
        self.app = app
        self.inbox = []
        self.token = ""
        self.me = {}
        self.users = {}
    
    def makeReady(self):
        userInfo = requests.get(f"https://stoat.chat/api/users/@me", headers={"X-Session-Token": self.token})
        if userInfo.ok:
            userInfo = userInfo.json()
            self.me["id"] = userInfo["_id"]
            self.me["name"] = userInfo["username"]
            self.me["display_name"] = userInfo["displa_name"]
            self.me["discriminator"] = userInfo["discriminator"]
    
    def getInbox(self):
        inbox = requests.get(f"https://stoat.chat/api/users/@me/notifications", headers={"X-Session-Token": self.token})
        if inbox.ok:
            self.inbox = inbox.json()
    
    def sendMessage(self, message: str, channel: str, masqData={}, mentions=[], reply=[], atachments=[]):
        send = {"content": ""}
        if message != "":
            send["content"] = message
        if len(atachments) > 0:
            atachmentIDs = []
            for file in atachments:
                path = file.strip().split("/")
                with open(file, "rb") as f:
                    resp = requests.post("https://cdn.stoatusercontent.com/attachments", files={"file": (path[-1], f, "image/png")}, headers={"x-session-token": self.token})
                    if resp.ok:
                        atachmentIDs.append(resp.json()["id"])
        if len(reply) > 0:
            pass
        if masqData != {}:
            pass
        answer = requests.post(f"https://stoat.chat/api/channels/{channel}/messages?", headers={"X-Session-Token": self.token}, json=send)