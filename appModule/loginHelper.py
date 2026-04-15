# (c) 2026 Spyro24
# License: GPLv3

import pygame as p
import requests
import appModule

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
        self.execute()
    
    def execute(self):
        while not self.finished:
            self.currentRun()
        
    def loginTry(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.font.render(f"Loging in to {self.serviceName}...", antialias=True, color=(255,255,255)), (10,10))
        p.display.flip()
        print("loging in")
        try:
            token = self.encryptModule.saveDecrypt(self.app.config["loginData"]["token"]).decode("UTF8")
            self.serviceName = self.app.config["loginData"]["platform"]
            validSession = requests.get("https://stoat.chat/api/users/@me", headers={"X-Session-Token": token}).status_code
            if validSession == 200:
                self.app.modules['account'].loadAccount(self.app.config["loginData"])
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
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"email":f"{self.email}","password":f"{self.password}","friendly_name": self.app.modules['account'].clientName})
        if answer.status_code == 200:
            json = answer.json()
            if json["result"] == "Success":
                self.app.config["loginData"] = {}
                self.app.config["loginData"]["_id"] = json["_id"]
                self.app.config["loginData"]["session"] = json["token"]
                self.app.config["loginData"]["userId"] = json["user_id"]
            elif json["result"] == "MFA":
                self.MFATicket = json["ticket"]
                self.currentRun = self.loginWithMFA
                return
        self.currentRun = self.loginTry
    
    def loginWithMFA(self):
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"mfa_response":{"totp_code":self.MFACode},"mfa_ticket": self.MFATicket,"friendly_name": self.app.modules['account'].clientName})
                    if answer.status_code == 200:
                        json = answer.json()
                        if json["result"] == "Success":
                            self.app.config["loginData"] = {}
                            self.app.config["loginData"]["_id"] = json["_id"]
                            self.app.config["loginData"]["session"] = json["token"]
                            self.app.config["loginData"]["userId"] = json["user_id"]
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