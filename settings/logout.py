import pygame as p
import settings

class escape(settings.base.skeleton):
    def __init__(self, config):
        super().__init__(config)
        self.settingName = "Logout"
        self.warningText = self.font.render(self.i18n.strings["setting.logout.warning"], True, (255,255,255))
        self.logoutButton = p.Surface((self.tileSize * 3, self.tileSize / 2))
        self.logoutButton.fill(self.theming["settings"]["button"])
        text = self.font.render(self.i18n.strings["settings.logout.logout"], True, self.theming["settings"]["text"])
        self.logoutButton.blit(text, (self.logoutButton.width / 2 - text.width / 2, self.logoutButton.height / 2 - text.height / 2))
    
    def render(self, surface: p.Surface, mousePos):
        rect = surface.blit(self.warningText, (self.tileSize, self.tileSize))
        rect = surface.blit(self.logoutButton, (self.tileSize, rect.bottom + self.tileSize / 2))
        if rect.collidepoint(mousePos):
            p.draw.rect(surface, self.theming["settings"]["buttonHiglight"], rect, width= self.tileSize // 16)
            if self.app.mouseButtons[0]:
                self.app.logout()