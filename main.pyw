import pygame as p
import stoat_pylib as stoat
import json

VERSION = "0.0.1"

socketHandler = stoat.socketHandler.socketHandler({})
account = stoat.user.Account()
account.clientName = f"UStoat (v {VERSION})"
account.login("email", "password")
if account.curentLoginStatus == "MFA":
    account.authMFA(input())
account.subToAPI()

userManager = stoat.user.users()

while True:
    if account.apiSuscription.has_new_data():
        for packet in account.apiSuscription.get_messages():
            packet = json.loads(packet)
            if packet["type"] == "Ready":
                for user in packet["users"]:
                    userManager.addUser(user)
                print(userManager.userInfo)