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
        self.isPassword = False #If thats set to True the text will be replaced with "*" to hide it
        self.label = "Test"
        self.text = ""
    
    def text_input(self, event: p.Event):
        if event.key == p.K_RETURN:
            pass
        elif event.key == p.K_BACKSPACE:
            if self.text != "":
                self.text = self.text[:-1]
        else:
            if event.unicode != "":
                self.text += event.unicode
        
    def render(self, pos: tuple[int, int]):
        rect = p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, pos[1], self.rectSize[0], self.rectSize[1]))
        if self.parent.mouseButtons[0]:
            if rect.collidepoint(self.parent.mousePos):
                self.isActive = True
                self.parent.receiveTextInput = self
            else:
                self.isActive = False
                if self.parent.receiveTextInput == self:
                    self.parent.receiveTextInput = None
        if self.isPassword:
            self.parent.window.blit(self.font.render("*" * len(self.text), True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        else:
            self.parent.window.blit(self.font.render(self.text, True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        self.parent.window.blit(self.font.render(self.label, True, (255,255,255)), (rect[0], rect[1] - self.fontSize[1]))
        if self.isActive:
            p.draw.rect(self.parent.window, self.activeBorderColor, rect, width=self.borderSize)
        else:
            p.draw.rect(self.parent.window, self.notActiveBorderColor, rect, width=self.borderSize)
        return rect
    
class button:
    def __init__(self, parent, font: p.Font, borderSize=4, chars=24, call=None):
        '''you should use a lambda function for call because it will insert no args'''
        self.fontSize = font.size(" ")
        self.font = font
        self.rectColor = (64, 128, 255)
        self.border = (0, 64, 128)
        self.chars = chars #The lenght in chars of this button (works only with a monospace font)
        self.isActive = False
        self.parent = parent
        self.borderSize = borderSize
        self.rectSize = (self.borderSize * 2 + self.fontSize[0] * self.chars, self.borderSize * 2 + self.fontSize[1])
        self.label = "Test"
    
    def render(self, pos: tuple[int, int]):
        rect = p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, pos[1], self.rectSize[0], self.rectSize[1]))
        text = self.font.render(self.label, True, (255,255,255))
        self.parent.window.blit(text, (rect.centerx - text.width / 2, rect.centery - text.height / 2))
        p.draw.rect(self.parent.window, self.border, rect, width=self.borderSize)
        '''
        if self.parent.mouseButtons[0]:
            if rect.collidepoint(self.parent.mousePos):
                self.isActive = True
                self.parent.receiveTextInput = self
            else:
                self.isActive = False
                if self.parent.receiveTextInput == self:
                    self.parent.receiveTextInput = None
        if self.isPassword:
            self.parent.window.blit(self.font.render("*" * len(self.text), True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        else:
            self.parent.window.blit(self.font.render(self.text, True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        self.parent.window.blit(self.font.render(self.label, True, (255,255,255)), (rect[0], rect[1] - self.fontSize[1]))
        if self.isActive:
            p.draw.rect(self.parent.window, self.activeBorderColor, rect, width=self.borderSize)
        else:
            p.draw.rect(self.parent.window, self.notActiveBorderColor, rect, width=self.borderSize)
        '''
        return rect

class textKeyDropdown:
    def __init__(self, parent, font: p.Font, keys, borderSize=4, chars=24):
        '''you should use a lambda function for call because it will insert no args'''
        self.fontSize = font.size(" ")
        self.font = font
        self.rectColor = (255, 128, 64)
        self.border = (128, 64, 64)
        self.chars = chars #The lenght in chars of this button (works only with a monospace font)
        self.isActive = False
        self.parent = parent
        self.borderSize = borderSize
        self.rectSize = (self.borderSize * 2 + self.fontSize[0] * self.chars, self.borderSize * 2 + self.fontSize[1])
        self.keys = list(keys)
        self.selectedKey = self.keys[0]
    
    def render(self, pos: tuple[int, int]):
        rect = p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, pos[1], self.rectSize[0], self.rectSize[1]))
        text = self.font.render(self.selectedKey, True, (255,255,255))
        self.parent.window.blit(text, (rect.centerx - text.width / 2, rect.centery - text.height / 2))
        p.draw.rect(self.parent.window, self.border, rect, width=self.borderSize)
        '''
        if self.parent.mouseButtons[0]:
            if rect.collidepoint(self.parent.mousePos):
                self.isActive = True
                self.parent.receiveTextInput = self
            else:
                self.isActive = False
                if self.parent.receiveTextInput == self:
                    self.parent.receiveTextInput = None
        if self.isPassword:
            self.parent.window.blit(self.font.render("*" * len(self.text), True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        else:
            self.parent.window.blit(self.font.render(self.text, True, (255,255,255)), (rect[0] + self.borderSize, rect[1] + self.borderSize))
        self.parent.window.blit(self.font.render(self.label, True, (255,255,255)), (rect[0], rect[1] - self.fontSize[1]))
        if self.isActive:
            p.draw.rect(self.parent.window, self.activeBorderColor, rect, width=self.borderSize)
        else:
            p.draw.rect(self.parent.window, self.notActiveBorderColor, rect, width=self.borderSize)
        '''
        return rect
