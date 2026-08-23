import pygame as p
import settings

class escape(settings.base.skeleton):
    def __init__(self, config):
        super().__init__(config)
        self.settingName = "Logout"
        self.warningText = self.font.render(self.i18n.strings["setting.logout.warning"], True, (255,255,255))
    
    def render(self, surface: p.Surface):
        surface.blit(self.warningText, (self.tileSize, self.tileSize))