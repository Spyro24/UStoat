import pygame as p

class textInput:
    def __init__(self, parent, font: p.Font, border=4, isPassword=False, chars=24):
        self.fontSize = font.size(" ")
        self.font = font
        self.rectColor = (0, 0, 255)
        self.activeBorderColor = (50, 50, 255)
        self.chars = chars #The lenght in chars of this input box (works only with a monospace font)
        self.isActive = False
        self.parent = parent
    
    def render(self, pos: tuple[int, int]):
        p.draw.rect(self.parent.window)