import appModule

class badgeSystem:
    def __init__(self, app: appModule.app):
        self.moduleName = ""
        self.app = app
        self.requestSystem = app.modules["requestHandler"]
        self.platform = app.modules["platform"]
        self.badgeData = {}
        self.requestedBadges = set()
        self.badges = {}
        self.isReady = False
    
    def insertRequestData(self, data: tuple):
        package = data[2]
        if data[1][0] == "badgeTree":
            self.isReady = True 
            if package != None:
                self.badgeData = package
    
    def getBadge(self, BadgeID):
        pass
    
    def getUserBadges(self, userID):
        try:
            return self.badges[userID]
        except KeyError:
            return []
    
    def makeReady(self):
        self.requestSystem.placeOnCallStack(self.moduleName, ["badgeTree"], lambda: self.platform.getBadgeData())
        self.platform = self.app.modules["platform"]
        