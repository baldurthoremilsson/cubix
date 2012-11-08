from GameObject import *
from TetrisCube import *

class TetrisNextCube(GameObject):
    
    def __init__(self, type, position = None, rotation = None):
        self.cube = TetrisCube(type, position, rotation)
        self.setType(type)
        self.time = glutGet(GLUT_ELAPSED_TIME)
    
    def display(self):
        self.cube.display()
        
    def setType(self, type):
        self.cube.setType(type)
        if self.cube.type == 0:
            for pos in self.cube.position:
                pos[0] += 0.0
                pos[1] -= 0.1
        if self.cube.type == 1:
            for pos in self.cube.position:
                pos[0] += 0.5
                pos[1] -= 0.2
        if self.cube.type == 2:
            for pos in self.cube.position:
                pos[0] -= 0.5
                pos[1] += 0.3
        if self.cube.type == 5 or self.cube.type == 6:
            for pos in self.cube.position:
                pos[0] += 0.5
                pos[1] -= 0.5