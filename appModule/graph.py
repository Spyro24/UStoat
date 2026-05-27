import pygame as p

class graph:
    def __init__(self, window: p.Surface, minVal, maxVal, collumHeight=50, collumWidth=10, collums=20):
        self.window = window
        self.collums = collums
        self.collumWidth = collumWidth
        self.collumHeight = collumHeight
        self.graphSurface = p.Surface((self.collumWidth + self.collums, collumHeight))
        self.lineColor = (0,255,0)
        self.fillColor = (0,0,255)
        self.lastValue = 0
        self.minVal = minVal
        self.maxVal = maxVal
        self.range = maxVal - minVal
    
    def addValue(self, value):
        value = min(self.maxVal, value)
        value = max(self.minVal, value)
        point = (value / self.range) * self.collumHeight
        newSurf = p.Surface((self.collumWidth * self.collums, self.collumHeight))
        newSurf.blit(self.graphSurface, (-self.collumWidth, 0))
        p.draw.polygon(newSurf, self.fillColor, ((newSurf.width - (1 + self.collumWidth), self.collumHeight - (1 + self.lastValue)), (newSurf.width - 1, self.collumHeight - (1 + point)), (newSurf.width - 1, newSurf.height - 1), (newSurf.width - (1 + self.collumWidth), newSurf.height - 1)))
        p.draw.line(newSurf, self.lineColor, (newSurf.width - (1 + self.collumWidth), self.collumHeight - (1 + self.lastValue)), (newSurf.width - 1, self.collumHeight - (1 + point)))
        self.lastValue = point
        self.graphSurface = newSurf

if __name__ == "__main__":
    import time
    import random
    
    window = p.display.set_mode((800,600))
    test = graph(window,0,200)
    
    while True:
        window.fill((0,0,0))
        test.addValue(random.randint(0,200))
        window.blit(test.graphSurface, (10,10))
        p.display.flip()
        time.sleep(0.5)