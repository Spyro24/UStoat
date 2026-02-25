import pygame as p
import appModule

class serverManager:
    def __init__(self):
        self.serverStructure = {}
        self.channelToServer = {}
        self.channelNameLookup = {}
    
    def insertReadyPackage(self, package: dict):
        for server in package["servers"]:
            self.serverStructure[server["_id"]] = {}
            self.serverStructure[server["_id"]]["name"] = server["name"]
            self.serverStructure[server["_id"]]["ownerId"] = server["owner"]
            self.serverStructure[server["_id"]]["channels"] = server["channels"]