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
        self.monoSpaceFont = self.app.monoFont
        self.tileSize = self.app.tileSize
        self.borderSize = 4
        self.receiveTextInput = None
        self.mouseIsGrabed = False #This is True if a element is the only receiver for mouse inputs
        self.email = ls.input.textInput(self, self.monoSpaceFont, borderSize=self.borderSize)
        self.email.label = self.i18n["ui.login_system.username"]
        self.password = ls.input.textInput(self, self.monoSpaceFont, borderSize=self.borderSize)
        self.password.label = self.i18n["ui.login_system.password"]
        self.password.isPassword = True
        self.loginButton = ls.input.button(self, self.monoSpaceFont, borderSize=self.borderSize, call=self.normalLogin)
        self.loginButton.label = self.i18n["ui.login_system.login"]
        self.platformSelector = ls.input.textKeyDropdown(self, self.monoSpaceFont, accountModules.platforms.keys())
        self.statusInfo = ls.design.simpleText(self, "")
        self.mfaInput = ls.input.textInput(self, self.monoSpaceFont, borderSize=self.borderSize)
        self.mfaInput.label = self.i18n['ui.login_system.mfa']
        self.validateMfaButton = ls.input.button(self, self.monoSpaceFont, borderSize=self.borderSize, call=self.loginWithMfa)
        self.validateMfaButton.label = self.i18n['ui.login_system.mfa_validate']
        #This contains every screen that will get used
        self.screens = {"login":(self.platformSelector, self.email, self.password, self.loginButton, self.statusInfo, self.platformSelector),
                        "mfa":[self.mfaInput, self.validateMfaButton],
                        "action":[self.statusInfo]}
        self.renderQuee = self.screens["login"]
        self.lastRender = 0
        self.FPS = 1 / 60
        self.mousePos = p.mouse.get_pos()
        self.mouseButtons = p.mouse.get_pressed() #Contains the button states of the mouse
        self.checkConfig() #Make sure that the config is complete
        self.mainLoop() #Execute the main function (and make sure that the user can login)
        
    def mainLoop(self):
        if not self.app.config["loginData"]["logedOut"]:
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
                self.platformSelector.secondPass = False
                for element in self.renderQuee:
                    element.render(renderPos)
                    renderPos[1] += self.tileSize * 1.5
                p.display.flip()
        if not self.app.exit and self.logedIn:
            self.app.config["loginData"]["logedOut"] = False
    
    def loginWithToken(self):
        def worker(self, platform, token): #This is the function for the thread (we dont use async to make sure we always know the programm execution path before the programm runs
            platformHelper = accountModules.platforms[platform](self.appModules["log"])
            validSession = platformHelper.resumeSession(token) #It will return 0 if the resume works
            if validSession == 0:
                self.app.modules['platform'] = platformHelper
                self.logedIn = True
            else: #rebuilding the render quee to show the login thingy if the token is invalid (it can hapen)
                self.renderQuee = self.screens['login']
                self.statusInfo.text = self.i18n['ui.login_system.invalid_token']
        try:
            self.statusInfo.text = self.i18n['ui.login_system.login']
            self.renderQuee = self.screens['action']
            token = self.app.modules["encryption"].saveDecrypt(self.app.config["loginData"]["token"]).decode("UTF8")
            platform = self.app.config["loginData"]["platform"]
            threading.Thread(target=lambda: worker(self, platform, token)).start()
        except KeyError: #Rebuilding the login thingy if the config has missing things like token or platform
            self.statusInfo.text = ""
            self.renderQuee = self.screens['login']
    
    def normalLogin(self):
        def worker(self):
            self.app.modules['platform'] = accountModules.platforms[self.platformSelector.selectedKey](self.app.modules["log"])
            status = self.app.modules['platform'].login(self.email.text, self.password.text, f"UStoat (v {self.app.VERSION})")
            if status == 0: #It returns 0 if ewverything goes right and no MFA needed
                export = self.app.modules['platform'].returnSaveInfo()
                self.app.config["loginData"]["token"] = self.app.modules["encryption"].saveEncrypt(export["token"].encode("UTF8")).decode("UTF8")
                self.app.config["loginData"]["platform"] = export['service']
                self.loginWithToken()
            elif status == 1:
                self.statusInfo.text = self.i18n["ui.login_system.invalid_credentials"]
                self.renderQuee = self.screens['login']
            elif status == 2:
                self.renderQuee = self.screens['mfa']
                
        try:
            self.statusInfo.text = self.i18n['ui.login_system.get_token']
            self.renderQuee = self.screens['action']
            threading.Thread(target=lambda: worker(self)).start()
        except:
            pass
    
    def loginWithMfa(self):
        def worker(self):
            if self.app.modules['platform'].loginMFA(self.mfaInput.text) == 0:
                export = self.app.modules['platform'].returnSaveInfo()
                self.app.config["loginData"]["token"] = self.app.modules["encryption"].saveEncrypt(export["token"].encode("UTF8")).decode("UTF8")
                self.app.config["loginData"]["platform"] = export['service']
                self.loginWithToken()
            else:
                self.statusInfo.text = self.i18n['ui.login_system.mfa_code_wrong']
                self.renderQuee = self.screens['login']
        try:
            self.statusInfo.text = self.i18n['ui.login_system.mfa_code_validate']
            self.renderQuee = self.screens['action']
            threading.Thread(target=lambda: worker(self)).start()
        except:
            pass
    
    def checkConfig(self):
        if "loginData" in self.app.config:
            if not "platform" in self.app.config["loginData"]:
                self.app.config["loginData"]["platform"] = ""
            if not "token" in self.app.config["loginData"]:
                self.app.config["loginData"]["token"] = ""
            if not "logedOut" in self.app.config["loginData"]:
                self.app.config["loginData"]["logedOut"] = True
        else:
            self.app.config["loginData"] = {"platform": "", "token":"", "logedOut":True}