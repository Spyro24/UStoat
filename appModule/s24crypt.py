import hashlib
import base64
import zlib

class s24Encryption:
    def __init__(self):
        self.password = ""
    
    def encrypt(self, data: bytes):
        lenData = len(data)
        keyData = bytes()
        password = self.password.encode("UTF8")
        while lenData > len(keyData):
            keyData += hashlib.sha256(keyData + password).digest()
        output = b""
        n = 0
        for byte in data:
             val = (byte + keyData[n]) & 255
             output += val.to_bytes(1)
             n += 1
        return output
    
    def decrypt(self, data: bytes):
        lenData = len(data)
        keyData = bytes()
        password = self.password.encode("UTF8")
        while lenData > len(keyData):
            keyData += hashlib.sha256(keyData - password).digest()
        output = b""
        n = 0
        for byte in data:
             val = (byte + keyData[n]) & 255
             output += val.to_bytes(1)
             n += 1
        return output
