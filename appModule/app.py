import pygame as p
import stoat_pylib as stoat
import time
import json
import appModule
import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self):
        p.init()
        self.VERSION = "0.2.3"
        self.window = p.display.set_mode((1080, 720), flags=p.RESIZABLE)
        self.configFilePath = p.system.get_pref_path("spyro24", "ustoat") + "config.json"
        try:
            confgFile = open(self.configFilePath, "r")
            self.config = json.loads(confgFile.read())
            confgFile.close()
        except:
            self.config = {}
        self.renderQuee = []
        self.themeable = []
        self.tileSize = 64
        self.modules = {"font": p.font.SysFont(p.font.match_font(p.font.get_default_font()), size=24, ),
                        "account": stoat.user.Account(),
                        "userManager": stoat.user.users(),
                        "APISubscrption": None,
                        "serverManager": appModule.serverManager.serverManager(),
                        "notify": appModule.notficationHandler.notificatonSystem(),
                        "messageManager": appModule.messageHandler.messageManager()}
        self.modules["userCard"] = appModule.userCard.userCard(self)
        self.modules["cache"] = appModule.cacheSystem.cache(self)
        self.modules["serverSelector"] = appModule.serverManager.serverSelector(self)
        self.modules["channelSelector"] = appModule.serverManager.channelSelector(self)
        self.modules["messageInput"] = appModule.messageBox.inputTextBox(self)
        self.modules["messageRender"] = appModule.messageHandler.messageRender(self)
        self.modules["themeManager"] = appModule.themeManager.themeManager(self)
        self.modules["settings"] = appModule.settingsManager.settingsManager(self)
        self.sounds = {"message": p.mixer.Sound("./res/sounds/stoat.ogg")}
        self.isFocused = False
        self.modules['account'].clientName = f"UStoat (v {self.VERSION})"
        p.display.set_caption(self.modules['account'].clientName)
        self.textInput = None
        self.mousePos = p.mouse.get_pos()
        self.mouseButtons = p.mouse.get_pressed()
        self.setup()
    
    def setup(self):
        appModule.loginHelper.loginHelper(self)
        self.modules['account'].subToAPI()
        self.modules['APISubscrption'] = self.modules['account'].apiSuscription
        self.modules["serverManager"].userManager = self.modules["userManager"]
        self.modules["serverManager"].userID = self.modules["account"].user_id
        self.modules["serverManager"].init()
        getInit = True
        while getInit:
            if self.modules['APISubscrption'].has_new_data():
                for packet in self.modules['APISubscrption'].get_messages():
                    packet = json.loads(packet)
                    if packet["type"] == "Ready":
                        print(packet)
                        for user in packet["users"]:
                            self.modules['userManager'].addUser(user)
                        self.modules["serverManager"].insertReadyPackage(packet)
                        getInit = False
        userInfo = self.modules['userManager'].userInfo[self.modules['account'].user_id]
        self.modules["userCard"].createCard(userInfo)
        print(self.modules["serverManager"].serverStructure)
        self.modules['userManager'].userToken = self.modules['account'].sessionToken
        self.modules["notificatonSystem"] = appModule.notficationHandler.notificationManager(self)

        self.ready()
    
    def ready(self):
        self.modules["serverSelector"].update()
        self.appLoop()
    
    def loginToStoat(self):
        email = input("Email: ")
        password = input("Password: ")
        self.modules['account'].login(email, password)
        if self.modules['account'].curentLoginStatus == "MFA":
            mfaCode = input("MFA Code: ")
            self.modules['account'].authMFA(mfaCode)
        
    def appLoop(self):
        lastRender = 0
        FPS = 1 / 60
        run = True
        while run:
            for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
                elif event.type == p.WINDOWFOCUSGAINED:
                    print("Focused")
                    self.isFocused = True
                elif event.type == p.WINDOWFOCUSLOST:
                    print("Focus lost")
                    self.isFocused = False
                elif event.type == p.KEYDOWN:
                    if self.textInput != None:
                        self.textInput.text_input(event)
            for event in self.modules['APISubscrption'].get_messages():
                eventJson = json.loads(event)
                if eventJson["type"] == "Message":
                    try:
                        self.modules["messageManager"].insertMessage(eventJson)
                        self.modules["notificatonSystem"].scanMessage(eventJson)
                    except BaseException as e:
                        print(eventJson)
                        print(e)
            
            if lastRender + FPS < time.time():
                lastRender = time.time()
                self.mousePos = p.mouse.get_pos()
                self.mouseButtons = p.mouse.get_pressed()
                displaySize = self.window.get_size()
                self.window.fill((0,0,0))
                for obj in self.renderQuee:
                    try:
                        obj.render(displaySize)
                    except AttributeError as e:
                        print(e)
                        run = False
                        break
                p.display.flip()
        
        self.close()
    
    def close(self):
        self.config["loginData"] = self.modules['account'].saveAccount()
        try:
            configFile = open(self.configFilePath, "w")
            json.dump(self.config, configFile, indent=4)
            configFile.close()
        except:
            pass
        p.quit()
    
    #helper functions
    def open_file_selector():
        root = tk.Tk()
        root.withdraw()
        result = {'path': None}
        root.after(0, lambda: result.update(path=filedialog.askopenfilename()))

        while result.get('path') is None:
            try:
                root.update()
            except tk.TclError:
                break
            p.event.get()
            time.sleep(0.5)

        path = result.get('path')
        root.destroy()
        return path
