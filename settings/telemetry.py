import pygame as p
import settings

class telemetry(settings.base.skeleton):
    def __init__(self, config):
        super().__init__(config)
        self.settingName = "Telemetry"