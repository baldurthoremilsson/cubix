from GameObject import *

class Cube(GameObject):
    
    def __init__(self, size, color):
        self.size = size
        self.color = color
    
    def display(self):
        glPushMatrix()
        glShadeModel(GL_SMOOTH)
        glEnable ( GL_COLOR_MATERIAL ) ;
        glColor3f(*self.color)
        glutSolidCube(self.size)
        
        glPopMatrix()