import pygame as p
import time
import loginSystem as ls 

class loginSystem:
    def __init__(self, simpleApp):
        self.app = simpleApp
        self.window = simpleApp.window
        self.appModules = simpleApp.modules # To acces the other modules that are loaded by the main app
        self.i18n = self.appModules["i18n"].strings
        self.logedIn = False
        self.monoSpaceFont = p.font.SysFont("Ubuntu-mono", self.app.fontSize)
        self.tileSize = self.app.tileSize
        self.borderSize = 4
        self.receiveTextInput = None
        self.email = ls.input.textInput(self, self.monoSpaceFont, borderSize=self.borderSize)
        self.renderQuee = [self.email]
        self.lastRender = 0
        self.FPS = 1 / 60
        self.mainLoop() #Execute the main function (and make sure that the user can login)
        
    def mainLoop(self):
        while not self.logedIn:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.app.exit = True
                    self.logedIn = True #We have to break the loop at this point
            if self.lastRender + self.FPS > time.time():
                self.lastRender = time.time()
                renderPos = (self.window.width / 2, 0)
                self.window.fill((0,0,0))
                p.display.flip()
