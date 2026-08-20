#! /bin/python3

import pygame as p
import appModule
import baseModules
import json
import sys

# Nuitka compilation support
import os
import sys
from pathlib import Path

args = set()

#---parsing args to make it easier for us---
if "--debug" in sys.argv:
    args.add("DEBUG")
#---

if getattr(sys, "frozen", False):
    DEBUG = False
    os.chdir(Path(sys.executable).parent)
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        os.chdir(meipass)
else:
    os.chdir(Path(__file__).parent)
#---

if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        try:
            app = appModule.app.App()
        except:
            raise SystemExit
    else:
        app = appModule.app.App(args)
