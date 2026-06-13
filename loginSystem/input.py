import pygame as p

class textInput:
    def __init__(self, font: p.Font, border=4, isPassword=False, chars=24):
        self.fontSize = font.size("")[1]
        self.chars = chars #The lenght in chars of this input box (works only with a monospace font)