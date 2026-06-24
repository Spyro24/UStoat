import pygame as p

class simpleText:
    def __init__(self, parent, text: str):
        self.text = text
        self.app = parent
        self.font = self.app.monoSpaceFont
    
    def render(self, pos: tuple[int, int]):
        text = self.font.render(self.text, True, (255,255,255))
        self.app.window.blit(text, (pos[0] - text.width / 2, pos[1] - text.height / 2))