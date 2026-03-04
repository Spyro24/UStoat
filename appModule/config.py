import json

class config:
    def __init__(self):
        self.config = {"isEncrypted": False,
                       }
    
    def load(self, file: str):
        pass
    
    def save(self, file:str):
        pass
    
    def merge_if_exists(self, dict1, dict2):
        for key in dict2:
            if key in dict1:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    self.merge_if_exists(dict1[key], dict2[key])
                else:
                    dict1[key] = dict2[key]
        return dict1
