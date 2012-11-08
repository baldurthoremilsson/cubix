try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '''
    ERROR: PyOpenGL not installed properly.
    '''

class GameObject:
    
    def update(self, delay): None
    def display(self): None
    def mouse(self, x, y): None
    def keyboard(self, key, x, y): None
    def keyboardUp(self, key, x, y): None
    def keyboardSpecial(self, key, x, y): None
    def keyboardSpecialUp(self, key, x, y): None