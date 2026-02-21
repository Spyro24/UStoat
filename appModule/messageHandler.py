class messageManager:
    def __init__(self):
        self.messages = {}
    
    def insertMessage(self, message: dict):
        if message['author'] != "00000000000000000000000000": #we cant handle the system messages
            msg = self.formatMessage(message)
            if not message['channel'] in self.messages:
                self.messages[message['channel']] = []
            self.messages[message['channel']].append(msg)
    
    def formatMessage(self, message: dict):
        msg = {}
        msg["author"] = message['author']
        msg["id"] = message
        msg["content"] = message["content"]
        return msg