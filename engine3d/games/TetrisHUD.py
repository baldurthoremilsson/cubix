import sys
reload(sys) 
sys.setdefaultencoding('iso-8859-1') 
from Image import *
from GameObject import *
from Textures import *
from TetrisGrid import *
from random import *
from TetrisCube import *
from TextureString import *
from Cube import *

class TetrisHUD(GameObject):
    
    def __init__(self, Tetris3d):
        self.Tetris3d = Tetris3d
        self.data = Tetris3d.data
        self.time = glutGet(GLUT_ELAPSED_TIME)
        self.state = 'mainMenu'
        self.menuitem = 'start'
        self.texture = Textures()
        self.tstring = TextureString(Tetris3d.data)
        self.playername = ''
        
        self.planes = {}
        self.skins = {}
        self.stringPlane = {}
        
        self.textureWidthRatio = 512.0 / 640.0
        self.textureHeightRatio = 512.0 / 480.0
        
        self.generateStringTexture('mainMenu')
        self.generateStringTexture('gameoverMenu')
        self.generateStringTexture('enterName')
        self.generateStringTexture('pause')
        self.generateStringTexture('play')
        self.generateStringTexture('highscore')
        
        self.backgroundTexture = self.texture.createTex(self.data.get('texture/menu/menu.jpg'))
        self.stringTexture = self.texture.createTex(self.stringPlane['mainMenu'])
        
        self.planes['0_background'] = {'texture': self.backgroundTexture, 'coord': [16.7, 12.525, 16.6]}
        self.planes['1_strings'] = {'texture': self.stringTexture, 'coord': [16.7, 12.525, 16.59]}
        
        self.cubePos = {'mainMenu':     { 'start': [4,4.6,0],    'highscore': [10,0.2,0], 'exit': [3,-4,0] },
                        'gameoverMenu': { 'start': [10.5,2.4,0], 'highscore': [10,-2,0],  'exit': [3,-6.2,0] }}
        self.cube = TetrisCube(1, self.cubePos[self.state][self.menuitem])
    
    def generateStringTexture(self, name):
        if self.stringPlane.has_key(name):
            del self.stringPlane[name]
        if name == 'mainMenu':
            self.registerString('mainMenu', self.tstring.create('Cubix'), 320, 20, 'center', 1)
            self.registerString('mainMenu', self.tstring.create('Start'), 320, 145, 'center', 0.8)
            self.registerString('mainMenu', self.tstring.create('Highscores'), 320, 215, 'center', 0.8)
            self.registerString('mainMenu', self.tstring.create('Exit'), 320, 290, 'center', 0.8)
        
        elif name == 'gameoverMenu':
            self.registerString('gameoverMenu', self.tstring.create('Game Over'), 320, 20, 'center', 1)
            self.registerString('gameoverMenu', self.tstring.create('Your Score: ' + str(self.Tetris3d.objects['mainGrid'].score.value)), 320, 120, 'center', 0.35)
            self.registerString('gameoverMenu', self.tstring.create('Try Again!'), 320, 180, 'center', 0.8)
            self.registerString('gameoverMenu', self.tstring.create('Highscores'), 320, 250, 'center', 0.8)
            self.registerString('gameoverMenu', self.tstring.create('Exit'), 320, 320, 'center', 0.8)
        
        elif name == 'enterName':
            self.registerString('enterName', self.tstring.create('Game Over'), 320, 20, 'center', 1)
            self.registerString('enterName', self.tstring.create('Enter Your Name:'), 320, 120, 'center', 0.4)
            self.registerString('enterName', self.tstring.create(self.playername), 320, 215, 'center', 0.5)
        
        elif name == 'pause':
            self.registerString('pause', self.tstring.create('Pause'), 320, 180, 'center', 1)
        
        elif name == 'highscore' or name == 'highscoreHighlight':
            if name == 'highscoreHighlight' and self.stringPlane.has_key('highscore'):
                del self.stringPlane['highscore']
            self.registerString('highscore', self.tstring.create('Highscores'), 320, 20, 'center', 1)
            self.registerString('highscore', self.tstring.create('Press escape to go back to menu'), 320, 110, 'center', 0.32)
            id = self.Tetris3d.objects['mainGrid'].db.getNewestId()
            extraSpace = 0
            i = 1
            for score in self.Tetris3d.objects['mainGrid'].db.getToTen():
                if score[2] == id and name == 'highscoreHighlight':
                    size = 0.5
                else:
                    size = 0.35
                
                nameString = self.tstring.create(score[0])
                scoreString = self.tstring.create(str(score[1]))
                
                # To prevent that the name and score overlap each other in the list
                if  int((nameString.size[0] + scoreString.size[0]) * size) > 540:
                    ratio = 540.0 / ((nameString.size[0] + scoreString.size[0]) * size)
                    size *= ratio
                
                self.registerString('highscore', nameString, 50, 120 + 30 * i + extraSpace, 'left', size)
                self.registerString('highscore', scoreString, 590, 120 + 30 * i + extraSpace, 'right', size)
                if score[2] == id and name == 'highscoreHighlight':
                    extraSpace = 8
                i += 1
        
        elif name == 'play':
            self.registerString('play', self.tstring.create('Cubix'), 320, 30, 'left', 1) 
            self.registerString('play', self.tstring.create('Score:'), 320, 365, 'left', 0.33)
            self.registerString('play', self.tstring.create('Level:'), 320, 423, 'left', 0.33)
    
    def registerString(self, skin, image, x, y, align, size):
        x = int(x * self.textureWidthRatio)
        y = int(y * self.textureHeightRatio)
        
        if not self.stringPlane.has_key(skin):
            self.stringPlane[skin] = new('RGBA', (512, 512))
        
        width  = int(image.size[0] * size * self.textureWidthRatio)
        height = int(image.size[1] * size * self.textureHeightRatio)
        image = image.resize((width, height), ANTIALIAS)
        
        
        posY = y
        if align == 'left':
            posX = x
        elif align == 'right':
            posX = x - width
        elif align == 'center':
            posX = x - (width / 2)
        else:
            posX = 0
        
        self.stringPlane[skin].paste(image, (posX, posY))
    
    def setState(self, state):
        if state == 'mainMenu':
            self.state = 'mainMenu'
            self.texture.createTex(self.stringPlane['mainMenu'], self.stringTexture)
            self.menuitem = 'start'
            self.cube.renderPos = self.cubePos[self.state][self.menuitem]
        elif state == 'gameoverMenu':
            self.state = 'gameoverMenu'
            self.generateStringTexture('gameoverMenu')
            self.texture.createTex(self.data.get('texture/menu/menu.jpg'), self.backgroundTexture)
            self.texture.createTex(self.stringPlane['gameoverMenu'], self.stringTexture)
            self.menuitem = 'start'
            self.cube.renderPos = self.cubePos[self.state][self.menuitem]
        elif state == 'play':
            self.state = 'play'
            self.Tetris3d.objects['mainGrid'].run = True
            self.texture.createTex(self.data.get('texture/menu/front.jpg'), self.backgroundTexture)
            self.texture.createTex(self.stringPlane['play'], self.stringTexture)
            if self.Tetris3d.objects['mainGrid'].gameover:
                self.Tetris3d.objects['mainGrid'].gameover = 0
                self.Tetris3d.objects['mainGrid'].clearGrid()
        elif state == 'pause':
            self.state = 'pause'
            self.Tetris3d.objects['mainGrid'].run = None
            self.texture.createTex(self.data.get('texture/menu/menu.jpg'), self.backgroundTexture)
            self.texture.createTex(self.stringPlane['pause'], self.stringTexture)
        elif state == 'highscore':
            if self.state == 'enterName':
                self.generateStringTexture('highscoreHighlight')
            else:
                self.generateStringTexture('highscore')
            self.state = 'highscore'
            self.texture.createTex(self.data.get('texture/menu/highscore.jpg'), self.backgroundTexture)
            self.texture.createTex(self.stringPlane['highscore'], self.stringTexture)
        elif state == 'enterName':
            self.state = 'enterName'
            self.generateStringTexture('enterName')
            self.texture.createTex(self.data.get('texture/menu/menu.jpg'), self.backgroundTexture)
            self.texture.createTex(self.stringPlane['enterName'], self.stringTexture)
    
    def keyboardSpecial(self, key, x, y):
        if self.state == 'mainMenu' or self.state == 'gameoverMenu':
            if key == 101: # up arrow key
                if self.menuitem == 'start':        self.menuitem = 'exit'
                elif self.menuitem == 'exit':       self.menuitem = 'highscore'
                elif self.menuitem == 'highscore':  self.menuitem = 'start'
            elif key == 103: # down arrow key
                if self.menuitem == 'start':        self.menuitem = 'highscore'
                elif self.menuitem == 'highscore':  self.menuitem = 'exit'
                elif self.menuitem == 'exit':       self.menuitem = 'start'
            self.cube.renderPos = self.cubePos[self.state][self.menuitem]
    
    def keyboard(self, key, x, y):
        if self.state == 'mainMenu' or self.state == 'gameoverMenu':
            if ord(key) == 27: # key = esc
                sys.exit()
            if ord(key) == 13: # key = enter
                if self.menuitem == 'start':
                    self.setState('play')
                elif self.menuitem == 'highscore':
                    self.setState('highscore')
                elif self.menuitem == 'exit':
                    sys.exit()
        elif self.state == 'highscore':
            if ord(key) == 27: # key = esc
                self.setState('mainMenu')
        elif self.state == 'enterName':
            if self.tstring.data.has_key(key) and len(self.playername) < 13:
                self.playername += key
            elif ord(key) == 8: # key = backspace
                self.playername = self.playername[:-1]
            self.generateStringTexture('enterName')
            self.texture.createTex(self.stringPlane['enterName'], self.stringTexture)
            if ord(key) == 13 and len(self.playername) != 0: # key = enter
                self.Tetris3d.objects['mainGrid'].db.addScore(unicode(self.playername), self.Tetris3d.objects['mainGrid'].score.getValue())
                self.setState('highscore')
            elif ord(key) == 27: # key = esc
                self.setState('mainMenu')
        elif self.state == 'pause':
            if key == 'p':
                self.setState('play')
            if ord(key) == 27: # key = esc
                self.Tetris3d.objects['mainGrid'].gameOver()
        elif self.state == 'play':
            if key == 'p':
                self.setState('pause')
            if ord(key) == 27: # key = esc
                self.Tetris3d.objects['mainGrid'].gameOver()
    
    def display(self):
        for name, plane in self.planes.iteritems():
            x = plane['coord'][0]
            y = plane['coord'][1]
            z = plane['coord'][2]
            glEnable (GL_BLEND)
            glBlendFunc (GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, plane['texture'])
            glBegin(GL_QUADS)
            glTexCoord2f(1.0, 0.0); glVertex3f(-x, -y,  z)    # Bottom Right
            glTexCoord2f(0.0, 0.0); glVertex3f( x, -y,  z)    # Bottom Left
            glTexCoord2f(0.0, 1.0); glVertex3f( x,  y,  z)    # Top Left
            glTexCoord2f(1.0, 1.0); glVertex3f(-x,  y,  z)    # Top Right
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)
        
        if self.state == 'mainMenu' or self.state == 'gameoverMenu':
            glPushMatrix()
            glScaled(0.2,0.2,0.2)
            glTranslated(0,0,-0.2)
            self.cube.display()
            glPopMatrix()
    
    def update(self, delay):
        if self.time + 1000 < glutGet(GLUT_ELAPSED_TIME) and (self.state == 'mainMenu' or self.state == 'gameoverMenu'):
            new = randrange(0,6)
            if new >= self.cube.type:
                self.cube.setType(new + 1)
            else:
                self.cube.setType(new)
            if self.cube.type == 0:
                for pos in self.cube.position:
                    pos[0] += 0.5
            elif self.cube.type == 2:
                for pos in self.cube.position:
                    pos[1] += 0.5
            elif self.cube.type == 3 or self.cube.type == 4:
                for pos in self.cube.position:
                    pos[0] -= 0.5
            elif self.cube.type == 5 or self.cube.type == 6:
                for pos in self.cube.position:
                    pos[1] -= 0.5
            self.time = glutGet(GLUT_ELAPSED_TIME)