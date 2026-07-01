import requests
import json

class gifboxManager:
    def __init__(self):
        self.apiUrl = "https://api.gifbox.me"
        self.mediaUrl = "https://media.gifbox.me"
        self.rpcUrl = "https://rpc.gifbox.me"
        self.categories = [] #Will be filled with self.getCategories() (Please never fill it by yourself)
        self.stoatToken = "" #contains a stoat user token (will be inserted by UStoat)
    
    def getCategories(self):
        if self.stoatToken != "":
            categories = requests.get(f"{self.apiUrl}/categories?")
            if categories.ok:
                jsonData = categories.json()
        else:
            categories = requests.get(f"{self.rpcUrl}/trpc/explore.categories?")
            if categories.ok:
                jsonData = categories.json()
                self.categories = []
                for obj in json.loads(jsonData["result"]["data"]):
                    if type(obj) == str:
                        self.categories.append(obj)
        
    
    def search(self, query: str):
        results = []
        if self.stoatToken != "":
            search = requests.get(f"{self.rpcUrl}/trpc/explore.categories?")
        else:
            search = requests.get(f"{self.rpcUrl}/trpc/posts.search?batch=1&input=" + '%7B%220%22%3A%22%5B%7B%5C%22query%5C%22%3A1%2C%5C%22limit%5C%22%3A2%2C%5C%22direction%5C%22%3A3%7D%2C%5C%22' + query + '%5C%22%2C24%2C%5C%22forward%5C%22%5D%22%7D')
            if search.ok:
                index = 0
                jsonData = search.json()
                data = json.loads(jsonData[0]["result"]["data"])
                resolve = lambda v: resolve(data[v]) if isinstance(v, int) and v < len(data) else v
                results = [[resolve(i.get('title')), resolve(i.get('id'))] for i in data if isinstance(i, dict) and 'id' in i and 'title' in i]
        return results
            

if __name__ == "__main__":
    test = gifboxManager()
    test.getCategories()
    print(test.categories)
    print(test.search("cat"))