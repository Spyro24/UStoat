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
        self.colors = self.app.modules["themeManager"].theme["toolbar"]
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, self.colors["background"], (displaySize[0] - self.tileSize * 5, displaySize[1] - self.tileSize, self.tileSize * 5, self.tileSize))