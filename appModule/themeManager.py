import json

class themeManager:
    def __init__(self):
        self.theme = {"status":{"online":(0, 255, 0),
                                "offline":(100, 100, 100),
                                "focus":(70, 150, 240),
                                "idle":(250, 160, 0),
                                "bussy":(250, 70, 70),
                                "invisible":(100, 100, 100)},
                      "messageBox":{"background":(35, 35, 75),
                                    "text":(255, 255, 255),
                                    "textNone":(0, 0, 0)},
                      "serverSelector":{"background":(234,123,40)},
                      "channelSelector":{"background":(211, 75, 100),
                                         "selected":(200,150,100)},
                      "messageRender":{"background":(75, 35, 125),
                                        "text":(255, 255, 255)},
                      "toolbar":{"background":(140, 0, 140)},
                      "channelHeader":{"background":(140, 0, 140)},
                      "settings": {"buttonBackground": (50,50,60), #We have stolen this values from stoat's settings pages (because my color scheme is bad)
                                   "background":(30,30,30),
                                   "selected":(30,30,30),
                                   "button":(70,70,90),
                                   "buttonHiglight": (90,90,110),
                                   "text":(220,230,250)},
                      }
    
    def loadTheme(self, path: str):
        try:
            themeFile = open(path, "r")
            self.theme = self.merge_into(self.theme, json.load(themeFile)["theme"])
            self.reloadTheme()
            themeFile.close()
        except FileNotFoundError: pass
    
    def reloadTheme(self):
        print("reloadTheme")
        for obj in self.app.themeable:
            obj.reloadTheme()
    
    def merge_into(self, dest: dict, source: dict) -> dict:
        for k, v in source.items():
            if k in dest and isinstance(dest[k], dict) and isinstance(v, dict):
                self.merge_into(dest[k], v)
            else:
                dest[k] = v
        return dest
