import pygame as p

class masquradeTool:
    def __init__(self, app):
        self.app = app
        self.icon = p.image.load("res/icons/masq.png")
        self.app.modules["toolbar"].tools.append(self)
        self.toolbar = self.app.modules["toolbar"]
