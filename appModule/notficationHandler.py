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
        self.runtimeStore = app.modules['runtimeStore']
        self.userId = self.runtimeStore.userID
        self.cache = app.modules["cache"]
        self.userInMsg = "<@" + self.userId + ">"
    
    def scanMessage(self, msg: dict):
        print(msg)
        if "mentions" in msg and self.userId in msg["mentions"]:
            msgType = "[mention]"
            content = ""
            if "replies" in msg:
                msgType = "[reply]"
            if "content" in msg:
                newMsg = []
                oldMsg = msg["content"].split(" ")
                for word in oldMsg:
                    if word.startswith("<@") and word.endswith(">"):
                        mentionId = word[2:-1]
                        print(mentionId)
                        word = "@" + self.runtimeStore.users[mentionId]["username"]
                    newMsg.append(word)
                content = " ".join(newMsg)
            self.notify.notifyUser(content, channel=msgType + " " + self.runtimeStore.channels[msg["channel"]]["name"], icon=self.cache.getUserAvatar(msg["user"]["_id"]))
        '''
        if "content" in msg:
            for word in msg["content"].split(" "):
                if word == self.userInMsg:
                    self.notify.notifyUser(content, channel=self.runtimeStore.channels[msg["channel"]]["name"], icon=self.cache.getUserAvatar(msg["user"]["_id"]))
                    return
        if "replies" in msg:
            for replyId in msg["replies"]:
                if replyId in self.messageManager.userMessages:
                    self.notify.notifyUser(content, channel="[reply]", icon=self.cache.getUserAvatar(msg["user"]["_id"]))
                    return
                
        '''