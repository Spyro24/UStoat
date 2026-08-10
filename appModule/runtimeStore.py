class runtimeStore:
    def __init__(self):
        self.messages = {}
        self.channels = {}
        self.users = {}
        self.servers = {}
    
    def insertMessage(self, messageId: str, content: str, author: str, deleted=False, edited=False):
        self.messages[messageId] = {"content": content, "author": author, "deleted": deleted, "edited": edited}
    
    def parseStoatMessage(self, package): #I dont want to add hundreds of lines to the main app
        message = {}
        message["author"] = package["author"]
        message["channel"] = package["channel"]
        if "content" in package:
            message["content"] = package["content"]
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
    
    def parseStoatUser(self, package):
        user = {}
        user["username"] = package["username"]
        user["discriminator"] = package["discriminator"]
        if "display_name" in package:
            user["display_name"] = package["display_name"]
        self.users[package["_id"]] = user
