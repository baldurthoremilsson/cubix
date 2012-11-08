from GameObject import *
from CubixNum import *

class TetrisNum(GameObject):
    
    def __init__(self, x, y, z):
        self.value = 0
        self.number = CubixNum(0,[1,1,0])
        self.x = x
        self.y = y
        self.z = z
        self.color = [1, 1, 0]
    
    def add(self, plus):
        self.value += plus
    
    def getValue(self):
        return self.value
    
    def display(self):
        self.pow = 0
        
        while pow(10, self.pow) <= self.value:
            self.pow += 1
        
        if self.value != 0:
            self.pow -= 1
        self.valueTemp = self.value
        
        while self.pow >= 0:
            glPushMatrix()
            glTranslated(self.x, self.y, self.z)
            glTranslated(self.pow * 1.5, 0, 0)
            self.number = CubixNum(self.valueTemp / pow(10, self.pow), self.color)
            self.number.display()
            glPopMatrix()
            self.valueTemp -= (self.valueTemp / pow(10, self.pow)) * pow(10, self.pow)
            self.pow -= 1