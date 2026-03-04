import appModule
import requests
import pygame as p
import io

class cache:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.modules = self.app.modules
        self.store = {"avatars":{},
                      "icons": {}}
    
    def getUserAvatar(self, userId: str):
        try:
            return(self.store['avatars'][userId])
        except KeyError:
            userData = self.modules['userManager'].getUser(userId)
            avatarId = userData['avatarId']
            if avatarId != "": 
                avatar = io.BytesIO(requests.get(f"https://cdn.stoatusercontent.com/avatars/{avatarId}").content)
            else:
                avatar = "./res/images/default_avatar.png"
            avatar = p.image.load(avatar)
            avatar = self.make_square_and_scale(avatar)
            self.store['avatars'][userId] = avatar
            return avatar
    
    def getIcon(self, iconPath: str):
        try:
            return(self.store['icons'][iconPath])
        except KeyError:
            icon = io.BytesIO(requests.get(f"https://cdn.stoatusercontent.com/icons/{iconPath}").content)
            icon = p.image.load(icon)
            icon = self.make_square_and_scale(icon)
            icon = self.create_circular_surface(icon)
            self.store['icons'][iconPath] = icon
            return icon
    
    def make_square_and_scale(self, surface: p.Surface):
        orig_width, orig_height = surface.get_size()
        square_size = min(orig_width, orig_height)
        square_surface = p.Surface((square_size, square_size), p.SRCALPHA)
        x = (square_size - orig_width) // 2
        y = (square_size - orig_height) // 2
        square_surface.blit(surface, (x, y))
        return square_surface

    def create_circular_surface(self, surface):
        circleSurface = p.Surface(surface.get_size(), flags=p.SRCALPHA)
        circleSurface.fill((0,0,0,255))
        p.draw.ellipse(circleSurface, (0,0,0,0), circleSurface.get_rect())
        surface.blit(circleSurface, (0,0), special_flags=p.BLEND_RGBA_SUB)
        return surface
    
