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
        self.sizeY = app.tileSize
        self.hasDefault = False
        self.tilesX = 5
        self.app = app
        self.font = self.app.modules['font']
        self.renderRect = p.rect.Rect()
        
    def createCard(self, userData: dict):
        canvas = p.Surface((self.sizeY * self.tilesX, self.sizeY))
        avatar = self.app.modules["cache"].getUserAvatar(self.app.modules["account"].user_id)
        spacing = self.sizeY // 8
        canvas.fill((50,50,50))
        canvas.blit(p.transform.scale(avatar, (spacing * 6, spacing * 6)), (spacing, spacing))
        canvas.blit(self.font.render(userData["display_name"], color=(255, 255, 255), antialias=False), (self.sizeY, spacing))
        name = self.font.render(userData["name"], color=(200, 200, 200), antialias=False)
        number = self.font.render("#" + userData["discriminator"], color=(150, 150, 150), antialias=False)
        canvas.blit(name, (self.sizeY, spacing * 5))
        canvas.blit(number, (self.sizeY + name.size[0], spacing * 5))
        self.card = canvas.convert()
        self.app.renderQuee.append(self)
    
    def render(self, screenSize: tuple[int, int]):
        self.renderRect = self.app.window.blit(self.card, (0, screenSize[1] - self.card.size[1]))