import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

import pygame as p

import appModule

class messageEncryption:
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.moduleName = "messageEncryption"
        self.configPath = self.app.configFolderPath + "encryptData/"
        self.log = self.app.modules["log"].log
        self.publicKeys = {} # contains all public eky of every user in the key folder
        os.makedirs(self.configPath, exist_ok=True)
        try:
            self.log(self.moduleName, "loading user key")
            keyFile = open(self.configPath + "userKey.pem", "br")
            self.userKey = serialization.load_pem_private_key(keyFile.read(), password=None)
            keyFile.close()
            self.log(self.moduleName, "user key loaded")
        except FileNotFoundError:
            self.log(self.moduleName, "user key missing, generating one ...")
            self.userKey = rsa.generate_private_key(65537, 4096)
            self.log(self.moduleName, "user key generated")
            self.log(self.moduleName, "saving user key ...")
            keyFile = open(self.configPath + "userKey.pem", "bw")
            keyFile.write(self.userKey.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
            keyFile.close()
            self.log(self.moduleName, "user key saved")

class encryptionHelper():
    def __init__(self, app: appModule.app.App):
        self.app = app
        self.moduleName = "encryptionHelper<"
        self.log = self.app.modules["log"].log
        self.encryption: messageEncryption = self.app.modules["messageEncryption"]
        self.icons = {"locked": p.image.load("./res/icons/locked.png"),
                      "unlocked": p.image.load("./res/icons/unlocked.png")}
        
    
    def scanMessage(self, message: str):
        if message.startswith("e2ee") and message.endswith("e2eeend"):
            pass
        return None