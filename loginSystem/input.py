import pygame as p

class textInput:
    def __init__(self, parent, font: p.Font, borderSize=4, isPassword=False, chars=24):
        self.fontSize = font.size(" ")
        self.font = font
        self.rectColor = (0, 0, 255)
        self.activeBorderColor = (128, 128, 255)
        self.notActiveBorderColor = (0, 0, 128)
        self.chars = chars #The lenght in chars of this input box (works only with a monospace font)
        self.isActive = False
        self.parent = parent
        self.borderSize = borderSize
        self.rectSize = (self.borderSize * 2 + self.fontSize[0] * self.chars, self.borderSize * 2 + self.fontSize[1])
        self.text = "Test"
    
    def render(self, pos: tuple[int, int]):
        rect = p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, pos[1], self.rectSize[0], self.rectSize[1]))
        if self.parent.mouseButtons[0]:
            if rect.collidepoint(self.parent.mousePos):
                self.isActive = True
        self.parent.window.blit(self.font.render(self.text, True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        if self.isActive:
            p.draw.rect(self.parent.window, self.activeBorderColor, rect, width=self.borderSize)
        else:
            p.draw.rect(self.parent.window, self.notActiveBorderColor, rect, width=self.borderSize)
        return rect