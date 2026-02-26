import pygame as p
import appModule

class serverManager:
    def __init__(self):
        self.serverStructure = {}
        self.channelToServer = {}
        self.channelNameLookup = {}
        self.servers = []
    
    def insertReadyPackage(self, package: dict):
        for server in package["servers"]:
            self.servers.append(server["_id"])
            self.serverStructure[server["_id"]] = {}
            self.serverStructure[server["_id"]]["name"] = server["name"]
            self.serverStructure[server["_id"]]["ownerId"] = server["owner"]
            self.serverStructure[server["_id"]]["channels"] = server["channels"]

class serverSelector:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.serverManager = app
        self.selectedServer = ""
        self.serverManager = self.app.modules['serverManager']
    
    def update(self):
        self.selectedServer = self.serverManager.servers[0]

class channelSelector:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.window = app.window
        self.tileSize = app.tileSize
        self.serverSelector = app.modules["serverSelector"]