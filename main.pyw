import pygame as p
import stoat_pylib as stoat

VERSION = "0.0.1"

account = stoat.user.Account()
account.clientName = f"UStoat (v {VERSION})"
account.login("user@example.com", "password")
if account.curentLoginStatus == "MFA":
    account.authMFA(input())