import pygame as p
import appModule

class serverManager:
    def __init__(self):
        self.serverStructure = {}
        self.channelToServer = {}
        self.channelNameLookup = {}
        self.servers = []
        self.userManager = None
        self.userID = None
    
    def init(self):
        self.createDefaultEntrys()
    
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
        
        for channel in package["channels"]:
            if channel["channel_type"] == "TextChannel":
                self.channelNameLookup[channel["_id"]] = channel["name"]
            elif channel["channel_type"] == "DirectMessage":
                self.channelNameLookup[channel["_id"]] = channel["_id"]
                #user = self.userManager.getUser(channel["_id"])
                if len(channel["recipients"]) == 2:
                    for user in channel["recipients"]:
                        if user != self.userID:
                            self.channelNameLookup[channel["_id"]] = self.userManager.getUser(user)["name"]
                print(user)
                self.serverStructure["0"]["channels"].append(channel["_id"])
    
    def createDefaultEntrys(self):
        self.servers.append("0")
        self.serverStructure["0"] = {}
        self.serverStructure["0"]["name"] = "Direct Messages"
        self.serverStructure["0"]["ownerId"] = "None"
        self.serverStructure["0"]["channels"] = []
        self.serverStructure["0"]["iconPath"] = ""
    
    def formatPackage(self, packageSegment: dict):
        pass

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
        self.channelSelector = None
        self.app.themeable.append(self)
        self.bgCol = (234,123,40)
    
    def reloadTheme(self):
        theme = self.app.modules["themeManager"].theme["serverSelector"]
        try:
            self.bgCol = theme["background"]
        except KeyError: pass
    
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
        self.channelSelector.update()
    
    def returnChannels(self) -> list[str]:
        return self.serverManager.serverStructure[self.selectedServer]["channels"]
    
    def render(self, displaySize):
        self.renderedRect = p.draw.rect(self.window, self.bgCol, (0, 0, self.tileSize, self.app.modules["userCard"].renderRect[1]))
        renderPos = 0
        for icon in self.icons:
            if self.window.blit(icon, (self.borderSize, renderPos * self.tileSize + self.borderSize)).collidepoint(self.app.mousePos) and self.app.mouseButtons[0]:
                self.selectorPos = renderPos
                self.selectedServer = self.serverManager.servers[self.selectorPos]
                self.channelSelector.update()
            if renderPos == self.selectorPos:
                p.draw.rect(self.window, (255,255,255), (0,renderPos * self.tileSize + self.borderSize, self.borderSize / 2, self.iconSize))
            renderPos += 1

class channelSelector:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.tileSize = app.tileSize
        self.serverSelector = app.modules["serverSelector"]
        self.serverManager = app.modules["serverManager"]
        self.serverSelector.channelSelector = self
        self.app.renderQuee.append(self)
        self.renderedRect = p.rect.Rect()
        self.selectedChannelIndex = 0
        self.tileSize = self.app.tileSize
        self.font = self.app.modules['font']
        self.backedSurfaces = []
        self.curentServerChannels = []
        self.halfTile = self.tileSize // 2
        self.selectedChannel = ""
        self.bgCol = (211, 75, 100)
        self.selCol = (200,150,100)
        self.app.themeable.append(self)
        self.renderOverflow = False
        self.renderfromChannel = 0
    
    def reloadTheme(self):
        theme = self.app.modules["themeManager"].theme["channelSelector"]
        try:
            self.bgCol = theme["background"]
            self.selCol = theme["selected"]
        except KeyError: pass
    
    def update(self):
        self.backedSurfaces = []
        self.curentServerChannels = self.serverSelector.returnChannels()
        self.selectedChannelIndex = 0
        self.selectedChannel = self.curentServerChannels[self.selectedChannelIndex]
        self.renderfromChannel = 0
        for channel in self.curentServerChannels:
            try:
                text = self.font.render(self.serverManager.channelNameLookup[channel], True, (255,255,255))
            except KeyError:
                text = self.font.render("NO_NAME", True, (255,255,255))
            surface = p.Surface((self.tileSize * 4, self.halfTile))
            surface.fill(self.bgCol)
            surface.blit(text, (surface.height, surface.height // 2 - text.height // 2))
            self.backedSurfaces.append(surface)
    
    def render(self, displaySize):
        self.renderedRect = p.draw.rect(self.window, self.bgCol, (self.tileSize, 0, self.tileSize * 4, self.app.modules["userCard"].renderRect[1]))
        if self.app.mouseWheel != 0:
            if self.renderedRect.collidepoint(self.app.mousePos):
                self.renderfromChannel += self.app.mouseWheel
                if self.renderfromChannel < 0:
                    self.renderfromChannel = 0
                if not self.renderOverflow and self.app.mouseWheel == 1:
                    self.renderfromChannel -= 1
        #elif not self.renderOverflow and self.renderfromChannel > 0:
        #    self.renderfromChannel -= 1
        #if self.renderfromChannel < 0:
        #    self.renderfromChannel = 0
        renderPos = 0
        renderfromChannel = self.renderfromChannel
        self.renderOverflow = False
        while (renderPos + renderfromChannel) < len(self.backedSurfaces):
            surface = self.backedSurfaces[renderfromChannel + renderPos]
            rect = self.window.blit(surface, (self.renderedRect[0], renderPos * self.halfTile))
            if (renderPos + renderfromChannel) == self.selectedChannelIndex: p.draw.rect(self.window, self.selCol, rect, width=4)
            if self.app.mouseButtons[0] and rect.collidepoint(self.app.mousePos):
                self.selectedChannelIndex = renderPos + renderfromChannel
                self.selectedChannel = self.curentServerChannels[self.selectedChannelIndex]
                self.app.modules["messageRender"].curMessageIndex = -1
            if rect.bottom > self.renderedRect.bottom - self.halfTile:
                self.renderOverflow = True
                break
            renderPos += 1