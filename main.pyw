#! /bin/python3

import pygame as p
import stoat_pylib as stoat
import appModule
import baseModules
import json

# Nuitka compilation support
import os
import sys
from pathlib import Path

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
        app = appModule.app.App()
