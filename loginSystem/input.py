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
        '''you should use a lambda function for 'call' because it will insert no args'''
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
        self.fontSize = font.size(" ")
        self.font = font
        self.rectColor = (255, 128, 64)
        self.border = (128, 64, 64)
        self.selected = (64, 128, 64)
        self.chars = chars #The lenght in chars of this button (works only with a monospace font)
        self.isActive = False
        self.parent = parent
        self.borderSize = borderSize
        self.rectSize = (self.borderSize * 2 + self.fontSize[0] * self.chars, self.borderSize * 2 + self.fontSize[1])
        self.keys = list(keys)
        self.selectedKey = self.keys[0]
        self.isOpen = False
        self.secondPass = False
        self.renderPos = (0,0)
    
    def render(self, pos: tuple[int, int]):
        if self.secondPass:
            savedPos = pos #Save the Position of the render because we dont know if the nnext element need it
            pos = self.renderPos
            rect = p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, pos[1], self.rectSize[0], self.rectSize[1]))
            text = self.font.render(self.selectedKey, True, (255,255,255))
            self.parent.window.blit(text, (rect.centerx - text.width / 2, rect.centery - text.height / 2))
            p.draw.rect(self.parent.window, self.border, rect, width=self.borderSize)
            if self.parent.mouseButtons[0]:
                if not self.isOpen:
                    self.isOpen = rect.collidepoint(self.parent.mousePos) #Its a little faster btw to use this method because we only will set one var here
                    self.parent.mouseIsGrabed = True
            if self.isOpen:
                relaseInput = True
                if rect.collidepoint(self.parent.mousePos):
                    relaseInput = False
                start = rect.bottom
                for key in self.keys:
                    if key != self.selectedKey:
                        text = self.font.render(key, True, (255,255,255))
                        clickRect = p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, start, self.rectSize[0], self.rectSize[1]))
                        self.parent.window.blit(text, (clickRect.centerx - text.width / 2, clickRect.centery - text.height / 2))
                        if clickRect.collidepoint(self.parent.mousePos):
                            relaseInput = False
                            p.draw.rect(self.parent.window, self.selected, clickRect, width=self.borderSize)
                            if self.parent.mouseButtons[0]:
                                self.selectedKey = key
                                self.parent.mouseIsGrabed = False
                                self.isOpen = False
                        start = clickRect.bottom
                if self.parent.mouseButtons[0] and relaseInput:
                    self.parent.mouseIsGrabed = False
                    self.isOpen = False
            self.secondPass = False
            return savedPos
        else:
            self.secondPass = True
            self.renderPos = (pos[0], pos[1])
            return p.draw.rect(self.parent.window, self.rectColor, (pos[0] - self.rectSize[0] / 2, pos[1], self.rectSize[0], self.rectSize[1]))
