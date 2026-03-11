import hashlib
import base64
import zlib

class s24Encryption:
    def __init__(self):
        self.password = ""
    
    def encrypt(self, data: bytes, salt="salt"):
        salt = salt.encode("UTF8")
        lenData = len(data)
        keyData = bytes()
        password = self.password.encode("UTF8")
        while lenData > len(keyData):
            keyData += hashlib.sha256(keyData + password + salt).digest()
        output = b""
        n = 0
        for byte in data:
            val = (byte + keyData[n]) & 255
            output += val.to_bytes(1, byteorder="little")
            n += 1
        return output
    
    def decrypt(self, data: bytes, salt="salt"):
        salt = salt.encode("UTF8")
        lenData = len(data)
        keyData = bytes()
        password = self.password.encode("UTF8")
        while lenData > len(keyData):
            keyData += hashlib.sha256(keyData + password + salt).digest()
        output = b""
        n = 0
        for byte in data:
            val = (byte - keyData[n]) & 255
            output += val.to_bytes(1, byteorder="little")
            n += 1
        return output
    
    def saveEncrypt(self, data: bytes):
        data = self.encrypt(data, salt="UStoat")
        data = base64.b64encode(data)
        data = self.encrypt(data, salt="Random")
        data = zlib.compress(data, 9)
        data = self.encrypt(data, salt="Lookup")
        data = base64.b64encode(data)
        return data
    
    def saveDecrypt(self, data: str):
        data = base64.b64decode(data)
        data = self.decrypt(data, salt="Lookup")
        data = zlib.decompress(data)
        data = self.decrypt(data, salt="Random")
        data = base64.b64decode(data)
        data = self.decrypt(data, salt="UStoat")
        return data

if __name__ == "__main__":
    test = s24Encryption()
    test.password = "Never Gonna Give You Up"
    encryptedData = test.saveEncrypt("If you can read this you know the password and you have cracked my encryption".encode("UTF8"))
    print(encryptedData)
    print(test.saveDecrypt(encryptedData))