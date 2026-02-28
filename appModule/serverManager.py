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
        self.icons = []
        self.borderSize = self.tileSize // 8
        self.iconSize = self.borderSize * 6
        self.selectorPos = 0
        self.serverListLen = 0
    
    def update(self):
        self.borderSize = self.tileSize // 8
        self.iconSize = self.borderSize * 6
        self.selectedServer = self.serverManager.servers[0]
        self.serverListLen = len(self.serverManager.servers)
        for server in self.serverManager.servers:
            if self.serverManager.serverStructure[server]["iconPath"] != "":
                self.icons.append(p.transform.scale(self.cache.getIcon(self.serverManager.serverStructure[server]["iconPath"]), (self.iconSize, self.iconSize)))
            else:
                self.icons.append(p.Surface((self.iconSize, self.iconSize)))
    
    def returnChannels(self) -> list[str]:
        return self.serverManager.serverStructure[self.selectedServer]["channels"]
    
    def render(self, displaySize):
        self.renderedRect = p.draw.rect(self.window, (234,123,40), (0, 0, self.tileSize, self.app.modules["userCard"].renderRect[1]))
        renderPos = 0
        for icon in self.icons:
            if self.window.blit(icon, (self.borderSize, renderPos * self.tileSize + self.borderSize)).collidepoint(self.app.mousePos) and self.app.mouseButtons[0]:
                self.selectorPos = renderPos
                self.selectedServer = self.serverManager.servers[self.selectorPos]
            if renderPos == self.selectorPos:
                p.draw.rect(self.window, (255,255,255), (0,renderPos * self.tileSize + self.borderSize, self.borderSize / 2, self.iconSize))
            renderPos += 1

class channelSelector:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.tileSize = app.tileSize
        self.serverSelector = app.modules["serverSelector"]
        self.app.renderQuee.append(self)
        self.renderedRect = p.rect.Rect()
        self.selectedChannel = 0
        self.tileSize = self.app.tileSize
        self.font = self.app.modules['font']
    
    def update(self):
        pass
    
    def render(self, displaySize):
        self.renderedRect = p.draw.rect(self.window, (211, 75, 100), (self.tileSize, 0, self.tileSize * 4, self.app.modules["userCard"].renderRect[1]))
        renderPos = 0
        for channel in self.serverSelector.returnChannels():
            self.window.blit(self.font.render(channel, True, (255,255,255)), (self.renderedRect[0] + 8, self.tileSize / 2 * renderPos))
            renderPos += 1