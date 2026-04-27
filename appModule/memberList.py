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
        self.renderedRect = p.rect.Rect()
    
    def render(self, displaySize: tuple[int, int]):
        self.renderedRect = p.draw.rect(self.window, (50,50,50), (displaySize[0] - self.tileSize * 5, 0, displaySize[1], self.toolBar.renderedRect.top))