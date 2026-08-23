import pygame as p
import settings

class info(settings.base.skeleton):
    def __init__(self, config):
        super().__init__(config)
        self.settingName = "About UStoat"
        self.poweredByPygameCeBanner = p.image.load("./res/misc/powered_by_pygame-ce.png")
        self.poweredByPygameCeBanner = p.transform.smoothscale(self.poweredByPygameCeBanner, (self.poweredByPygameCeBanner.width / 2, self.poweredByPygameCeBanner.height / 2))
        self.infoText = self.font.render(f"Version: {self.app.VERSION}\nRelease: {self.app.FROZEN}\nLicense: GPLv3", False, (255,255,255))
    
    def reset(self):
        try:
            with open("/proc/self/status") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        rss_kib = int(line.split()[1])
                        self.ramUsageInfo = self.font.render(f"RAM Usage: {rss_kib / 1024:.2f} MB", True, (255,255,255))
                        print(f"{rss_kib / 1024:.2f} MB")
                        break
        except FileNotFoundError:
            self.ramUsageInfo = self.font.render(f"RAM Usage: NOT SUPPORTED", True, (255,255,255))
    
    def render(self, surface: p.Surface):
        pos = (surface.width - self.poweredByPygameCeBanner.width - self.tileSize / 4, surface.height - self.poweredByPygameCeBanner.height - self.tileSize / 4)
        surface.blit(self.ramUsageInfo, surface.blit(self.infoText, (self.tileSize, self.tileSize)).bottomleft) #yes we are using a nested call
        surface.blit(self.poweredByPygameCeBanner, pos)