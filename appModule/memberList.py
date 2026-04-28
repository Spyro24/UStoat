import appModule
import pygame as p

class memebrList:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.tileSize = app.tileSize
        self.appModules = app.modules
        self.app.renderQuee.append(self)
        self.toolBar = self.appModules["toolbar"]
        self.renderedUserCards = {}
        self.serverMembers = {}
        self.initServer = ["0"] #contains the DM server because no platform has that server
        self.platformHandler = app.modules["platform"]
        self.serverSelector = app.modules["serverSelector"]
        self.renderedRect = p.rect.Rect()
    
    def createUserCard(self, userID: str):
        background = p.surface.Surface((self.tileSize * 5, self.tileSize))
        background.fill((100,100,150))
        return background
        
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, (50,50,50), (displaySize[0] - self.tileSize * 5, 0, displaySize[1], self.toolBar.renderedRect.top))
        selectedServer = self.serverSelector.selectedServer
        if selectedServer not in self.initServer:
            if selectedServer != "":
                self.initServer.append(selectedServer)
                self.serverMembers[selectedServer] = []
                package = self.platformHandler.fetchServerMembers(selectedServer, "")
                if "members" in package:
                    memberList = package["members"]
                    self.serverMembers[selectedServer] = []
                    for member in memberList:
                        self.serverMembers[selectedServer].append(member["_id"]["user"])
                print(self.serverMembers[selectedServer])
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