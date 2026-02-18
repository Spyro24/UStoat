import pygame as p
import stoat_pylib as stoat
import time
import json
import appModule

class App:
    def __init__(self):
        p.init()
        self.tileSize = 64
        self.modules = {"font": p.font.SysFont(None, size=24),
                        "account": stoat.user.Account(),
                        "userManager": stoat.user.users(),
                        "APISubscrption": None}
        self.modules["userCard"] = appModule.userCard.userCard(self)
        self.modules["cache"] = appModule.cacheSystem.cache(self)
        self.window = p.display.set_mode((1080, 720), flags=p.RESIZABLE)
        self.sounds = {"message": p.mixer.Sound("./res/sounds/stoat.ogg")}
        self.renderQuee = []
        self.VERSION = "0.0.2"
        self.setup()
    
    def setup(self):
        self.modules['account'].clientName = f"UStoat (v {self.VERSION})"
        email = input("Email: ")
        password = input("Password: ")
        self.modules['account'].login(email, password)
        if self.modules['account'].curentLoginStatus == "MFA":
            mfaCode = input("MFA Code: ")
            self.modules['account'].authMFA(mfaCode)
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
                        getInit = False
        userInfo = self.modules['userManager'].userInfo[self.modules['account'].user_id]
        self.modules["userCard"].createCard(userInfo)
        print(userInfo)

        self.appLoop()
    
    def playSound(self, name: str):
        self.sounds[name].play()
        
    def appLoop(self):
        lastRender = 0
        FPS = 1 / 60
        run = True
        while run:
            for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
            if lastRender + FPS < time.time():
                lastRender = time.time()
                displaySize = self.window.get_size()
                self.window.fill((0,0,0))
                for obj in self.renderQuee:
                    obj.render(displaySize)
                p.display.flip()
        
        self.close()
    
    def close(self):
        p.quit()