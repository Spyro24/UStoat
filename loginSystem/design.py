import pygame as p

class simpleText:
    def __init__(self, parent, text: str):
        self.text = text
        self.app = parent
        self.font = self.app.monoSpaceFont
    
    def render(self, pos: tuple[int, int]):
        self.app.window.blit(self.font.render(self.text, True, (255,255,255)), (pos))