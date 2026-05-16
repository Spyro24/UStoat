from notifypy import Notify
import appModule
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
                p.image.save(icon, tmp.name)
                notifycation.icon = tmp.name
            if channel != None:
                notifycation.title = channel
            notifycation.message = message
            notifycation.send()
            self.sound.play()
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)

class notificationManager:
    def __init__(self, app: appModule.app.App):
        self.notify = notificatonSystem()
        self.userId = app.modules['platform'].userID
        self.cache = app.modules["cache"]
        self.userInMsg = "<@" + self.userId + ">"
        self.messageManager = app.modules['messageManager']
        self.messageManager.userId = self.userId
    
    def scanMessage(self, msg: dict):
        notified = False
        if "content" in msg and not notified:
            content = msg["content"]
            if self.userInMsg in content:
                self.notify.notifyUser(content, channel=None, icon=self.cache.getUserAvatar(msg["user"]["_id"]))
                notified = True
        if "replies" in msg and not notified:
            for replyId in msg["replies"]:
                if replyId in self.messageManager.userMessages:
                    self.notify.notifyUser(content, channel="[reply]", icon=self.cache.getUserAvatar(msg["user"]["_id"]))
                    notified = True