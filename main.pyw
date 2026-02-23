import pygame as p
import stoat_pylib as stoat
import appModule
import json

# Nuitka compilation support
import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    os.chdir(Path(sys.executable).parent)
else:
    os.chdir(Path(__file__).parent)
#---
if __name__ == "__main__":
    app = appModule.app.App()
