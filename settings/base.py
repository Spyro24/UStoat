import pygame as p

class skeleton:
    def __init__(self, config): #yes we are using a new style here (this is the test for class inheritance)
        self.font = config["font"]
        self.tileSize = config["tileSize"]
        self.app = config["app"] #i dont want this ...
        self.settingName = "<skeleton>"
    
    def reset(self): #gets called every time the option is openend
        pass
    
    def createSettingsEntry(self, surface: p.Surface):
        pass
    
    def render(self, surface: p.Surface):
        pass