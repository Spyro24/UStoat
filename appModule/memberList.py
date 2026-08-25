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
        self.requestSystem = app.modules["requestHandler"]
        self.runtimeStoreManager = app.modules["runtimeStoreManager"]
        self.rerenderUsers = set()
        self.statusColors = app.modules["themeManager"].theme['status']
    
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
        avatar = self.runtimeStoreManager.getUserAvatar(userID)
        if avatar.height == 1 and avatar.width == 1:
            self.rerenderUsers.add(userID)
        background.blit(p.transform.scale(avatar, (self.tileSize - self.octet * 2, self.tileSize - self.octet * 2)), (self.octet, self.octet))
        if "display_name" in self.runtimeStoreManager.runtimeStore.users[userID]:
            background.blit(self.font.render(self.runtimeStoreManager.runtimeStore.users[userID]["display_name"], antialias=True, color=(255,255,255)),(self.tileSize, self.octet))
        else:
            background.blit(self.font.render(self.runtimeStoreManager.runtimeStore.users[userID]["username"], antialias=True, color=(255,255,255)),(self.tileSize, self.octet))
        statusColor = self.statusColors['offline']
        if self.runtimeStoreManager.runtimeStore.users[userID]["online"]:
            statusColor = self.statusColors['online']
        statusIndicator = p.Surface((self.tileSize / 4, self.tileSize /4))
        statusIndicator.fill(statusColor)
        background.blit(statusIndicator, (self.tileSize, self.tileSize / 8 * 5))
        return background
        
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, (50,50,50), (displaySize[0] - self.tileSize * 5, 0, displaySize[1], self.toolBar.renderedRect.top))
        selectedServer = self.serverSelector.selectedServer
        if selectedServer != "0":
            indexPos = 0
            oldIndexPos = 0
            renderPos = self.renderedRect.top
            memberList = self.runtimeStoreManager.getMemberList(selectedServer)
            while indexPos < len(memberList):
                indexPos += 1
                if not self.renderedRect.collidepoint((self.renderedRect.centerx, renderPos + self.tileSize)):
                    break
                try:
                    userCard = self.renderedUserCards[memberList[oldIndexPos]]
                    if memberList[oldIndexPos] in self.rerenderUsers:
                        self.rerenderUsers.remove(memberList[oldIndexPos])
                        raise KeyError #as always we use this as a shortcut
                except KeyError:
                    userCard = self.createUserCard(memberList[oldIndexPos])
                    if userCard == 20: continue
                    self.renderedUserCards[memberList[oldIndexPos]] = userCard
                renderPos = self.window.blit(userCard, (self.renderedRect[0], renderPos)).bottom
                oldIndexPos = indexPos