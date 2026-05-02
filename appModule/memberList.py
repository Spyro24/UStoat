import appModule
import pygame as p

class memebrList:
    def __init__(self, app: appModule.app.App):
        self.moduleName = ""
        self.app = app
        self.window = app.window
        self.tileSize = app.tileSize
        self.octet = self.tileSize / 8
        self.appModules = app.modules
        self.app.renderQuee.append(self)
        self.toolBar = self.appModules["toolbar"]
        self.renderedUserCards = {}
        self.serverMembers = {}
        self.initServer = ["0"] #contains the DM server because no platform has that server
        self.platformHandler = app.modules["platform"]
        self.serverSelector = app.modules["serverSelector"]
        self.renderedRect = p.rect.Rect()
        self.cache = self.app.modules["cache"]
        self.font = self.app.modules['font']
        self.userManager = self.app.modules["userManager"]
        self.requestSystem = app.modules["requestHandler"]
    
    def insertRequestData(self, data: tuple):
        package = data[2]
        if data[1][0] == "getServerMembers":
            if "members" in package:
                memberList = package["members"]
                server = data[1][1]
                self.serverMembers[server] = []
                for member in memberList:
                    self.serverMembers[server].append(member["_id"]["user"])
    
    def createUserCard(self, userID: str):
        background = p.surface.Surface((self.tileSize * 5, self.tileSize))
        background.fill((100,100,150))
        avatar = self.cache.getUserAvatar(userID)
        background.blit(p.transform.scale(avatar, (self.tileSize - self.octet * 2, self.tileSize - self.octet * 2)), (self.octet, self.octet))
        background.blit(self.font.render(self.userManager.getUser(userID)["display_name"], antialias=True, color=(255,255,255)),(self.tileSize, self.octet))
        return background
        
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, (50,50,50), (displaySize[0] - self.tileSize * 5, 0, displaySize[1], self.toolBar.renderedRect.top))
        selectedServer = self.serverSelector.selectedServer
        if selectedServer not in self.initServer:
            if selectedServer != "":
                self.initServer.append(selectedServer)
                self.serverMembers[selectedServer] = []
                self.requestSystem.placeOnCallStack(self.moduleName, ["getServerMembers", selectedServer], lambda: self.platformHandler.fetchServerMembers(selectedServer, ""))
        if selectedServer != "0":
            indexPos = 0
            renderPos = self.renderedRect.top
            memberList = self.serverMembers[selectedServer]
            while indexPos < len(memberList):
                if not self.renderedRect.collidepoint((self.renderedRect.centerx, renderPos + self.tileSize)):
                    break
                try:
                    userCard = self.renderedUserCards[memberList[indexPos]]
                except KeyError:
                    userCard = self.createUserCard(memberList[indexPos])
                    self.renderedUserCards[memberList[indexPos]] = userCard
                renderPos = self.window.blit(userCard, (self.renderedRect[0], renderPos)).bottom
                indexPos += 1