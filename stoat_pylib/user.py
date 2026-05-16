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

class users:
    def __init__(self):
        self.userInfo = {}
        self.userToken = ""
        self.platformHelper = None
    
    def getUser(self, userId: str):
        try:
            return self.userInfo[userId]
        except KeyError:
            answer = self.platformHelper.fetchUser(userId)
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