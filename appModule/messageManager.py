class messageManager:
    def __init__(self, app):
        self.app = app
        self.messages = {}
    
    def insertMessagePackage(self, package):
        self.insertMessage(_id=package["_id"], authorId=package["author"], channel=package["channel"], content=package["content"])
        if "replies" in package:
            self.messages[package["_id"]]["replies"] = package["replies"]
    
    def insertMessage(self, _id=None, authorId=None, content=None, channel=None, replies=[], edited=False, deleted=False):
        message = {"id":_id, "author":authorId, "content":content, "replies":replies, "channel":channel, "edited":edited, "deleted":deleted}
        self.messages[_id] = message

class userManager:
    def __self__(self, app):
        self.app = app
        self.users = {}
    
    def insertUser(self, userId=None, name=None, displayName=None, pfpId=None, discriminator=None):
        pass
    
    def clear(self):
        self.users = {}