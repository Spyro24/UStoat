import pygame as p
import stoat_pylib as stoat
import time
import json
import appModule

class App:
    def __init__(self):
        p.init()
        self.configFilePath = p.system.get_pref_path("spyro24", "ustoat") + "config.json"
        try:
            confgFile = open(self.configFilePath, "r")
            self.config = json.loads(confgFile.read())
            confgFile.close()
        except:
            self.config = {}
        self.renderQuee = []
        self.tileSize = 64
        self.modules = {"font": p.font.SysFont(p.font.match_font(p.font.get_default_font()), size=24, ),
                        "account": stoat.user.Account(),
                        "userManager": stoat.user.users(),
                        "APISubscrption": None,
                        "serverManager": stoat.serverManager.serverManager(),
                        "notify": appModule.notficationHandler.notificatonSystem()}
        self.modules["userCard"] = appModule.userCard.userCard(self)
        self.modules["cache"] = appModule.cacheSystem.cache(self)
        self.modules["messageInput"] = appModule.messageBox.inputTextBox(self)
        self.window = p.display.set_mode((1080, 720), flags=p.RESIZABLE)
        self.sounds = {"message": p.mixer.Sound("./res/sounds/stoat.ogg")}
        self.VERSION = "0.0.2"
        self.isFocused = False
        self.modules['account'].clientName = f"UStoat (v {self.VERSION})"
        p.display.set_caption(self.modules['account'].clientName)
        self.setup()
    
    def setup(self):
        try:
            if self.modules['account'].loadAccount(self.config["loginData"]):
                self.loginToStoat()
        except:
            self.loginToStoat()
        self.modules['account'].subToAPI()
        self.modules['APISubscrption'] = self.modules['account'].apiSuscription
        getInit = True
        while getInit:
            if self.modules['APISubscrption'].has_new_data():
                for packet in self.modules['APISubscrption'].get_messages():
                    packet = json.loads(packet)
                    if packet["type"] == "Ready":
                        print(packet)
                        for user in packet["users"]:
                            self.modules['userManager'].addUser(user)
                        self.modules["serverManager"].loadServers(packet["servers"])
                        getInit = False
        userInfo = self.modules['userManager'].userInfo[self.modules['account'].user_id]
        self.modules["userCard"].createCard(userInfo)
        print(self.modules["serverManager"].structure)
        self.modules['userManager'].userToken = self.modules['account'].sessionToken

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
            for event in self.modules['APISubscrption'].get_messages():
                eventJson = json.loads(event)
                if eventJson["type"] == "Message":
                    try:
                        self.modules["notify"].notifyUser(eventJson["content"], icon=self.modules["cache"].getUserAvatar(eventJson["author"]))
                    except KeyError:
                        print(eventJson)
            
            if lastRender + FPS < time.time():
                lastRender = time.time()
                displaySize = self.window.get_size()
                self.window.fill((0,0,0))
                for obj in self.renderQuee:
                    obj.render(displaySize)
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