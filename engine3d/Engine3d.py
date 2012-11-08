import sys
import time

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GL.ARB import *
    from OpenGL.GLU import *
except:
    print '''
    ERROR: PyOpenGL not installed properly.
    '''
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class Engine3d:

    def __init__(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_DEPTH)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow('Cubix')
        
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, 4.0/3.0, 1.0, 100.0)
        
        #LIGHTS
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])        
        glLightfv (GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.5, 1.0])
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        #Anti aliasing 
        glShadeModel(GL_SMOOTH) #Enable Smooth Shading
        glEnable(GL_BLEND)  #Enable Blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) #Type Of Blending To Use
        self.lastUpdate = glutGet(GLUT_ELAPSED_TIME)

    def setCallbacks(self):
        glutDisplayFunc( self.display )    
        glutIdleFunc( self.update )
        glutPassiveMotionFunc( self.mouse )
        glutSpecialFunc( self.keyboardSpecial )
        glutSpecialUpFunc( self.keyboardSpecialUp )
        glutKeyboardFunc( self.keyboard )
        glutKeyboardUpFunc( self.keyboardUp )
        glutReshapeFunc( self.resize )

    def run(self, game):
        self.game = game;
        self.setCallbacks()
        glutMainLoop()
        
    def mouse(self, x, y):
        self.game.mouse(x, y)

    def resize(self, width, height):
        self.game.resize(width, height)

    def keyboard(self, key, x, y):
        self.game.keyboard(key, x, y)
        
    def keyboardUp(self, key, x, y):
        self.game.keyboardUp(key, x, y)

    def keyboardSpecial(self, key, x, y):
        self.game.keyboardSpecial(key, x, y)

    def keyboardSpecialUp(self, key, x, y):
        self.game.keyboardSpecialUp(key, x, y)
        
    def display(self):
        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.game.display()
        glutSwapBuffers()
        
    def update(self):
        if(self.lastUpdate + 1000.0/72.0 > glutGet(GLUT_ELAPSED_TIME)):
            time.sleep(1.0 / 72.0)
        else:
            self.game.update(self.lastUpdate - glutGet(GLUT_ELAPSED_TIME) / 1000.0)
            self.lastUpdate = glutGet(GLUT_ELAPSED_TIME)
            glutPostRedisplay()
