import json

class credentialManager:
    def __init__(self):
        self.store = {}
        
    def load(self, path: str):
        file = open(path, "r")
        self.store = json.load(file.readall())
        file.close() 
    
    def save(self, path: str):
        jsonString = json.dump(self.store, indent=4)
        file = open(path, "w")
        file.write()
        file.close()
    
    def getEntry(self, name: str):
        pass
    
    def insertEntry(self, name: str, value):
        pass
    
    def removeEntry(self, name: str):
        try:
            self.store.pop(name)
        except KeyError:
            pass