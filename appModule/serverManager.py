import pygame as p
import appModule

class serverManager:
    def __init__(self):
        self.serverStructure = {}
        self.channelToServer = {}
        self.channelNameLookup = {}
        self.servers = []
    
    def insertReadyPackage(self, package: dict):
        for server in package["servers"]:
            self.servers.append(server["_id"])
            self.serverStructure[server["_id"]] = {}
            self.serverStructure[server["_id"]]["name"] = server["name"]
            self.serverStructure[server["_id"]]["ownerId"] = server["owner"]
            self.serverStructure[server["_id"]]["channels"] = server["channels"]
            try:
                self.serverStructure[server["_id"]]["iconPath"] = server["icon"]["_id"]
            except KeyError:
                self.serverStructure[server["_id"]]["iconPath"] = ""

class serverSelector:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.serverManager = app
        self.selectedServer = ""
        self.serverManager = self.app.modules['serverManager']
        self.renderedRect = p.rect.Rect()
        self.app.renderQuee.append(self)
        self.tileSize = app.tileSize
        self.cache = app.modules["cache"]
    
    def update(self):
        self.selectedServer = self.serverManager.servers[0]
    
    def render(self, displaySize):
        self.renderedRect = p.draw.rect(self.window, (234,123,40), (0, 0, self.tileSize, self.app.modules["userCard"].renderRect[1]))
        renderPos = 0
        for server in self.serverManager.servers:
            if self.serverManager.serverStructure[server]["iconPath"] != "":
                self.window.blit(p.transform.scale(self.cache.getIcon(self.serverManager.serverStructure[server]["iconPath"]), (self.tileSize, self.tileSize)), (0, self.tileSize * renderPos))
            renderPos += 1

class channelSelector:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.tileSize = app.tileSize
        self.serverSelector = app.modules["serverSelector"]