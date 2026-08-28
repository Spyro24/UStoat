import pygame as p

class skeleton:
    def __init__(self, config): #yes we are using a new style here (this is the test for class inheritance)
        self.font = config["font"]
        self.tileSize = config["tileSize"]
        self.app = config["app"] #i dont want this ...
        self.theming = self.app.modules["themeManager"].theme
        self.i18n = config["i18n"]
        self.settingName = "<skeleton>"
    
    def reset(self): #gets called every time the option is openend
        pass
    
    def createSettingsEntry(self, surface: p.Surface):
        name = self.font.render(self.settingName, True, (255,255,255))
        surface.blit(name, (surface.width / 2 - name.width / 2, surface.height / 2 - name.height / 2))
    
    def render(self, surface: p.Surface, mousePos: tuple[int, int]):
        pass