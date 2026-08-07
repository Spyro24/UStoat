import appModule
import pygame as p

class toolbar:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.app.renderQuee.append(self)
        self.tools = []
        self.renderedRect = p.rect.Rect()
        self.tileSize = app.tileSize
        self.octet = self.tileSize / 8
        self.colors = self.app.modules["themeManager"].theme["toolbar"]
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, self.colors["background"], (displaySize[0] - self.tileSize * 5, displaySize[1] - self.tileSize, self.tileSize * 5, self.tileSize))
        renderPos = 0
        for tool in self.tools:
            cliclRec = self.window.blit(tool.icon, (self.renderedRect[0] + renderPos * self.tileSize + self.octet, self.renderedRect[1] + self.octet))

class channelHeader:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.app.renderQuee.append(self)
        self.app.renderQuee.append(self.app.renderQuee.pop(self.app.renderQuee.index(self.app.modules["channelSelector"])))
        self.tools = []
        self.renderedRect = p.rect.Rect()
        self.tileSize = app.tileSize
        self.octet = self.tileSize / 8
        self.colors = self.app.modules["themeManager"].theme["channelHeader"]
        self.hasRendered = False
        self.app.modules["channelSelector"].channelHeader = self
    
    def render(self, displaySize: tuple[int, int]):
        self.hasRendered = False 
        try:
            self.renderedRect = p.draw.rect(self.window, self.colors["background"], (self.tileSize * 5, 0, displaySize[0] - self.tileSize * 10, self.tileSize))
            self.hasRendered = True 
        except: pass