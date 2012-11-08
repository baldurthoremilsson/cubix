from TetrisGrid import *
from Cameras import FPSCamera
from Cube import *
from TetrisCube import *
from TetrisHUD import *
from TetrisData import *
from random import *
import os

class Tetris3d:
    
    def __init__(self):
        self.data = TetrisData()
        self.objects = {}
        self.registerObject('1camera', FPSCamera())
        self.registerObject('mainGrid', TetrisGrid(self, 10, 20))
        self.registerObject('TetrisHUD', TetrisHUD(self))
        self.cheatChangeCube = ""
        self.cheatHelperCube = ""
        self.cheatSlideCube = ""
    
    def registerObject(self, name, object):
        self.objects[name] = object

    def deleteObject(self, name):
        self.objects.pop(name)
    
    def mouse(self, x, y):
        for key, obj in self.objects.iteritems():
            obj.mouse(x, y)

    def resize(self, width, height):
        pass

    def keyboard(self, key, x, y):
        # cheat
        # changeCube
        if self.cheatChangeCube != None:
            if key == 'e':
                self.cheatChangeCube = key
            else:
                self.cheatChangeCube += key
            if self.cheatChangeCube == 'eddi3d':
                self.objects['mainGrid'].cheatChangeCube = True
                self.cheatChangeCube = None
        #changeCube
        # helperCube
        if key == 'v':
            self.cheatHelperCube = key
        else:
            self.cheatHelperCube += key
        if self.cheatHelperCube == 'verzlo':
            if self.objects['mainGrid'].cheatHelperCube == True:
                self.objects['mainGrid'].cheatHelperCube = None
            else:
                self.objects['mainGrid'].cheatHelperCube = True
            self.cheatHelperCube = ""
        #helperCube
        # slideCube
        if key == 'a' and self.cheatSlideCube != 'all':
            self.cheatSlideCube = key
        else:
            self.cheatSlideCube += key
        if self.cheatSlideCube == 'alla':
            if self.objects['mainGrid'].cheatSlideCube == True:
                self.objects['mainGrid'].cheatSlideCube = None
                try:
                    os.remove('slidecheat')
                except: pass
            else:
                self.objects['mainGrid'].cheatSlideCube = True
                f = os.open('slidecheat', os.O_CREAT)
                print f
        #slideCube
        #cheat
        
        for k, obj in self.objects.iteritems():
            obj.keyboard(key, x, y)
        
    def keyboardUp(self, key, x, y):
        for k, obj in self.objects.iteritems():
            obj.keyboardUp(key, x, y)

    def keyboardSpecial(self, key, x, y):
        for k, obj in self.objects.iteritems():
            obj.keyboardSpecial(key, x, y)

    def keyboardSpecialUp(self, key, x, y):
        for k, obj in self.objects.iteritems():
            obj.keyboardSpecialUp(key, x, y)
        
    def display(self):
        for key, obj in self.objects.iteritems():
            obj.display()

    def update(self, delay):
        for k, obj in self.objects.iteritems():
            obj.update(delay)