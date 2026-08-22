import pygame as p
import settings

class info(settings.base.skeleton):
    def __init__(self, config):
        super().__init__(config)
        self.settingName = "About UStoat"
        self.poweredByPygameCeBanner = p.image.load("./res/misc/powered_by_pygame-ce.png")
        self.poweredByPygameCeBanner = p.transform.smoothscale(self.poweredByPygameCeBanner, (self.poweredByPygameCeBanner.width / 2, self.poweredByPygameCeBanner.height / 2))
        self.infoText = self.font.render(f"Version: {self.app.VERSION}\nRelease: {self.app.FROZEN}", False, (255,255,255))
    
    def createSettingsEntry(self, surface):
        surface.blit(self.font.render(self.settingName, False, (255,255,255)), (self.tileSize / 4, self.tileSize / 4))
    
    def render(self, surface: p.Surface):
        pos = (surface.width - self.poweredByPygameCeBanner.width - self.tileSize / 4, surface.height - self.poweredByPygameCeBanner.height - self.tileSize / 4)
        surface.blit(self.infoText, (self.tileSize, self.tileSize))
        surface.blit(self.poweredByPygameCeBanner, pos)