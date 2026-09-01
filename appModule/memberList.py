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
        self.lastSeletedServer = ""
        self.renderFromPos = 0
    
    def shortenTextToLenght(self, text: str, lenght: int):
        if lenght <= 0 or len(text) <= lenght:
            return text
        elif len(text) > lenght:
            return text[0:lenght - 3] + "..."
    
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
        background.fill((50,50,100))
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
            if self.runtimeStoreManager.runtimeStore.users[userID]["presence"]:
                statusColor = self.statusColors[self.runtimeStoreManager.runtimeStore.users[userID]["presence"]]
            else:
                statusColor = self.statusColors['online']
        if self.runtimeStoreManager.runtimeStore.users[userID]["status"]:
            text = self.font.render(self.shortenTextToLenght(self.runtimeStoreManager.runtimeStore.users[userID]["status"], 26), True, (200,200,200))
            background.blit(text, (self.tileSize + self.tileSize / 8 * 3, self.tileSize / 16 * 15 - text.height))
        statusIndicator = p.Surface((self.tileSize / 4, self.tileSize /4))
        statusIndicator.fill(statusColor)
        background.blit(statusIndicator, (self.tileSize, self.tileSize / 8 * 5))
        return background
        
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, (50,50,50), (displaySize[0] - self.tileSize * 5, 0, displaySize[0], self.toolBar.renderedRect.top))
        selectedServer = self.serverSelector.selectedServer
        if self.lastSeletedServer != selectedServer:
            self.renderFromPos = 0
            self.lastSeletedServer = selectedServer
        if selectedServer == "0":
            #Here will be the code for rendering a small user card
            pass
        else:
            renderPos = self.renderedRect.top
            memberList = self.runtimeStoreManager.getMemberList(selectedServer)
            membercount = len(memberList)
            maxEntrysOnScreen = self.renderedRect.height // self.tileSize
            if self.renderedRect.collidepoint(self.app.mousePos):
                self.renderFromPos += self.app.mouseWheel
                if self.renderFromPos < 0:
                    self.renderFromPos = 0
            if self.renderFromPos > 0:
                if self.renderFromPos + maxEntrysOnScreen > membercount:
                    self.renderFromPos -= 1
            indexPos = self.renderFromPos
            oldIndexPos = indexPos
            try:
                oldIndexPos = self.renderFromPos
                for n in range(maxEntrysOnScreen):
                    indexPos = self.renderFromPos + n
                    try:
                        userCard = self.renderedUserCards[memberList[indexPos]]
                        if memberList[indexPos] in self.rerenderUsers:
                            self.rerenderUsers.remove(memberList[indexPos])
                            raise KeyError #as always we use this as a shortcut
                    except KeyError:
                        userCard = self.createUserCard(memberList[indexPos])
                        if userCard == 20: continue
                        self.renderedUserCards[memberList[indexPos]] = userCard
                    renderPos = self.window.blit(userCard, (self.renderedRect[0], renderPos)).bottom
            except IndexError: pass
