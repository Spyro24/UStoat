import appModule
import requests
import pygame as p

class messageRender:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = self.app.window
        self.colors = {"bg": (75, 35, 125),
                       "text": (255, 255, 255),
                       "userName": (150, 150, 150)}
        self.selectedChannel = ""
        self.channelSelector = app.modules["channelSelector"]
        self.tileSize = self.app.tileSize
        self.borderWidth = self.tileSize // 8
        self.app.renderQuee.append(self)
        self.font = self.app.modules["font"]
        self.cache = app.modules["cache"]
        self.app.themeable.append(self)
        self.curMessageIndex = -1
        self.renderedRect = p.rect.Rect()
        self.platform = self.app.modules["platform"]
        self.runtimeStore = self.app.modules["runtimeStore"]
        self.runtimeStoreManager = self.app.modules["runtimeStoreManager"]
        self.requestHandler = self.app.modules["requestHandler"]
        self.fetchingMessages = set()
    
    def reloadTheme(self):
        theme = self.app.modules["themeManager"].theme["messageRender"]
        try:
            self.colors["bg"] = theme["background"]
            self.colors["text"] = theme["text"]
        except KeyError: pass
    
    def fetchChannelMessages(self, channelId):
        reqData = self.platform.fetchMessages(channelId, "")
        messages = reqData["messages"]
        messages.reverse()
        for message in messages:
            print(message)
            self.runtimeStore.parseStoatMessage(message)
        for user in reqData["users"]:
            self.runtimeStore.parseStoatUser(user)
        self.fetchingMessages.remove(channelId)
    
    
    def wrap_text_to_width(self, text: str, font: p.font.Font, max_width: int) -> str:
        lines: list[str] = []
        for paragraph in text.split("\n"):
            words: list[str] = paragraph.split(" ")
            current_line: str = ""
            for word in words:
                test_line: str = word if current_line == "" else current_line + " " + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line != "":
                        lines.append(current_line)
                    current_line = word
            lines.append(current_line)
        return "\n".join(lines)
    
    def renderMessage(self, message: dict, width: int, borderSize):
        message = self.runtimeStore.messages[message]
        surfaceSizeX = width + borderSize + self.tileSize
        if "content" in message: #avoid a crash if the user sended atachments
            renderedMessage = self.app.modules["font"].render(self.wrap_text_to_width(message["content"], self.app.modules["font"], width), antialias=True, color=self.colors["text"])
        else:
            renderedMessage = p.Surface((0,0))
        messageUserName = self.runtimeStore.users[message["author"]]["username"]
        if "display_name" in self.runtimeStore.users[message["author"]]: # checking if the user has a display name
            messageUserName = self.runtimeStore.users[message["author"]]["display_name"] # setting the render name to the dispaly name if the user has one
        renderedName = self.font.render(messageUserName, antialias=False, color=self.colors["userName"])
        textBoxHeight = borderSize * 2 + renderedName.height + renderedMessage.height
        if textBoxHeight < self.tileSize:
            textBoxHeight = self.tileSize
        renderSurface = p.Surface((width + self.tileSize + borderSize, textBoxHeight))
        renderSurface.fill(self.colors["bg"])
        renderSurface.blit(renderedName, (self.tileSize, borderSize))
        renderSurface.blit(renderedMessage, (self.tileSize, borderSize + renderedName.height))
        renderSurface.blit(p.transform.scale(self.runtimeStoreManager.getUserAvatar(message["author"]),(borderSize * 6, borderSize * 6)), (borderSize, borderSize))
        return(renderSurface)
    
    def render(self, displaySize: tuple[int, int]):
        selectedChannel = self.channelSelector.selectedChannel
        renderYPos = displaySize[1] - self.app.modules["messageInput"].renderedRect[3]
        renderXPos = self.app.modules["messageInput"].renderedRect[0]
        messageWith = self.app.modules["messageInput"].renderedRect[2] - (self.tileSize + self.borderWidth)
        self.renderedRect = p.rect.Rect(self.app.modules["channelSelector"].renderedRect.topright, (self.app.modules["messageInput"].renderedRect.width, displaySize[1] - self.app.modules["messageInput"].renderedRect.height))
        if self.app.mouseWheel != 0 and self.renderedRect.collidepoint(self.app.mousePos):
            messageCount = len(self.runtimeStore.channels[selectedChannel]["messages"])
            if self.app.mouseWheel == -1 and self.curMessageIndex == -1:
                self.curMessageIndex = messageCount - 1
            elif self.curMessageIndex != -1:
                self.curMessageIndex += self.app.mouseWheel
                if self.curMessageIndex >= messageCount:
                    self.curMessageIndex = -1
                elif self.curMessageIndex < 0:
                    self.curMessageIndex = 0
        try:
            msgIndex = self.curMessageIndex
            while renderYPos > 0:
                message = self.renderMessage(self.runtimeStore.channels[self.channelSelector.selectedChannel]["messages"][msgIndex], messageWith, self.borderWidth)
                renderYPos -= message.height
                self.window.blit(message, (renderXPos, renderYPos))[3]
                msgIndex -= 1
                if msgIndex == -1:
                    break
        except IndexError:
            self.curMessageIndex = -1
            try:
                if len(self.app.modules["messageManager"].messages[self.channelSelector.selectedChannel]) == 0:
                   raise BaseException
            except:
                if not self.channelSelector.selectedChannel in self.fetchingMessages:
                    self.fetchingMessages.add(self.channelSelector.selectedChannel)
                    self.requestHandler.placeOnCallStack(None, None, lambda: self.fetchChannelMessages(self.channelSelector.selectedChannel))
