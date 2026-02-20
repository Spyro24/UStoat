import pygame as p
import stoat_pylib as stoat
import appModule

class inputTextBox:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.curentMessage = "" #"Dies ist ein Teststring der automatisch umgebrochen werden soll wenn er eine bestimmte Breite überschreitet. Hier kommt eine neue Zeile die bereits manuell eingefügt wurde.\nDiese Zeile soll ebenfalls korrekt behandelt werden und weiterhin automatisch umbrechen falls sie zu lang ist. Zum Schluss noch ein sehrsehrsehrlangeswortohneleerzeichen um zu sehen wie sich die Funktion verhält."
        self.app.renderQuee.append(self)
        self.font = self.app.modules["font"]
        self.renderedRect = p.rect.Rect()
        self.isActive = False
        self.tileSize = self.app.tileSize
    
    def sendMessage(self):
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
    
    def text_input(self):
        pass
    
    def render(self, displaySize):
        textBox = None
        borderSize = self.tileSize // 8
        textBoxLenght = displaySize[0] - (self.app.modules["userCard"].renderRect.width + self.tileSize * 5)
        if self.curentMessage != "":
            pass
        else:
            textBox = p.surface.Surface((textBoxLenght, self.tileSize))
            textBox.fill((35, 35, 75))
            textBox.blit(self.font.render("Message...", antialias=False, color=(0, 0, 0)), (borderSize, borderSize))
        if self.isActive:
            pass
        else:
            p.draw.rect(textBox, (20, 20, 65), textBox.get_rect(), width=borderSize // 2)
        self.renderedRect = self.app.window.blit(textBox, (self.app.modules["userCard"].renderRect[2], displaySize[1] - textBox.height))
