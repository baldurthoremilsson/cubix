from GameObject import *
from Cube import *
from TetrisCube import *
from random import *
from TetrisDB import *
from TetrisNum import *
from TetrisNextCube import *
import types
import time

class TetrisGrid(GameObject):
    
    def __init__(self, Tetris3d, width, height):
        self.Tetris3d = Tetris3d
        self.grid = []
        self.tempGrid = []
        self.width = width
        self.height = height
        self.run = None
        self.gameover = 0
        self.dropTime = 500
        self.db = TetrisDB('score.db')
        self.keyDown = { 'key': None, 'time': None }
        self.initKeyEvent = None    
        self.score = TetrisNum(-15,-16.53,0)
        self.level = TetrisNum(-15,-19.34,0)
        
        for row in range(self.height):
            self.grid.append(self.getEmptyRow())
        
        for row in range(self.height):
            temp = []
            for column in range(self.width):
                temp.append(Cube(1, [1,1,1]))
            self.tempGrid.append(temp)
        
        self.tCube = TetrisCube(randrange(0,7), [2.55, 10.5, 16])
        self.helperCube = TetrisCube(self.tCube.type, [2.55, 10.5, 16])
        self.updateHelperCube()
        for color in self.helperCube.colors:
            color[0] = 0.2
            color[1] = 0.2
            color[2] = 0.2
        self.cubeTime = glutGet(GLUT_ELAPSED_TIME)
        self.completeRows = []
        self.tempRows = None
        self.nextCube = TetrisNextCube(randrange(0,7), [-13.45, 3.5, 16])
        self.blinkTime = 0
        self.cheatChangeCube = None
        self.cheatHelperCube = None
        try:
            open('slidecheat')
            self.cheatSlideCube = True
        except:
            self.cheatSlideCube = None
        self.blinkCount = 0
        
        for row in range(self.height):
            self.completeRows.append(True)
        
        self.level.value = 1

    def update(self, delay):
        if self.run:
            self.keyEvents()
            self.stickCube()
            self.completeRow()
            self.updateGrid()
            self.updateHelperCube()
    
    def display(self):
        if self.run == True:
            rowPos = 0
            for row in self.grid:
                colPos = 0
                for cube in row:
                    if cube:
                        glPushMatrix()
                        glTranslated(2.55, 10.5, 0)
                        glTranslated((self.width - colPos - 1) * 1.1, -rowPos * 1.1, 16)
                        cube.display()
                        glPopMatrix()
                    colPos += 1
                rowPos += 1
            if type(self.tCube) == types.InstanceType:
                self.tCube.display()
                if self.cheatHelperCube:
                    self.helperCube.display()
            self.score.display()
            self.level.display()
            self.nextCube.display()
    
    def getEmptyRow(self):
        row = []
        for col in range(self.width):
            row.append(None)
        return row
    
    def clearGrid(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = None
        self.score.value = 0
        self.level.value = 1
        self.nextCube.setType(randrange(0,7))
        self.tCube.setType(randrange(0,7))
        self.dropTime = 500
    
    def keyboard(self, key, x, y):
        if self.run:
            if ord(key) == 32 and type(self.tCube) == types.InstanceType: # spacebar
                while not self.checkCollision():
                    self.moveVert(1)
                if self.cheatSlideCube == True:
                    self.cubeTime = glutGet(GLUT_ELAPSED_TIME)
                else:
                    self.cubeTime -= self.dropTime
            if ord(key) > ord('0') and ord(key) < ord('8') and self.cheatChangeCube == True and type(self.tCube) == types.InstanceType:
                self.tCube.setType(ord(key) - ord('8'))
    
    def keyboardSpecial(self, key, x, y):
        if self.run:
            # cube thingy
            if key == 100: # left arrow key
                self.moveHoriz(1)
                self.initKeyEvent = True
                self.keyDown['key'] = 'left'
                self.keyDown['time'] = glutGet(GLUT_ELAPSED_TIME)
            if key == 102: # right arrow key
                self.moveHoriz(-1)
                self.initKeyEvent = True
                self.keyDown['key'] = 'right'
                self.keyDown['time'] = glutGet(GLUT_ELAPSED_TIME)
            if key == 103: # down arrow key
                self.moveVert(1)
                self.initKeyEvent = True
                self.keyDown['key'] = 'down'
                self.keyDown['time'] = glutGet(GLUT_ELAPSED_TIME)
            if key == 101: # up arrow key
                self.rotate()
                self.initKeyEvent = True
                self.keyDown['key'] = 'up'
                self.keyDown['time'] = glutGet(GLUT_ELAPSED_TIME)
            #cube thingy
    
    def keyboardSpecialUp(self, key, x, y):
        if self.run:
            if key == 100 and self.keyDown['key'] == 'left': # left arrow key
                self.keyDown['key'] = None
                self.keyDown['time'] = None
            if key == 102 and self.keyDown['key'] == 'right': # right arrow key
                self.keyDown['key'] = None
                self.keyDown['time'] = None
            if key == 103 and self.keyDown['key'] == 'down': # down arrow key
                self.keyDown['key'] = None
                self.keyDown['time'] = None
            if key == 101 and self.keyDown['key'] == 'up': # up arrow key
                self.keyDown['key'] = None
                self.keyDown['time'] = None
    
    def keyEvents(self):
        if self.keyDown['key'] != None:
            key = self.keyDown['key']
            time = self.keyDown['time']
            
            if self.initKeyEvent == True:
                halt = 140
            else:
                halt = 35
            if time + halt < glutGet(GLUT_ELAPSED_TIME):
                if key == 'left':
                    self.moveHoriz(1)
                elif key == 'right':
                    self.moveHoriz(-1)
                elif key == 'down':
                    self.moveVert(1)
                elif key == 'up':
                    self.rotate()
                self.initKeyEvent = None
                self.keyDown['time'] = glutGet(GLUT_ELAPSED_TIME)
    
    def stickCube(self):
        if self.cubeTime + self.dropTime < glutGet(GLUT_ELAPSED_TIME) and type(self.tCube) == types.InstanceType:
            if self.checkCollision():
                if self.tCube.position[0][0] == 0 and self.tCube.position[0][1] == self.tCube.types[self.tCube.type][0][1]:
                    self.gameOver()
                for row, col in self.tCube.position:
                    self.grid[row][self.width - 1 - col] = Cube(1, self.tCube.getColor())
                self.tCube = None
    
    def checkCollision(self, cube = None):
        if cube == None: cube = self.tCube
        for row, col in cube.position:
            if (row + 1 >= self.height) or (self.grid[row + 1][self.width - 1 - col]):
                return True
        return None

    def completeRow(self):
        if self.tCube == None:
            for rowNumber in range(20):
                self.completeRows[rowNumber] = True
            rowNumber = 0
            for row in self.grid:
                if row.count(None) > 0:
                    self.completeRows[rowNumber] = None
                rowNumber += 1
            if self.completeRows.count(True) > 0:
                self.tCube = 'blinkrows'
                self.blinkCount = 6
    
    def updateGrid(self):
        if type(self.tCube) == types.InstanceType:
            if self.cubeTime + self.dropTime < glutGet(GLUT_ELAPSED_TIME):
                self.moveVert(1)
                self.cubeTime = glutGet(GLUT_ELAPSED_TIME)
        
        elif self.tCube == None:
            self.tCube = TetrisCube(self.nextCube.cube.type, [2.55, 10.5, 16])
            self.nextCube.setType(randrange(0,7))
            self.cubeTime = glutGet(GLUT_ELAPSED_TIME)
        
        elif self.tCube == 'blinkrows':
            if self.blinkCount > 0:
                if self.blinkTime + (self.dropTime / 8) < glutGet(GLUT_ELAPSED_TIME):
                    rowNum = 0
                    for rowStatus in self.completeRows:
                        if rowStatus == True:
                            tempRow = self.grid[rowNum]
                            self.grid[rowNum] = self.tempGrid[rowNum]
                            self.tempGrid[rowNum] = tempRow
                        rowNum += 1
                    self.blinkCount -= 1
                    self.blinkTime = glutGet(GLUT_ELAPSED_TIME)
            else:
                if self.cheatHelperCube: addScore = 4
                else: addScore = 5
                rowNum = 0
                for rowStatus in self.completeRows:
                    if rowStatus == True:
                        self.grid.pop(rowNum)
                        self.grid.insert(0, self.getEmptyRow())
                        addScore *= 2
                    rowNum += 1
                if self.isGridEmpty() == True:
                    addScore *= 2
                self.addScore(addScore)
                self.tCube = None
    
    def updateHelperCube(self):
        if type(self.tCube) != types.InstanceType:
            return
        update = None
        cube = 0
        for pos in self.helperCube.position:
            if pos[1] != self.tCube.position[cube][1]:
                update = True
            elif pos[0] == self.tCube.position[cube][0] and pos[1] == self.tCube.position[cube][1]:
                update = True
            cube += 1
        if self.helperCube.type != self.tCube.type:
            update = True
        if update:
            self.helperCube.setType(self.tCube.type)
            for cube in range(len(self.helperCube.position)):
                self.helperCube.position[cube][0] = self.tCube.position[cube][0]
                self.helperCube.position[cube][1] = self.tCube.position[cube][1]
            drop = True
            while drop:
                if self.checkCollision(self.helperCube):
                    drop = None
                else:
                    for pos in self.helperCube.position:
                        pos[0] += 1
    
    def isGridEmpty(self):
        if self.grid[self.height - 1].count(None) == self.width:
            return True
        else:
            return None
    
    def gameOver(self):
        scores = self.db.getToTen()
        self.run = None
        self.gameover = 1
        if (len(scores) == 10 and self.score.getValue() < scores[9][1]) or (self.score.getValue() == 0):
            self.Tetris3d.objects['TetrisHUD'].setState('gameoverMenu')
        else:
            self.Tetris3d.objects['TetrisHUD'].setState('enterName')
    
    def addScore(self, score):
        self.score.add(score)
        if self.score.value >= 250 * self.level.value:
            self.level.add(1)
            self.dropTime -= 25
            if self.dropTime < 100:
                self.dropTime = 100
    
    # cube movement
    def moveHoriz(self, length):
        if type(self.tCube) == types.InstanceType:
            move = True
            for row, col in self.tCube.position:
                if (col + length < 0) or (col + length >= self.width):
                    move = None
                elif self.grid[row][self.width - 1 - col - length]:
                    move = None
            #test border
            if move:
                for pos in self.tCube.position:
                    pos[1] += length
    
    def moveVert(self, length):
        if type(self.tCube) == types.InstanceType:
            move = True
            for row, col in self.tCube.position:
                if row + length >= self.height:
                    move = None
                elif self.grid[row + length][self.width - 1 - col]:
                    move = None
            if move:
                for pos in self.tCube.position:
                    pos[0] += length
    
    def rotate(self):
        if type(self.tCube) == types.InstanceType:
            rotate = True
            for row, col in self.tCube.getRotation():
                if (row < -1 or row >= self.height): # top/bottom border test
                    rotate = None
                    break
                if (col < 0 or col >= self.width): # left/right border test
                    rotate = None
                    break
                if row != -1:
                    if self.grid[row][self.width - 1 - col]: # grid test
                        rotate = None
                        break
            if rotate:
                self.tCube.rotate()
    #cube movement
