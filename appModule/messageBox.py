import pygame as p
import stoat_pylib as stoat
import appModule

class inputTextBox:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.curentMessage = "Dies ist ein Teststring der automatisch umgebrochen werden soll wenn er eine bestimmte Breite überschreitet. Hier kommt eine neue Zeile die bereits manuell eingefügt wurde.\nDiese Zeile soll ebenfalls korrekt behandelt werden und weiterhin automatisch umbrechen falls sie zu lang ist. Zum Schluss noch ein sehrsehrsehrlangeswortohneleerzeichen um zu sehen wie sich die Funktion verhält."
        self.app.renderQuee.append(self)
        self.font = self.app.modules["font"]
    
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
    
    def render(self, displaySize):
        self.app.window.blit(self.font.render(self.wrap_text_to_width(self.curentMessage, self.font, 400), antialias=False, color=(255,255,255)))
