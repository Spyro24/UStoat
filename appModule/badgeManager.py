import appModule

class badgeSystem:
    def __init__(self, app: appModule.app):
        self.moduleName = ""
        self.app = app
        self.platform = app.modules["platform"]
        self.badgeServer = self.platform.supportServer
        self.badgeChannel = self.platform.badgeSystemChannel
        self.badges = {}
    
    def loadBadges():
        pass
        