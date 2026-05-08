# (c) 2026 Spyro24
# License: GPLv3

import pygame as p
import requests
import appModule
import accountModules

class loginHelper:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = self.app.window
        self.email = ""
        self.password = ""
        self.MFACode = ""
        self.MFATicket = ""
        self.serviceName = ""
        self.font = self.app.modules["font"]
        self.currentRun = self.loginTry
        self.finished = False
        self.encryptModule = app.modules["encryption"]
        self.platformHelper = accountModules.stoat.userAccount()
        self.execute()
    
    def execute(self):
        while not self.finished:
            self.currentRun()
        
    def loginTry(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.font.render(f"Login in to {self.serviceName}...", antialias=True, color=(255,255,255)), (10,10))
        p.display.flip()
        print("loging in")
        try:
            token = self.encryptModule.saveDecrypt(self.app.config["loginData"]["token"]).decode("UTF8")
            self.serviceName = self.app.config["loginData"]["platform"]
            self.platformHelper = accountModules.platforms[self.serviceName]()
            validSession = self.platformHelper.resumeSession(token)
            print(self.platformHelper.returnSaveInfo())
            print(validSession)
            if validSession == 0:
                self.app.modules['platform'] = self.platformHelper
                self.finished = True
            else:
                raise KeyError
        except KeyError:
            self.currentRun = self.askForServiceName
            self.email = ""
            self.password = ""
            self.MFACode = ""
    
    def askForServiceName(self):
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    self.currentRun = self.askForEmail
                elif event.key == p.K_BACKSPACE:
                    self.serviceName = self.serviceName[:-1]
                else:
                    self.serviceName+= event.unicode
        self.window.fill((0, 0, 0))
        self.window.blit(self.font.render("Enter the service name that you would to use\nService: " + self.serviceName + "|", antialias=True, color=(255,255,255)),(10,10))
        p.display.flip()
    
    def askForEmail(self):
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    self.currentRun = self.askForPassword
                elif event.key == p.K_BACKSPACE:
                    self.email = self.email[:-1]
                elif event.key == p.K_v and event.mod & p.KMOD_CTRL:
                    self.email = p.scrap.get_text()
                else:
                    self.email += event.unicode
        self.window.fill((0, 0, 0))
        self.window.blit(self.font.render("Enter your account Email\nEmail: " + self.email, antialias=True, color=(255,255,255)),(10,10))
        p.display.flip()
        
    def askForPassword(self):
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    self.currentRun = self.loginWithoutMFA
                elif event.key == p.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode
        self.window.fill((0, 0, 0))
        self.window.blit(self.font.render("Enter your account password\nPassword: " + self.password, antialias=True, color=(255,255,255)),(10,10))
        p.display.flip()
    
    def loginWithoutMFA(self):
        self.platformHelper = accountModules.platforms[self.serviceName]()
        answer = self.platformHelper.login(self.email, self.password, f"UStoat (v {self.app.VERSION})")
        if answer != 1:
            if answer == 0:
                export = self.platformHelper.returnSaveInfo()
                self.app.config["loginData"] = {}
                self.app.config["loginData"]["token"] = self.encryptModule.saveEncrypt(export["token"].encode("UTF8")).decode("UTF8")
                self.app.config["loginData"]["platform"] = export['service']
            elif answer == 2:
                self.currentRun = self.loginWithMFA
                return
        self.currentRun = self.loginTry
    
    def loginWithMFA(self):
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    if self.platformHelper.loginMFA(self.MFACode) == 0:
                        export = self.platformHelper.returnSaveInfo()
                        self.app.config["loginData"] = {}
                        self.app.config["loginData"]["token"] = self.encryptModule.saveEncrypt(export["token"].encode("UTF8")).decode("UTF8")
                        self.app.config["loginData"]["platform"] = export['service']
                        self.currentRun = self.loginTry
                    else:
                        self.MFACode = ""
                elif event.key == p.K_BACKSPACE:
                    self.MFACode = self.MFACode[:-1]
                else:
                    self.MFACode += event.unicode
        self.window.fill((0, 0, 0))
        self.window.blit(self.font.render("Enter your account MFA code\nCode: " + self.MFACode, antialias=True, color=(255,255,255)),(10,10))
        p.display.flip()