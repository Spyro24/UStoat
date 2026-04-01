import appModule
import requests
import pygame as p

class messageManager:
    def __init__(self):
        self.messages = {}
        self.userMessages = []
        self.userId = ""
    
    def insertMessage(self, message: dict):
        if "content" in message:
            msg = self.formatMessage(message)
            if not message['channel'] in self.messages:
                self.messages[message['channel']] = []
            self.messages[message['channel']].append(msg)
            if msg["author"] == self.userId:
                self.userMessages.append(msg["id"])
    
    def populateChannl(self, channel: str):
        pass
    
    def getMessage(self, channel: str, index: int):
        return self.messages[channel][index]
    
    def formatMessage(self, message: dict):
        msg = {}
        msg["author"] = message['author']
        msg["id"] = message["_id"]
        msg["content"] = message["content"]
        return msg
    
class messageRender:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = self.app.window
        self.colors = {"bg": (75, 35, 125),
                       "text": (255, 255, 255),
                       "userName": (150, 150, 150)}
        self.selectedChannel = "01F92C5ZXBQWQ8KY7J8KY917NM"
        self.channelSelector = app.modules["channelSelector"]
        self.tileSize = self.app.tileSize
        self.app.renderQuee.append(self)
        self.font = self.app.modules["font"]
        self.cache = app.modules["cache"]
        self.app.themeable.append(self)
    
    def reloadTheme(self):
        theme = self.app.modules["themeManager"].theme["messageRender"]
        try:
            self.colors["bg"] = theme["background"]
        except KeyError: pass
    
    def setChannel(self, channelId: str):
        pass
    
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
        surfaceSizeX = width + borderSize + self.tileSize
        renderedMessage = self.app.modules["font"].render(self.wrap_text_to_width(message["content"], self.app.modules["font"], width), antialias=True, color=self.colors["text"])
        renderedName = self.font.render(self.app.modules['userManager'].getUser(message["author"])["display_name"], antialias=False, color=self.colors["userName"])
        textBoxHeight = borderSize * 2 + renderedName.height + renderedMessage.height
        if textBoxHeight < self.tileSize:
            textBoxHeight = self.tileSize
        renderSurface = p.Surface((width + self.tileSize + borderSize, textBoxHeight))
        renderSurface.fill(self.colors["bg"])
        renderSurface.blit(renderedName, (self.tileSize, borderSize))
        renderSurface.blit(renderedMessage, (self.tileSize, borderSize + renderedName.height))
        renderSurface.blit(p.transform.scale(self.cache.getUserAvatar(message["author"]),(borderSize * 6, borderSize * 6)), (borderSize, borderSize))
        return(renderSurface)
    
    def render(self, displaySize: tuple[int, int]):
        renderYPos = displaySize[1] - self.app.modules["messageInput"].renderedRect[3]
        renderXPos = self.app.modules["messageInput"].renderedRect[0]
        borderWidth = self.tileSize // 8
        messageWith = self.app.modules["messageInput"].renderedRect[2] - (self.tileSize + borderWidth)
        try:
            msgIndex = -1
            while renderYPos > 0:
                text = self.renderMessage(self.app.modules["messageManager"].getMessage(self.channelSelector.selectedChannel, msgIndex), messageWith, borderWidth)
                renderYPos -= text.height
                self.window.blit(text, (renderXPos, renderYPos))[3]
                msgIndex -= 1
        except:
            try:
                print(len(self.app.modules["messageManager"].messages[self.channelSelector.selectedChannel]))
                if len(self.app.modules["messageManager"].messages[self.channelSelector.selectedChannel]) == 0:
                   raise BaseException
            except:
                messages = requests.get(f"https://stoat.chat/api/channels/{self.channelSelector.selectedChannel}/messages", headers={"X-Session-Token": self.app.modules['account'].sessionToken}).json()
                try:
                    messages.reverse()
                    for message in messages:
                        self.app.modules["messageManager"].insertMessage(message)
                except: pass