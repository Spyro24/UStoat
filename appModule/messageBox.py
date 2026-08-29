import pygame as p
import appModule

class inputTextBox:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.curentMessage = ""
        self.app.renderQuee.append(self)
        self.font = self.app.modules["font"]
        self.renderedRect = p.rect.Rect()
        self.isActive = False
        self.tileSize = self.app.tileSize
        self.sendInChannel = ""
        self.channelSelector = app.modules["channelSelector"]
        self.cursorPos = 0
        self.app.themeable.append(self)
        self.bgCol = (35, 35, 75)
        self.textCol = (255,255,255)
        self.textNoneCol = (0, 0, 0)
        self.i18n = self.app.modules["i18n"].strings
        self.platform = self.app.modules["platform"]
        self.serverSelector = self.app.modules["serverSelector"]
        self.runtimeStore = self.app.modules["runtimeStore"]
        self.hasRendered = False
    
    def reloadTheme(self):
        theme = self.app.modules["themeManager"].theme["messageBox"]
        try:
            self.bgCol = theme["background"]
            self.textCol = theme["text"]
            self.textNoneCol = theme["textNone"]
        except KeyError: pass
            
    def sendMessage(self):
        if self.curentMessage != "":
            self.platform.sendMessage(self.curentMessage, self.channelSelector.selectedChannel, self.serverSelector.selectedServer, {})
            self.curentMessage = ""
        
    def wrap_text_to_width(self, text: str, font: p.font.Font, max_width: int) -> str:
        lines: list[str] = []
        for paragraph in text.split("\n"):
            words: list[str] = paragraph.split(" ")
            current_line: str = ""
            for word in words:
                test_line: str = word if current_line == "" else current_line + " " + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line != "":
                        lines.append(current_line)
                    current_line = word
            lines.append(current_line)
        return "\n".join(lines)
    
    def releaseTextInput(self):
        self.app.textInput = None
        self.isActive = False
    
    def text_input(self, event: p.Event):
        if event.key == p.K_RETURN:
            self.sendMessage()
        elif event.key == p.K_BACKSPACE:
            if self.cursorPos > 0:
                self.curentMessage = self.curentMessage[:self.cursorPos - 1] + self.curentMessage[self.cursorPos:]
                self.cursorPos -= 1
        elif event.key == p.K_DELETE:
            if self.cursorPos < len(self.curentMessage):
                self.curentMessage = self.curentMessage[:self.cursorPos] + self.curentMessage[self.cursorPos + 1:]
        elif event.key == p.K_RIGHT:
            if self.cursorPos < len(self.curentMessage):
                self.cursorPos += 1
        elif event.key == p.K_LEFT:
            if self.cursorPos > 0:
                self.cursorPos -= 1
        else:
            if event.unicode != "":
                self.curentMessage = self.curentMessage[:self.cursorPos] + event.unicode + self.curentMessage[self.cursorPos:]
                self.cursorPos += 1
        
    def render(self, displaySize):
        textBox = None
        self.hasRendered = False
        borderSize = self.tileSize // 8
        textBoxLenght = displaySize[0] - (self.app.modules["userCard"].renderRect.width + self.tileSize * 5)
        usersWriting = False
        if self.channelSelector.selectedChannel in self.runtimeStore.channels:
            usersWriting = len(self.runtimeStore.channels[self.channelSelector.selectedChannel]["typing"]) > 0
        try:
            if self.curentMessage != "":
                showText = self.wrap_text_to_width(self.curentMessage[:self.cursorPos] + "|" + self.curentMessage[self.cursorPos:], self.font, textBoxLenght - (2 * borderSize))
                renderedText = self.font.render(showText, antialias=True, color=self.textCol)
                if renderedText.height > self.tileSize - borderSize / 2:
                    textBox = p.surface.Surface((textBoxLenght, renderedText.height + 2 * borderSize))
                else:
                    textBox = p.surface.Surface((textBoxLenght, self.tileSize))
                textBox.fill(self.bgCol)
                textBox.blit(renderedText, (borderSize, borderSize))
                
            else:
                textBox = p.surface.Surface((textBoxLenght, self.tileSize))
                textBox.fill(self.bgCol)
                textBox.blit(self.font.render(self.i18n['ui.name.message_empty'], antialias=True, color=self.textNoneCol), (borderSize, borderSize))
            self.hasRendered = True
        except p.error as e:
            print("[pygame-ce] Error: " + str(e))
        if self.hasRendered: #Make sure that the programm dont crash
            rectCol = (20, 20, 65)
            if self.isActive:
                rectCol = (120, 120, 165)
            p.draw.rect(textBox, rectCol, textBox.get_rect(), width=borderSize // 2)
            if usersWriting:
                textBoxSize = textBox.get_size()
                infoSurf = p.Surface((textBoxSize[0], self.tileSize // 2))
                infoSurf.fill(self.bgCol)
                newSurf = p.Surface((textBoxSize[0], textBoxSize[1] + infoSurf.height)) #we dont have a name for that
                p.draw.rect(infoSurf, rectCol, infoSurf.get_rect(), width=borderSize // 2)
                if usersWriting:
                    string = ""
                    n = 0
                    try:
                        for user in self.runtimeStore.channels[self.channelSelector.selectedChannel]["typing"]:
                            string += self.runtimeStore.users[user]["username"] + ", "
                            n += 1
                        if n > 1:
                            string = string[:-2] + " are typing"
                        else:
                            string = string[:-2] + " is typing"
                        string = self.font.render(string, True, (255,255,255))
                        infoSurf.blit(string, (borderSize, borderSize))
                    except KeyError: pass #yea that can hapen if the userbase is mising the user
                newSurf.blit(textBox, (0, infoSurf.height))
                newSurf.blit(infoSurf, (0, 0))
                textBox = newSurf
            self.renderedRect = self.app.window.blit(textBox, (self.app.modules["userCard"].renderRect[2], displaySize[1] - textBox.height))
            #Handle mouse input
            if self.renderedRect.collidepoint(self.app.mousePos):
                if self.app.mouseButtons[0]:
                    if self.app.textInput != None:
                        self.app.textInput.isActive = False
                    self.app.textInput = self
                    self.isActive = True
