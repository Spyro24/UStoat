import os
import pathlib
import time

class logger:
    def __init__(self, logPath: str):
        self.logFolder = str(pathlib.Path(logPath).joinpath("logs/"))
        os.makedirs(self.logFolder, exist_ok=True)
        self.latestLog = open(self.logFolder + "/latest.txt", "w")
        creationTime = time.gmtime()
        self.dateLog = open(self.logFolder + f"/{creationTime[0]}-{creationTime[1]:02d}-{creationTime[2]:02d} {creationTime[3]:02d}-{creationTime[4]:02d}-{creationTime[5]:02d}.txt", "w")
        self.log("Logger", "Ready")
        
    def log(self, moduleName: str, string: str):
        creationTime = time.gmtime()
        logStr = f"[{creationTime[0]}-{creationTime[1]:02d}-{creationTime[2]:02d} {creationTime[3]:02d}-{creationTime[4]:02d}-{creationTime[5]:02d}] [{moduleName}] {string}\n"
        self.latestLog.write(logStr)
        self.dateLog.write(logStr)
    
    def close(self):
        self.latestLog.close()
        self.dateLog.close()