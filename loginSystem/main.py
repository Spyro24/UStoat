import pygame as p
import time

class loginSystem:
    def __init__(self, simpleApp):
        self.app = simpleApp
        self.window = simpleApp.window
        self.appModules = simpleApp.modules # To acces the other modules that are loaded by the main app
        self.logedIn = False
        self.mainLoop() #Execute the main function (and make sure that the user can login)
        
    def mainLoop(self):
        while not self.logedIn:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.app.exit = True
                    self.logedIn = True #We have to break the loop at this point
            self.window.fill((0,0,0))
            p.display.flip()