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
        point = int((value / self.range) * self.collumHeight)
        newSurf = p.Surface((self.collumWidth * self.collums, self.collumHeight))
        newSurf.blit(self.graphSurface, (-self.collumWidth + 1, 0))
        if point > 0 or self.lastValue > 0:
            polygon = p.draw.polygon(newSurf, self.fillColor, ((newSurf.width - (self.collumWidth-1), self.collumHeight - (self.lastValue)), (newSurf.width - 1, self.collumHeight - (point)), (newSurf.width - 1, newSurf.height- 1), (newSurf.width - (self.collumWidth - 1), newSurf.height - 1)), width=1)
            if polygon.height > 3:
                p.draw.flood_fill(newSurf, self.fillColor, (polygon.centerx, polygon.bottom - 2))
        p.draw.line(newSurf, self.lineColor, (newSurf.width - (self.collumWidth-1), self.collumHeight - (self.lastValue)), (newSurf.width - 1, self.collumHeight - (point)))
        self.lastValue = point
        self.graphSurface = newSurf

if __name__ == "__main__":
    import time
    import random
    
    window = p.display.set_mode((800,600))
    test = graph(window,0,1, collums=70, collumHeight=300)
    
    while True:
        window.fill((0,0,0))
        test.addValue(random.random())
        window.blit(test.graphSurface, (10,10))
        p.display.flip()
        time.sleep(0.2)