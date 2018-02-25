# Mine Quest Mini Game
# Created by: Janine Baranski
# Dated: 6-11-15
# Updated to pygame: 7-7-15

# Can only gather resources if you win. Each "mine" is a resource asked for.

import pygame, random, sys, GraphicClass
from pygame.locals import *

class ResourceArea(object):
    """This class sets up resource maps"""
    def __init__(self, resourceName, areaName, width, resourceimage, resourceimage2, graphic):
        self.resource = resourceName
        self.area = areaName
        self.width = width
        self.height = 13
        self.resourceImage = resourceimage # set up images
        self.resourceImage2 = resourceimage2
        self.graphic = graphic
        self.resources = []
        self.visible = []
        self.count = []
        self.rGuess = []     # resource guess
        self.rowTuple = []
        self.columnLabel = [" "," A ", " B ", " C ", " D ", " E ", " F ", " G ", " H ", " I ", " J ", " K ", " L ", " M "]
        self.rowLine = ["  ", "1","2","3","4","5","6","7","8","9","10","11","12","13"]
        self.FPS = 40
        self.letters = []
        self.rows = []
        self.printSq = []
        self.windowSurface = pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
        self.introSound = pygame.mixer.Sound('intro.wav')
        #self.flagImage = pygame.image.load('flag.png') # set up images
        #self.zeroImage = pygame.image.load('zero.png') # set up images
        
    def Intro(self):
        # text, font, color, window, (x, y)
        self.graphic.drawText('Resource Search', self.graphic.basicFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 120, (self.graphic.WINDOWHEIGHT) - 560)
        self.graphic.drawText('Press a key to start.', self.graphic.basicFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 120, (self.graphic.WINDOWHEIGHT) - 520)
        self.graphic.drawText("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 480)
        self.graphic.drawText("Welcome to the %s!" % self.area, self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 40, (self.graphic.WINDOWHEIGHT) - 440)
        self.graphic.drawText("This area is %d by %d." % (self.width, self.height), self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 40, (self.graphic.WINDOWHEIGHT) - 400)
        self.graphic.drawText("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 360)
        self.graphic.drawText("The %s is covered in debris!" % self.area, self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 320)
        self.graphic.drawText("You have to clear each square to see what is there.", self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 280)
        self.graphic.drawText("Please mark all %s before gathering." % self.resource, self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 240)
        self.graphic.drawText("If you clear an area with %s you waste it and you" % self.resource, self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 200)
        self.graphic.drawText("must come back and start again in a new area of %s." %self.area, self.graphic.smallerFont, self.graphic.BLUE, self.graphic.windowSurface, (self.graphic.WINDOWWIDTH / 2) - 175, (self.graphic.WINDOWHEIGHT) - 160)
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()

    def setBoard(self):
        cnt = 0
        while cnt < self.width:
            self.rowTuple.append(False)
            cnt += 1
        
        cnt = 0
        while cnt < self.height:
            self.resources.append(self.rowTuple[:])
            cnt += 1
        
        cnt = 0
        while cnt < self.height:
            self.visible.append(self.rowTuple[:])
            cnt += 1

        cnt = 0
        while cnt < self.height:
            self.count.append(self.rowTuple[:])
            cnt += 1

        cnt = 0
        while cnt < self.height:
            self.rGuess.append(self.rowTuple[:])
            cnt += 1

        rowSq = []
        cnt = 0
        while cnt < self.width:
            rowSq.append({'rect':pygame.Rect(0, 0, 0, 0)})
            cnt += 1
        
        cnt = 0
        while cnt < self.height:
            #self.printSq.append([{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)},{'rect':pygame.Rect(0, 0, 0, 0)}])
            self.printSq.append(rowSq[:])
            cnt += 1
        
        # left, top, width, height
        rwInc = 0
        #range(stop). Starts at zero.
        for r in range(self.height):
            colInc = 0
            for c in range(self.width):
                self.printSq[r][c] = {'rect':(40 + colInc, 40 + rwInc, 40, 40)}
                colInc += 40
            rwInc += 40
            
        #Refreshes the screen from the intro
        self.windowSurface = pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
        pygame.display.update()

    def setMines(self):
        #Generate Resource Randomly in each row.
        cnt = 0
        while cnt < self.width:
            c = random.randint(0, (self.width - 1))
            r = random.randint(0, (self.height - 1))
            if self.resources[r][c] == False:
                self.resources[r][c] = True
                cnt += 1

    def isOnBoard(self, x, y):
         # Returns True if the coordinates are located on the board.
         return (x >= 0) and (x < (self.height)) and (y >= 0) and (y < (self.width))

    def setMineCount(self):
        #Generate Mine Count
        rCount = 0

        # Only execute if within range
        for r in range(self.height):
            for c in range(self.width):
                for x, y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    if self.isOnBoard(r + x, c + y):
                        if self.resources[r + x][c + y]:
                            rCount += 1
                self.count[r][c] = rCount
                rCount = 0

        for r in range(self.height):
            for c in range(self.width):
                if self.resources[r][c] == True:
                    self.count[r][c] = 10
                    
    def __printColumnLabel(self):
       # Prints column Letters
        for cnt in self.letters[:(self.width + 1)]:
            self.windowSurface.blit(cnt['text'], cnt['rect'])
        
    def __printRowLine(self):
        # Prints row numbers
        for rw in self.rows[:(self.height + 1)]:
            self.windowSurface.blit(rw['text'], rw['rect'])

    def __printCharacter(self, c, r, char):
        pygame.draw.rect(self.windowSurface, self.graphic.WHITE, self.printSq[r][c]['rect'], 1)
        self.windowSurface.blit(pygame.transform.scale(char, (40, 40)), self.printSq[r][c]['rect'])
        #self.__printRowLine()

    def chooseSquare(self):
        #Choose Square to Reveal
        mine = False
        message = ' '
        result = 0
        guess = ' '
        mine, message, result = self.printBoard()
        while mine == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()

                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        for pos1, rw in enumerate(self.printSq):
                            for pos2, col in enumerate(rw):
                                if pygame.Rect(col['rect']).contains(click):
                                    if self.visible[pos1][pos2]:
                                        self.showAdjacentNumbers(pos1, pos2)
                                    else:
                                        self.visible[pos1][pos2] = True
                                        self.showAdjacentZeros(pos1, pos2)   
                    elif event.button == 3:
                        for pos1, rw in enumerate(self.printSq):
                            for pos2, col in enumerate(rw):
                                if pygame.Rect(col['rect']).contains(click):
                                    if self.rGuess[pos1][pos2] == False:
                                        self.rGuess[pos1][pos2] = True
                                        self.visible[pos1][pos2] = True
                                    elif self.rGuess[pos1][pos2] == True:
                                        self.rGuess[pos1][pos2] = False
                                        self.visible[pos1][pos2] = False
                    mine, message, result = self.printBoard()

        self.graphic.drawText("You %s" % message, self.graphic.basicFont, self.graphic.BLUE, self.windowSurface, 0, 0)
        return result

    def showAdjacentZeros(self, row, column):
        adjacent = []
        cnt = 0
        flag = False
        #Fills list with false. Can't use for loop because its empty
        while cnt < self.height:
            adjacent.append(self.rowTuple[:])
            cnt += 1 

        adjacent[row][column] = True
        #Checks adjacent cells for zero. Then marks them as adjacent.
        #Have to check the adjacent cells for their adjacent zeros next.
        if adjacent[row][column] == True and self.count[row][column] == 0:
            for x, y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                if self.isOnBoard(row + x, column + y):
                    adjacent[row + x][column + y] = True
                    self.visible[row + x][column + y] = True

        #Loop to keep checking newly found adjacent 0's. Breaks loop if no new adjacents.
        while flag == False:
            flag = True        
            
            #Check adjacent[] True cells for adjacent #'s, reset change flag to false when nearby cells still need to be revealed
            for r in range(self.height):
                for c in range(self.width):
                    if adjacent[r][c] == True and self.count[r][c] == 0:
                        for x, y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                            if self.isOnBoard(r + x, c + y):
                                if adjacent[r + x][c + y] == False:
                                    adjacent[r + x][c + y] = True
                                    self.visible[r + x][c + y] = True
                                    flag = False

    def showAdjacentNumbers(self, row, column):
        adjacent = []
        cnt = 0
        flag = False
        #Fills list with false. Can't use for loop if list is empty
        while cnt < self.height:
            adjacent.append(self.rowTuple[:])
            cnt += 1 

        #Checks adjacent cells for mine. Then marks them as adjacent.
        #Have to check the adjacent cells for their adjacent zeros next.
        for x, y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            if self.isOnBoard(row + x, column + y) and (self.resources[row + x][column + y] and self.rGuess[row + x][column + y] == False):
                flag = True
        if flag == False:
            for x, y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                if self.isOnBoard(row + x, column + y):
                    self.visible[row + x][column + y] = True
                    self.showAdjacentZeros(row + x, column + y)
                                      
    def printBoard(self):
        #Print Game Board Reveal
        correctCount = 0
        mine = False
        message = ' '
        result = 0
        for r in range(self.height):
            for c in range(self.width):

                #Output for choosing a resouce square
                if self.resources[r][c] == True and self.rGuess[r][c] == True:
                    correctCount += 1
                    if correctCount == self.width:
                        mine = True
                        message = "found all the " + self.resource + "!"
                        result = correctCount
                elif self.resources[r][c] == True and self.rGuess[r][c] == False and self.visible[r][c] == True:
                    mine = True
                    message = "destroyed the " + str(self.resource) + "!"
                    result = 0

                # What board displays
                if self.visible[r][c] == True:
                    if self.rGuess[r][c] == True:
                        #Adds a flag
                        if mine == False:
                            self.__printCharacter(c, r, self.graphic.flagImage)
                        elif mine == True:
                            self.__printCharacter(c, r, self.resourceImage)
                    elif self.rGuess[r][c] == False:
                        #Reveals X for mine
                        if self.resources[r][c] == True:
                            self.__printCharacter(c, r, self.resourceImage2)
                        #Reveal mine count
                        elif self.resources[r][c] == False:
                            if self.count[r][c] != 0:
                                self.__printCharacter(c, r, self.rows[self.count[r][c]]['text'])
                            #Reveal * for 0's
                            elif self.count[r][c] == 0:
                                self.__printCharacter(c, r, self.graphic.zeroImage)
                elif self.visible[r][c] == False:
                    #Prints blanks
                    self.__printCharacter(c, r, self.graphic.blankImage)

        pygame.display.update()
        return mine, message, result

    def printBoardAnswers(self):
        #Print Game Board Reveal
        correctCount = 0
        mine = False
        message = ' '
        result = 0
        #self.__printColumnLabel()
        #self.__printRowLine()
        for r in range(self.height):
            for c in range(self.width):
                if self.rGuess[r][c] == True:
                    #Adds a flag
                    self.__printCharacter(c, r, self.graphic.flagImage)
                elif self.rGuess[r][c] == False:
                    #Reveals X for mine
                    if self.resources[r][c] == True:
                        self.__printCharacter(c, r, self.resourceImage)
                    #Reveal mine count
                    elif self.resources[r][c] == False:
                        if self.count[r][c] != 0:
                            self.__printCharacter(c, r, self.rows[self.count[r][c]]['text'])
                        #Reveal * for 0's
                        elif self.count[r][c] == 0:
                            self.__printCharacter(c, r, self.graphic.zeroImage)

                #Output for choosing a resouce square
                if self.resources[r][c] == True and self.rGuess[r][c] == True:
                    correctCount += 1
                    if correctCount == self.width:
                        mine = True
                        message = "found all the " + self.resource + "!"
                        result = correctCount
                elif self.resources[r][c] == True and self.rGuess[r][c] == False and self.visible[r][c] == True:
                    mine = True
                    message = "lose!"
                    result = 0

        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()

    def setUp(self):
        
        # set up window
        self.windowSurface = pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption("Resource Search")
        pygame.mouse.set_visible(True)

        # Set up lists of dictionaries
        # left, top, width, height
        l1 = {'rect':pygame.Rect(0, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[0], True, self.graphic.WHITE, self.graphic.BLACK)}
        l2 = {'rect':pygame.Rect(40, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[1], True, self.graphic.WHITE, self.graphic.BLACK)}
        l3 = {'rect':pygame.Rect(80, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[2], True, self.graphic.WHITE, self.graphic.BLACK)}
        l4 = {'rect':pygame.Rect(120, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[3], True, self.graphic.WHITE, self.graphic.BLACK)}
        l5 = {'rect':pygame.Rect(160, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[4], True, self.graphic.WHITE, self.graphic.BLACK)}
        l6 = {'rect':pygame.Rect(200, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[5], True, self.graphic.WHITE, self.graphic.BLACK)}
        l7 = {'rect':pygame.Rect(240, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[6], True, self.graphic.WHITE, self.graphic.BLACK)}
        l8 = {'rect':pygame.Rect(280, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[7], True, self.graphic.WHITE, self.graphic.BLACK)}
        l9 = {'rect':pygame.Rect(320, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[8], True, self.graphic.WHITE, self.graphic.BLACK)}
        l10 = {'rect':pygame.Rect(360, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[9], True, self.graphic.WHITE, self.graphic.BLACK)}
        l11 = {'rect':pygame.Rect(400, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[10], True, self.graphic.WHITE, self.graphic.BLACK)}
        l12 = {'rect':pygame.Rect(400, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[11], True, self.graphic.WHITE, self.graphic.BLACK)}
        l13 = {'rect':pygame.Rect(400, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[12], True, self.graphic.WHITE, self.graphic.BLACK)}
        l14 = {'rect':pygame.Rect(400, 0, 40, 40), 'text':self.graphic.basicFont.render(self.columnLabel[13], True, self.graphic.WHITE, self.graphic.BLACK)}

        self.letters = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14]

        r1 = {'rect':pygame.Rect(0, 0, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[0], True, self.graphic.WHITE, self.graphic.BLACK)}
        r2 = {'rect':pygame.Rect(0, 40, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[1], True, self.graphic.WHITE, self.graphic.BLACK)}
        r3 = {'rect':pygame.Rect(0, 80, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[2], True, self.graphic.WHITE, self.graphic.BLACK)}
        r4 = {'rect':pygame.Rect(0, 120, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[3], True, self.graphic.WHITE, self.graphic.BLACK)}
        r5 = {'rect':pygame.Rect(0, 160, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[4], True, self.graphic.WHITE, self.graphic.BLACK)}
        r6 = {'rect':pygame.Rect(0, 200, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[5], True, self.graphic.WHITE, self.graphic.BLACK)}
        r7 = {'rect':pygame.Rect(0, 240, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[6], True, self.graphic.WHITE, self.graphic.BLACK)}
        r8 = {'rect':pygame.Rect(0, 280, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[7], True, self.graphic.WHITE, self.graphic.BLACK)}
        r9 = {'rect':pygame.Rect(0, 320, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[8], True, self.graphic.WHITE, self.graphic.BLACK)}
        r10 = {'rect':pygame.Rect(0, 360, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[9], True, self.graphic.WHITE, self.graphic.BLACK)}
        r11 = {'rect':pygame.Rect(0, 400, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[10], True, self.graphic.WHITE, self.graphic.BLACK)}
        r12 = {'rect':pygame.Rect(0, 440, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[11], True, self.graphic.WHITE, self.graphic.BLACK)}
        r13 = {'rect':pygame.Rect(0, 480, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[12], True, self.graphic.WHITE, self.graphic.BLACK)}
        r14 = {'rect':pygame.Rect(0, 520, 40, 40), 'text':self.graphic.basicFont.render(self.rowLine[13], True, self.graphic.WHITE, self.graphic.BLACK)}

        self.rows = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14]

    def refreshVariables(self):
        self.resources = []
        self.visible = []
        self.count = []
        self.rGuess = []    
              
def main():
    # set up pygame, the window, and the mouse cursor
    pygame.init()
    graphic = GraphicClass.Graphics()
    game = ResourceArea("oak", "forest", 28, pygame.image.load("Oak.png"),  pygame.image.load("Oak2.png"), graphic)
    
    while True:
        # set up sounds
        game.introSound.play()
        game.setUp()

        # show the "Start" screen
        game.Intro()
        
        # Set up the start of the game
        game.setBoard()
        game.setMines()
        game.setMineCount()
        game.printBoardAnswers()
        finalResult = game.chooseSquare()
        game.refreshVariables()
        graphic.waitForPlayerToPressKey()

if __name__ == "__main__":
    main()
