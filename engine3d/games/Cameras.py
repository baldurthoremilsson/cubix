import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '''
    ERROR: PyOpenGL not installed properly.
    '''
    
from GameObject import *
from Vector import *
import math


class Camera(GameObject):
    def __init__(self):
        self.up = Vector([0,1,0])
        self.position = Vector([0,0,-5])
        self.lookat = Vector([0,0,0])
        self.keysDown = {}
        self.keysDownSpecial = {}
        self.debug = None

        
    def strafe(self,speed):
        if self.debug:
            tmpvect = (self.lookat - self.position).normalize()
            strafe = tmpvect.cross( self.up );
            strafe.y = 0
            strafe.normalize();

            self.position.x +=  (strafe.x * speed)
            self.position.z +=  (strafe.z * speed)

            self.lookat.x += (strafe.x*speed)
            self.lookat.z += (strafe.z*speed)
        
    def move(self, speed):
        if self.debug:
            move = (self.lookat - self.position)
            #move.y = 0
            move.normalize()

            self.position.x +=  (move.x * speed)
            self.position.z +=  (move.z * speed)
            self.position.y +=  (move.y * speed)        

            self.lookat.x += (move.x*speed)
            self.lookat.z += (move.z*speed)
            self.lookat.y += (move.y*speed)
        
    def yaw(self, angle):
        if self.debug:
            view = self.lookat - self.position
            (sinAngle, cosAngle) = (math.sin(angle), math.cos(angle))
            newView = Vector([ view.x * cosAngle + view.z * sinAngle, 
                               view.y,
                               view.x * -sinAngle + view.z * cosAngle])
        
            self.lookat.x = self.position.x + newView.x
            self.lookat.y = self.position.y + newView.y
            self.lookat.z = self.position.z + newView.z


    def pitch(self, angle):
        if self.debug:
            view = self.lookat - self.position
            view.normalize()
            
            #if( (view.x > 0.99 and angle < 0) or (view.y < -0.99 and angle > 0 ) ):
            #    return 0
                  
            crossViewUp = self.up.cross(view).normalize()
            self.up.normalize()
            (sinAngle, cosAngle) = (math.sin(angle), math.cos(angle))
            
            newView = Vector( [ (view.x * ( cosAngle + ( 1 - cosAngle) * (crossViewUp.x**2) ) ) + \
                                (view.y * (( 1 - cosAngle) * crossViewUp.x * crossViewUp.y - sinAngle*crossViewUp.z)) + \
                                (view.z * (( 1 - cosAngle) * crossViewUp.z * crossViewUp.x + sinAngle*crossViewUp.y) ),
                                
                                (view.x * (( 1 - cosAngle) * crossViewUp.x * crossViewUp.y + sinAngle*crossViewUp.z)) + \
                                (view.y * ( cosAngle + ( 1 - cosAngle) * (crossViewUp.y**2) ) ) + \
                                (view.z * (( 1 - cosAngle) * crossViewUp.z * crossViewUp.y - sinAngle*crossViewUp.x) ),
                                
                                (view.x * (( 1 - cosAngle) * crossViewUp.x * crossViewUp.z - sinAngle*crossViewUp.y) )+ \
                                (view.y * (( 1 - cosAngle) * crossViewUp.z * crossViewUp.y + sinAngle*crossViewUp.x)) + \
                                (view.z * ( cosAngle + ( 1 - cosAngle) * (crossViewUp.z**2) ) ) ])
                                
            self.lookat = (self.position + newView )
    
    def apply(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt( self.position.x, self.position.y, self.position.z,
                   self.lookat.x,   self.lookat.y,   self.lookat.z, 
                   self.up.x,       self.up.y,       self.up.z        )
    
    

class FPSCamera(Camera):
    def __init__(self):
        Camera.__init__(self)
                    
    def keyboard(self, key, x, y):
        self.keysDown[ord(key)] = True
    
    def keyboardUp(self, key, x, y):
        self.keysDown[ord(key)] = False
    
    def keyboardSpecial(self, key, x, y):
        self.keysDownSpecial[key] = True

    def keyboardSpecialUp(self, key, x, y):
        self.keysDownSpecial[key] = False

        
    def display(self):
        if(self.keysDown.has_key(ord('w')) and self.keysDown[ord('w')]): 
            self.move(0.005)
        
        if(self.keysDown.has_key(ord('s')) and self.keysDown[ord('s')]):
            self.move(-0.005)
        
        if(self.keysDown.has_key(ord('a')) and self.keysDown[ord('a')]):
            self.strafe(-0.05)
        
        if(self.keysDown.has_key(ord('d')) and self.keysDown[ord('d')]):
            self.strafe(0.05)
        
        
        if(self.keysDown.has_key(106) and self.keysDown[106]):
            self.yaw(0.005)    
            
        if(self.keysDown.has_key(105) and self.keysDown[105]):
            self.pitch(0.005)
            
        if(self.keysDown.has_key(108) and self.keysDown[108]):
            self.yaw(-0.005)
            
        if(self.keysDown.has_key(107) and self.keysDown[107]):
            self.pitch(-0.005)
        
        self.apply()