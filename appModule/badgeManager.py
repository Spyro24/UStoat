import appModule

class badgeSystem:
    def __init__(self, app: appModule.app):
        self.moduleName = ""
        self.app = app
        self.platform = app.modules["platform"]
        self.badgeServer = self.platform.supportServer
        self.badgeChannel = self.platform.badgeSystemChannel
        self.requestSystem = app.modules["requestHandler"]
        self.badgeData = {}
        self.requestedBadges = set()
        self.badges = {}
    
    def insertRequestData(self, data: tuple):
        package = data[2]
        if data[1][0] == "badgeTree":
                print(package)
    
    def loadBadges():
        pass
    
    def makeReady(self):
        self.requestSystem.placeOnCallStack(self.moduleName, ["badgeTree"], lambda: self.platform.getBadgeData())
        