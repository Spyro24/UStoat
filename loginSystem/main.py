import pygame as p
import time
import loginSystem as ls
import appModule
import accountModules
import threading

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
        self.email.label = self.i18n["ui.login_system.username"]
        self.password = ls.input.textInput(self, self.monoSpaceFont, borderSize=self.borderSize)
        self.password.label = self.i18n["ui.login_system.password"]
        self.password.isPassword = True
        self.loginButton = ls.input.button(self, self.monoSpaceFont, borderSize=self.borderSize)
        self.loginButton.label = self.i18n["ui.login_system.login"]
        self.platformSelector = ls.input.textKeyDropdown(self, self.monoSpaceFont, accountModules.platforms.keys())
        self.renderQuee = [self.platformSelector, self.email, self.password, self.loginButton]
        self.lastRender = 0
        self.FPS = 1 / 60
        self.mousePos = p.mouse.get_pos()
        self.mouseButtons = p.mouse.get_pressed() #Contains the button states of the mouse
        self.mainLoop() #Execute the main function (and make sure that the user can login)
        
    def mainLoop(self):
        self.loginWithToken()
        while not self.logedIn:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.app.exit = True
                    self.logedIn = True #We have to break the loop at this point
                if event.type == p.KEYDOWN:
                    if self.receiveTextInput:
                        self.receiveTextInput.text_input(event)
            if self.lastRender + self.FPS < time.time():
                self.lastRender = time.time()
                self.mousePos = p.mouse.get_pos()
                self.mouseButtons = p.mouse.get_pressed()
                self.window.fill((0,0,0))
                renderPos = [self.window.width / 2, self.window.height /4]
                for element in self.renderQuee:
                    element.render(renderPos)
                    renderPos[1] += self.tileSize * 1.5
                p.display.flip()
    
    def loginWithToken(self):
        def worker(self, platform, token): #This is the function for the thread (we dont use async to make sure we always know the programm execution path before the programm runs
            platformHelper = accountModules.platforms[platform]()
            validSession = platformHelper.resumeSession(token) #It will return 0 if the resume works
            if validSession == 0:
                self.app.modules['platform'] = platformHelper
                self.logedIn = True
            else: #rebuilding the render quee to show the login thingy if the token is invalid (it can hapen)
                self.renderQuee = [self.platformSelector, self.email, self.password, self.loginButton]
        try:
            self.renderQuee = [ls.design.simpleText(self, "Loging IN")]
            token = self.app.modules["encryption"].saveDecrypt(self.app.config["loginData"]["token"]).decode("UTF8")
            platform = self.app.config["loginData"]["platform"]
            threading.Thread(target=lambda: worker(self, platform, token)).start()
        except KeyError: #Rebuilding the login thingy if the config has missing things like token or platform
            self.renderQuee = [self.platformSelector, self.email, self.password, self.loginButton]
    
    def normalLogin(self):
        def worker(self):
            pass
        