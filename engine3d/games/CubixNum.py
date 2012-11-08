from GameObject import *
from Cube import *

class CubixNum(GameObject):
    
    def __init__(self,num,color):
        self.numbers= [ [   [1,1,1],
                            [1,0,1],
                            [1,0,1],
                            [1,0,1],
                            [1,1,1]
                        ],[ [0,1,0],
                            [0,1,0],
                            [0,1,0],
                            [0,1,0],
                            [0,1,0]
                        ],[ [1,1,1],
                            [0,0,1],
                            [1,1,1],
                            [1,0,0],
                            [1,1,1]
                        ],[ [1,1,1],
                            [0,0,1],
                            [0,1,1],
                            [0,0,1],
                            [1,1,1]
                        ],[ [1,0,1],
                            [1,0,1],
                            [1,1,1],
                            [0,0,1],
                            [0,0,1]
                        ],[ [1,1,1],
                            [1,0,0],
                            [1,1,1],
                            [0,0,1],
                            [1,1,1]
                        ],[ [1,1,1],
                            [1,0,0],
                            [1,1,1],
                            [1,0,1],
                            [1,1,1]
                        ],[ [1,1,1],
                            [0,0,1],
                            [0,0,1],
                            [0,0,1],
                            [0,0,1]
                        ],[ [1,1,1],
                            [1,0,1],
                            [1,1,1],
                            [1,0,1],
                            [1,1,1]
                        ],[ [1,1,1],
                            [1,0,1],
                            [1,1,1],
                            [0,0,1],
                            [0,0,1]
                      ] ]
        self.number = self.numbers[num]
        self.color = color
    
    def display(self):
        y = 0
        for row in self.number:
            x = 0
            for cube in row:
                if cube:
                    theCube = Cube(0.35, self.color)
                    glPushMatrix()
                    glTranslated(2.55, 10.5, 0)
                    glTranslated(-x * 1.1 * theCube.size, -y * 1.1 * theCube.size, 16)
                    theCube.display()
                    glPopMatrix()
                x += 1
            y += 1