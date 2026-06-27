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
import platform
import loginSystem

class App:
    def __init__(self, erxternalVars=set()):
        p.init()
        self.OS_TYPE = platform.system()
        self.env = erxternalVars
        self.mouseWheel = 0
        self.FROZEN = getattr(sys, "frozen", False)
        self.VERSION = "0.4.0"
        self.exit = False # If this var is set to true the Exit will instantly be trigered (it is used by submodules, they arent allowed to raise the SystemExit)
        self.window = p.display.set_mode((1080, 720), flags=p.RESIZABLE)
        self.configFilePath = p.system.get_pref_path("spyro24", "ustoat") + "config.json"
        try:
            confgFile = open(self.configFilePath, "r")
            self.config = json.loads(confgFile.read())
            confgFile.close()
        except:
            self.config = {"locale":"en_us"}
        self.renderQuee = []
        self.themeable = []
        self.tileSize = 64
        self.fontSize = 24 #Global font size (changing this will change the fontsize of every font)
        self.modules = {"font": p.font.SysFont(p.font.match_font(p.font.get_default_font()), size=self.fontSize),
                        "userManager": stoat.user.users(),
                        "APISubscrption": None,
                        "serverManager": appModule.serverManager.serverManager(),
                        "notify": appModule.notficationHandler.notificatonSystem(),
                        "messageManager": appModule.messageHandler.messageManager(),
                        "i18n": appModule.i18n.i18n(),
                        "encryption": appModule.s24crypt.s24Encryption(),
                        "platform": accountModules.stoat.userAccount(),
                        "requestHandler": appModule.requestHandler.requestHandler()}
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
        self.modules["badgeManager"] = appModule.badgeManager.badgeSystem(self)
        self.sounds = {"message": p.mixer.Sound("./res/sounds/stoat.ogg")}
        self.debugGraph = appModule.graph.graph(self.window, 0, 1/60 * 2)
        self.frameCount = 0
        self.avgFrameRate = 0
        self.isFocused = False
        #self.modules['account'].clientName = f"UStoat (v {self.VERSION})"
        p.display.set_caption(f"UStoat (v {self.VERSION})")
        self.textInput = None
        self.mousePos = p.mouse.get_pos()
        self.mouseButtons = p.mouse.get_pressed()
        self.setup()
    
    def setup(self):
        if not "locale" in self.config:
            self.config["locale"] = "en_us"
        self.modules['i18n'].loadI18N(self.config['locale']) #Load the language file
        loginSystem.main.loginSystem(self) #Call the Login system to make sure that the user will get logged in into the selected platform
        if self.exit: #Check if the user exited from the login system
            self.close() #And close UStoat if that is True
        self.modules["userManager"].platformHelper = self.modules["platform"]
        self.modules["cache"].platform = self.modules["platform"]
        self.modules["messageInput"].platform = self.modules["platform"]
        self.modules["messageRender"].platform = self.modules["platform"]
        self.modules["serverManager"].userManager = self.modules["userManager"]
        self.modules["serverManager"].userID = self.modules["platform"].userID
        self.modules["serverManager"].init()
        self.modules["memberList"] = appModule.memberList.memebrList(self)
        packet = self.modules["platform"].getReadyPackage()
        if packet["type"] == "Ready":
            print(packet)
            for user in packet["users"]:
                self.modules['userManager'].addUser(user)
            self.modules["serverManager"].insertReadyPackage(packet)
        userInfo = self.modules['userManager'].userInfo[self.modules['platform'].userID]
        print(self.modules["serverManager"].serverStructure)
        self.modules['userManager'].userToken = self.modules["platform"].token
        self.modules["notificatonSystem"] = appModule.notficationHandler.notificationManager(self)
        for moduleName in self.modules.keys():
            try:
                self.modules[moduleName].moduleName = moduleName
            except AttributeError: pass
        self.modules["userCard"].createCard(userInfo)
        self.ready()
    
    def ready(self):
        self.RPC = appModule.RPCHandler.RPCHandler(self)
        self.modules["serverSelector"].update()
        self.modules["badgeManager"].makeReady()
        self.appLoop()
        
    def appLoop(self):
        lastRender = 0
        FPS = 1 / 60
        run = True
        while run:
            frameTime = time.time()
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
            for request in self.modules["requestHandler"].getResponses():
                self.modules[request[0]].insertRequestData(request)
            
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
                if "DEBUG" in self.env:
                    self.window.blit(self.debugGraph.graphSurface,(0,0))
                p.display.flip()
                self.frameCount += 1
                self.avgFrameRate += time.time() - frameTime
                if self.frameCount > 20:
                    self.frameCount = 0
                    self.debugGraph.addValue(self.avgFrameRate / 20)
                    self.avgFrameRate = 0
                self.mouseWheel = 0
        
        self.close()
    
    def close(self):
        try:
            configFile = open(self.configFilePath, "w")
            json.dump(self.config, configFile, indent=4)
            configFile.close()
            self.RPC.server.stop()
            self.modules["requestHandler"].stop()
        except:
            pass
        p.quit()
        raise SystemExit
    
    #helper functions
    
    def keyboardInput(self, event: p.Event):
        char = None
        control = None
        action = None
        return (cgar, control, action)
    
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
