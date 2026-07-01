import requests
import json

class gifboxManager:
    def __init__(self):
        self.apiUrl = "https://api.gifbox.me"
        self.mediaUrl = "https://media.gifbox.me"
        self.rpcUrl = "https://rpc.gifbox.me"
        self.categories = [] #Will be filled with self.getCategories() (Please never fill it by yourself)
        self.stoatToken = ""
    
    def getCategories(self):
        categories = requests.get(f"{self.apiUrl}/categories?")
        if categories.ok:
            json = categories.json()
            print(json)
    
    def getCategoriesWithoutToken(self): #Use this functiion to initalize the categories if you dont have a stoat token
        categories = requests.get(f"{self.rpcUrl}/trpc/explore.categories?")
        if categories.ok:
            jsonData = categories.json()
            self.categories = []
            for obj in json.loads(jsonData["result"]["data"]):
                if type(obj) == str:
                    self.categories.append(obj)

if __name__ == "__main__":
    test = gifboxManager()
    test.getCategoriesWithoutToken()
    print(test.categories)