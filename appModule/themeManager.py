import json

class themeManager:
    def __init__(self, app):
        self.theme = {"messageBox":{"background":(35, 35, 75),
                                    "text":(255, 255, 255),
                                    "textNone":(0, 0, 0)},
                      }
        self.app = app
    
    def loadTheme(self, path: str):
        try:
            themeFile = open(path, "r")
            self.theme = self.merge_into(self.theme, json.load(themeFile))
            self.reloadTheme()
            themeFile.close()
        except FileNotFoundError: pass
    
    def reloadTheme(self):
        for obj in self.app.themeable:
            obj.reloadTheme()
    
    def merge_into(self, dest: dict, source: dict) -> dict:
        for k, v in source.items():
            if k in dest and isinstance(dest[k], dict) and isinstance(v, dict):
                self.merge_into(dest[k], v)
            else:
                dest[k] = v
        return dest
