import pygame as p
import stoat_pylib as stoat
import accountModules
import time
import json
import appModule
import tkinter as tk
from tkinter import filedialog
import threading
import queue
import sys
import tools

class App:
    def __init__(self):
        p.init()
        self.mouseWheel = 0
        self.FROZEN = getattr(sys, "frozen", False)
        self.VERSION = "0.3.2"
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
                        "messageManager": appModule.messageHandler.messageManager(),
                        "i18n": appModule.i18n.i18n(),
                        "encryption": appModule.s24crypt.s24Encryption(),
                        "platform": accountModules.stoat.userAccount()}
        self.modules["userCard"] = appModule.userCard.userCard(self)
        self.modules["cache"] = appModule.cacheSystem.cache(self)
        self.modules["serverSelector"] = appModule.serverManager.serverSelector(self)
        self.modules["channelSelector"] = appModule.serverManager.channelSelector(self)
        self.modules["messageInput"] = appModule.messageBox.inputTextBox(self)
        self.modules["messageRender"] = appModule.messageHandler.messageRender(self)
        self.modules["themeManager"] = appModule.themeManager.themeManager(self)
        self.modules["settings"] = appModule.settingsManager.settingsManager(self)
        self.modules["toolbar"] = appModule.toolbar.toolbar(self)
        self.modules["masqTool"] = tools.masqurade.masquradeTool(self)
        self.sounds = {"message": p.mixer.Sound("./res/sounds/stoat.ogg")}
        self.isFocused = False
        #self.modules['account'].clientName = f"UStoat (v {self.VERSION})"
        p.display.set_caption(f"UStoat (v {self.VERSION})")
        self.textInput = None
        self.mousePos = p.mouse.get_pos()
        self.mouseButtons = p.mouse.get_pressed()
        self.setup()
    
    def setup(self):
        appModule.loginHelper.loginHelper(self)
        #self.modules['account'].subToAPI()
        #self.modules['APISubscrption'] = self.modules['account'].apiSuscription
        self.modules["userManager"].platformHelper = self.modules["platform"]
        self.modules["cache"].platform = self.modules["platform"]
        self.modules["messageInput"].platform = self.modules["platform"]
        self.modules["messageRender"].platform = self.modules["platform"]
        self.modules["serverManager"].userManager = self.modules["userManager"]
        self.modules["serverManager"].userID = self.modules["account"].user_id
        self.modules["serverManager"].init()
        self.modules["memberList"] = appModule.memberList.memebrList(self)
        packet = self.modules["platform"].getReadyPackage()
        if packet["type"] == "Ready":
            print(packet)
            for user in packet["users"]:
                self.modules['userManager'].addUser(user)
            self.modules["serverManager"].insertReadyPackage(packet)
        userInfo = self.modules['userManager'].userInfo[self.modules['platform'].userID]
        self.modules["userCard"].createCard(userInfo)
        print(self.modules["serverManager"].serverStructure)
        self.modules['userManager'].userToken = self.modules['account'].sessionToken
        self.modules["notificatonSystem"] = appModule.notficationHandler.notificationManager(self)
        self.ready()
    
    def ready(self):
        self.RPC = appModule.RPCHandler.RPCHandler(self)
        self.modules["serverSelector"].update()
        self.appLoop()
        
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
                elif event.type == p.MOUSEWHEEL:
                    if self.mouseWheel == 0:
                        self.mouseWheel = -event.y
            
            self.modules["platform"].pumpSocket()
            for package in self.modules["platform"].returnSocketData():
                if package["type"] == "Message":
                    try:
                        self.modules["messageManager"].insertMessage(package)
                        self.modules["notificatonSystem"].scanMessage(package)
                    except BaseException as e:
                        print(package)
                        print(e)
            
            if not self.FROZEN: #RPC feature is deactivated in the EXECUTABLEs because its experimental
                self.RPC.handleRequests()
            
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
                self.mouseWheel = 0
        
        self.close()
    
    def close(self):
        try:
            configFile = open(self.configFilePath, "w")
            json.dump(self.config, configFile, indent=4)
            configFile.close()
            self.RPC.server.stop()
        except:
            pass
        p.quit()
        exit()
    
    #helper functions
    def open_file_selector(self):
        def _worker(q):
            root = tk.Tk()
            try:
                q.put(filedialog.askopenfilename(parent=root) or '')
            except Exception:
                q.put('')
            try:
                root.destroy()
            except Exception:
                pass

        q = queue.Queue()
        threading.Thread(target=_worker, args=(q,), daemon=True).start()

        selected = None
        while selected is None:
            p.event.pump()
            try:
                selected = q.get_nowait()
            except queue.Empty:
                selected = None
            time.sleep(0.01)

        return selected 
