import pygame as p
import requests
import appModule
import io

class userCard:
    def __init__(self, app: appModule.app.App):
        self.scale = 1
        self.card = p.Surface((0, 0))
        self.name = ""
        self.descriptor = ""
        self.sizeY = 64
        self.hasDefault = False
        self.tilesX = 5
        self.app = app
        self.font = self.app.modules['font']
        
    def createCard(self, userData: dict):
        canvas = p.Surface((self.sizeY * self.tilesX, self.sizeY))
        if userData["avatarId"] == "":
            pass
        else:
            avatar = requests.get(f"https://cdn.stoatusercontent.com/avatars/{userData['avatarId']}")
            image = io.BytesIO(avatar.content)
        avatar = p.image.load(image)
        spacing = self.sizeY // 8
        canvas.fill((50,50,50))
        canvas.blit(self.make_square_and_scale(avatar, spacing * 6), (spacing, spacing))
        canvas.blit(self.font.render(userData["display_name"], color=(255, 255, 255), antialias=False), (self.sizeY, spacing))
        name = self.font.render(userData["name"], color=(200, 200, 200), antialias=False)
        number = self.font.render("#" + userData["discriminator"], color=(150, 150, 150), antialias=False)
        canvas.blit(name, (self.sizeY, spacing * 5))
        canvas.blit(number, (self.sizeY + name.size[0], spacing * 5))
        self.card = canvas
        self.app.renderQuee.append(self)

    def make_square_and_scale(self, surface: p.Surface, target_size: int):
        orig_width, orig_height = surface.get_size()
        square_size = min(orig_width, orig_height)

        square_surface = p.Surface((square_size, square_size), p.SRCALPHA)
        x = (square_size - orig_width) // 2
        y = (square_size - orig_height) // 2
        square_surface.blit(surface, (x, y))
        scaled_surface = p.transform.scale(square_surface, (target_size, target_size))
        return scaled_surface
    
    def render(self, screenSize: tuple[int, int]):
        self.app.window.blit(self.card, (0, screenSize[1] - self.card.size[1]))