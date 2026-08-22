import pygame as p
import time
import settings

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
        self.selectedEntry = 0
        self.entrys = [] #contains the settings entrys
        self.selectorEntrys = []
        self.config = {"tileSize": self.app.tileSize, "font": self.app.modules["font"], "app": self.app}
        for setting in settings.entrys:
            entry = setting(self.config)
            self.entrys.append(entry)
            surf = p.Surface((self.tileSize * 5, self.tileSize * 2))
            entry.createSettingsEntry(surf)
            self.selectorEntrys.append(surf)
            
        
    
    def render(self, displaySize: tuple[int, int]):
        if self.minimized:
            pos = self.userCard.renderRect.topright
            button = self.window.blit(self.icon,(pos[0] - self.tileSize + self.quarter, pos[1] + self.quarter))
            if self.app.mouseButtons[0]:
                if button.collidepoint(self.app.mousePos):
                    self.savedRenderQuee = self.app.renderQuee
                    self.app.renderQuee = [self]
                    self.minimized = False
                    if self.app.textInput != None:
                        self.app.textInput.releaseTextInput()
                    self.selectedEntry = 0
                    self.entrys[self.selectedEntry].reset()
        else:
            pos = (displaySize[0] - self.tileSize + self.quarter, self.quarter)
            button = self.window.blit(self.closeButton, pos)
            if self.app.mouseButtons[0]:
                if button.collidepoint(self.app.mousePos):
                    self.app.renderQuee = self.savedRenderQuee
                    self.minimized = True
            pos = 0
            settingsEntrys = len(self.entrys)
            for n in range(settingsEntrys):
                self.window.blit(self.selectorEntrys[n], (0, pos * self.tileSize * 2))
            surf = p.Surface((self.window.width - self.tileSize * 5, self.window.height - self.tileSize))
            self.entrys[self.selectedEntry].render(surf)
            self.window.blit(surf, (self.tileSize * 5, self.tileSize))