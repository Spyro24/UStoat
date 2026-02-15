import requests

class Account:
    def __init__(self):
        self.curentLoginStatus: str = "login"
        self.userName: str = ""
        self.clientName: str = "stoat_pylib"
        self.sessionToken = ""
        self.mfa_ticket = ""
        self._id = ""
        self.user_id = ""
        
    def login(self, email: str, password: str):
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"email":f"{email}","password":f"{password}","friendly_name": f"{self.clientName}"}).json()
        self.curentLoginStatus = answer["result"]
        if self.curentLoginStatus == "MFA":
            self.mfa_ticket = answer["ticket"]
    
    def authMFA(self, code: str):
        answer = requests.post("https://stoat.chat/api/auth/session/login?", json={"mfa_response":{"totp_code":f"{code}"},"mfa_ticket": self.mfa_ticket,"friendly_name": self.clientName}).json()
        print(answer)
        self._id = answer["_id"]
        self.user_id = answer["user_id"]
        self.sessionToken = answer["token"]
        