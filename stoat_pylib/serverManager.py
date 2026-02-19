import requests

class serverManager:
    def __init__(self):
        self.structure = {}
        self.servers = []
        
    def loadServers(self, data: dict):
        for server in data:
            serverId = server["_id"]
            self.servers.append(serverId)
            self.structure[serverId] = {}
            self.structure[serverId]["name"] = server["name"]
            
            