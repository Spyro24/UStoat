import pygame as p
import time

class settingsManager:
    def __init__(self, app):
        self.minimized = True
        self.icon = p.image.load("./res/icons/settings.png")
        self.closeButton = p.image.load("res/icons/close.png")
        self.savedRenderQuee = []
        self.app = app
        self.app.renderQuee.append(self)
        self.window = self.app.window
        self.tileSize = self.app.tileSize
        self.quarter = self.tileSize // 8
        self.userCard = self.app.modules["userCard"]
    
    def render(self, displaySize: tuple[int, int]):
        if self.minimized:
            pos = self.userCard.renderRect.topright
            button = self.window.blit(self.icon,(pos[0] - self.tileSize + self.quarter, pos[1] + self.quarter))
            if self.app.mouseButtons[0]:
                if button.collidepoint(self.app.mousePos):
                    self.app.textInput.releaseTextInput()
                    self.savedRenderQuee = self.app.renderQuee
                    self.app.renderQuee = [self]
                    self.minimized = False
        else:
            pos = (displaySize[0] - self.tileSize + self.quarter, self.quarter)
            button = self.window.blit(self.closeButton, pos)
            if self.app.mouseButtons[0]:
                if button.collidepoint(self.app.mousePos):
                    self.app.renderQuee = self.savedRenderQuee
                    self.minimized = True