class socketHandler:
    def __init__(self, globalSystem: dict):
        self.globalSystem = globalSystem
    
    def handleIncomingMessage(self, msg):
        print(msg)