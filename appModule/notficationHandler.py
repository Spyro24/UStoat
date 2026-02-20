from notifypy import Notify
import pygame as p
import tempfile
import os

class notificatonSystem:
    def __init__(self):
        self.sound = p.Sound("./res/sounds/stoat.ogg")

    def notifyUser(self, message: str, channel=None, icon=None):
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        try:
            tmp.close()
            notifycation = Notify()
            if icon != None:
                pygame.image.save(icon, tmp.name)
                notifycation.icon = tmp.name
            if channel != None:
                notifycation.title = channel
            notifycation.message = message
            notifycation.send()
            self.sound.play()
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
        
        
    