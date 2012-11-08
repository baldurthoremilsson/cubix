from GameObject import *
from Cube import *

class TetrisCube(GameObject):
    
    def __init__(self, type, position = None, rotation = None):
        self.time = glutGet(GLUT_ELAPSED_TIME)
        self.renderPos = position
        self.renderRot = rotation
        self.cheat = None
        
        self.types = [  [ [0,3], [0,4], [0,5], [0,6] ],
                        [ [0,4], [0,5], [1,4], [1,5] ],
                        [ [0,3], [0,4], [0,5], [1,4] ],
                        [ [0,4], [1,4], [2,4], [2,5] ],
                        [ [0,5], [1,5], [2,5], [2,4] ],
                        [ [0,5], [0,6], [1,4], [1,5] ],
                        [ [0,4], [0,5], [1,5], [1,6] ]  ]
        
        self.colors = [ [0.1, 1, 1], [1, 1, 0], [0.6, 0, 0.8], [0, 0, 1], [0.9, 0.6, 0], [1, 0, 0], [0, 1, 0]]
        self.setType(type)
        
        self.rotations =     [	
			[   [[-1, 1], [ 0, 0], [ 1,-1], [ 2,-2]],
                [[ 1,-1], [ 0, 0], [-1, 1], [-2, 2]],
			],
			[	[[ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0]],
			],
			[	[[-1, 1], [ 0, 0], [ 0, 0], [ 0, 0]],
				[[ 0, 0], [ 0, 0], [ 0, 0], [-1,-1]],
				[[ 0, 0], [ 0, 0], [ 1,-1], [ 0, 0]],
				[[ 1,-1], [ 0, 0], [-1, 1], [ 1, 1]],
			],
			[
				[[ 1,-1], [ 0, 0], [-1, 1], [-2, 0]],
				[[ 1, 1], [ 0, 0], [-1,-1], [ 0,-2]],
				[[-1, 1], [ 0, 0], [ 1,-1], [ 2, 0]],
				[[-1,-1], [ 0, 0], [ 1, 1], [ 0, 2]],
			],
			[
				[[ 1,-1], [ 0, 0], [-1, 1], [ 0, 2]],
				[[ 1, 1], [ 0, 0], [-1,-1], [-2, 0]],
				[[-1, 1], [ 0, 0], [ 1,-1], [ 0,-2]],
				[[-1,-1], [ 0, 0], [ 1, 1], [ 2, 0]],
			],
			[
				[[-1,-1], [ 0,-2], [-1, 1], [ 0, 0]],
				[[ 1, 1], [ 0, 2], [ 1,-1], [ 0, 0]],
			],
			[	[[-1, 2], [ 0, 0], [-1, 1], [ 0,-1]],
				[[ 1,-2], [ 0, 0], [ 1,-1], [ 0, 1]],
			]
		]
        
    def display(self):
        for pos in self.position:
            if pos[0] > -1 :
                glPushMatrix()
                if self.renderRot:
                    glRotatef(*self.renderRot)
                if self.renderPos:
                    glTranslated(*self.renderPos)
                glTranslated(pos[1] * 1.1, -pos[0] * 1.1, 0)
                Cube.display(Cube(1, self.color))
                glPopMatrix()
    
    def setType(self, type):
        self.type = type
        self.time = glutGet(GLUT_ELAPSED_TIME)
        self.rotation = 0
        self.color = self.colors[self.type]
        self.position = []
        for pos in self.types[type]:
            # copy position, not use the same object
            self.position.append([pos[0], pos[1]])
    
    def rotate(self):
        i = 0
        for pos in self.position:
            pos[0] += self.rotations[self.type][self.rotation][i][0]
            pos[1] += self.rotations[self.type][self.rotation][i][1]
            i += 1
        if self.rotation == len(self.rotations[self.type]) - 1:
            self.rotation = 0
        else:
            self.rotation += 1
    
    def getRotation(self):
        i = 0
        temp = []
        for pos in self.position:
            temp.append([   pos[0] + self.rotations[self.type][self.rotation][i][0],
                            pos[1] + self.rotations[self.type][self.rotation][i][1]])
            i += 1
        return temp
    
    def getColor(self):
        return self.colors[self.type]