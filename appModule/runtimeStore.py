class runtimeStore:
    def __init__(self):
        self.userID = None #We need it only for user ID stuff like resolving the names of DM channels
        self.messages = {}
        self.channels = {}
        self.users = {}
        self.servers = {"0":{"name": "Direct Messages", "owner": None, "channels": []}}
    
    def insertMessage(self, messageId: str, content: str, author: str, deleted=False, edited=False):
        self.messages[messageId] = {"content": content, "author": author, "deleted": deleted, "edited": edited}
    
    def parseStoatMessage(self, package): #I dont want to add hundreds of lines to the main app
        message = {}
        message["author"] = package["author"]
        message["channel"] = package["channel"]
        if "content" in package:
            message["content"] = package["content"]
        if "replies" in package:
            message["replies"] = package["replies"]
        self.messages[package["_id"]] = message
        try:
            self.channels[message["channel"]]["messages"].append(package["_id"])
        except: #creating a dummy channel
            self.channels[message["channel"]] = {}
            self.channels[message["channel"]]["messages"] = []
            self.channels[message["channel"]]["messages"].append(package["_id"])
    
    def insertChannel(self):
        pass
    
    def parseStoatChannel(self, package):
        print(package)
        channel = {}
        if package["channel_type"] == "DirectMessage":
            package["recipients"].remove(self.userID)
            if "display_name" in self.users[package["recipients"][0]]:
                channel["name"] = self.users[package["recipients"][0]]["display_name"]
            else:
                channel["name"] = self.users[package["recipients"][0]]["username"]
        elif package["channel_type"] == "TextChannel":
            channel["name"] = package["name"]
        channel["messages"] = []
        self.channels[package["_id"]] = channel
    
    def parseStoatUser(self, package):
        user = {}
        user["username"] = package["username"]
        user["discriminator"] = package["discriminator"]
        if "display_name" in package:
            user["display_name"] = package["display_name"]
        self.users[package["_id"]] = user
    
    def parseStoatServer(self, package):
        #print(package)
        server = {}
        server["name"] = package["name"]
        server["owner"] = package["owner"]
        server["channels"] = package["channels"]
        self.servers[package["_id"]] = server
        
