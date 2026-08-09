class runtimeStore:
    def __init__(self):
        self.messages = {}
        self.users = {}
        self.servers = {}
    
    def insertMessage(self, messageId: str, content: str, author: str, deleted=False, edited=False):
        self.messages[messageId] = {"content": content, "author": author, "deleted": deleted, "edited": edited}
    
    def parseStoatMessage(self, package): #I dont want to add hundreds of lines to the main app
        print(package)
