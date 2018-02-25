# Project 3 - Dragon Slayer 2
# Created by: Janine Baranski
# Dated: 7-7-15
# Gather the necessary tools to slay the dragon.

import pygame, random, time, ResourceQuest2, sys, GraphicClass, VillagerClass
from pygame.locals import * 

class Fighter(object):
    """ This class holds variables and methods common to fighting objects """
    def __init__(self, health, attack, graphic):
        self.health = health
        self.attack = attack
        self.graphic = graphic
        self.allWeapons = [["sword", 10], ["claw", 20], ["teeth", 5], ["fire", 10]]
        self.allProtection = ["shield", 5]

    def updateHealth(self, newHealth):
        self.health = newHealth

    def scoring(self, name):
        num = 3
        if name == "player":
            self.graphic.drawDialog("Player Health: " + str(self.health), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[0][0], 0)
            if self.health <= 0:
                self.graphic.drawDialog("Dragon wins!", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
                self.graphic.waitForPlayerToPressKey()
                num = 0
        elif name == "village":
            self.graphic.drawDialog("Village Health: " + str(self.health), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[0][0] - 45, 0)
            if self.health <= 0:
                self.graphic.drawDialog("The village was destroyed!", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[1][0], self.graphic.centerTextBox[1][1])
                num = 2
        elif name == "dragon":
            self.graphic.drawDialog("Dragon Health: " + str(self.health), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], 0)
            if self.health <= 150 and self.health > 100:
                self.graphic.drawText("Release the bait", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[1][0], self.graphic.centerTextBox[1][1])
            if self.health <= 0:
                self.graphic.drawDialog("Player wins!", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[1][0] - 45, self.graphic.centerTextBox[1][1])
                self.graphic.waitForPlayerToPressKey()
                num = 1
        return num
    
    def attackOther(self, weapon, healthOpponent):
        for pos1, itemSet in enumerate(self.allWeapons):
            for pos2, item in enumerate(itemSet):
                if item == weapon:
                    attack = self.allWeapons[pos1][1]

        healthOpponent -= attack
        attackBlit = self.healthFont.render(str(attack), 1, (255, 0, 0))
        
        return healthOpponent

class Player(Fighter):
    """ This class holds all stats and actions unique to the player """
    def __init__(self, health, attack, graphic, dragon):
        super(Player, self).__init__(health, attack, graphic)
        self.graphic = graphic
        self.name = " "
        self.invPlayer = []
        self.money = 50
        self.dragon = dragon
        self.x, self.y = 1080, 550
        self.playerHeight = 50
        self.playerWidth = 20
        self.playerRect = pygame.Rect(self.x, self.y, self.playerWidth, self.playerHeight)
        self.speed = 7
        self.healthFont = pygame.font.Font(None, 64)
        self.cowRect =  pygame.Rect((self.graphic.WINDOWWIDTH / 2), (self.graphic.WINDOWHEIGHT - self.playerHeight), 100, self.playerHeight)
        self.cowName = "cow"

    def getPlayerInventory(self):
        """ Display inventory """
        inventory = ''
        self.graphic.drawDialogCenter(("%s's wallet: $%d" % (self.name, self.money)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[0][0], self.graphic.centerTextBox[0][1])
        self.graphic.drawDialogCenter(("%s's inventory: " % (self.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[1][0], self.graphic.centerTextBox[1][1])
        for index, item in enumerate(self.invPlayer):
            self.graphic.drawDialogCenter(item, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[index + 2][0], self.graphic.centerTextBox[index + 2][1])

    def validatePlayerInventory(self):
        """ Inventory can only hold 6 items """
        if len(self.invPlayer) <= 6:
            return True
        else:
            return False
         
    def setName(self):
        self.graphic.drawDialog("What is your name? ", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
        pygame.display.update()   
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                if event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        self.name += event.unicode
                        self.graphic.drawDialog(self.name, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
                        pygame.display.update()
                    elif event.key == K_BACKSPACE:
                        self.name = self.name[:-1]
                        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.background, 1)
                        self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.intro, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), self.graphic.background)
                        self.graphic.drawDialog("What is your name? ",self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
                        self.graphic.drawDialog(self.name, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
                        pygame.display.update()
                    elif event.key == K_RETURN:
                        pygame.display.update()
                        return
                    elif event.key == QUIT:
                        return

    def movement(self):        
        # Gather user input    
        keys = pygame.key.get_pressed()
        if not self.playerRect.colliderect(self.dragon.dragonRect):
            if keys[pygame.K_UP]:
                self.y -= self.speed
            elif keys[pygame.K_DOWN]:
                self.y += self.speed    

            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            elif keys[pygame.K_RIGHT]:
                self.x += self.speed

        if self.playerRect.colliderect(self.dragon.dragonRect):

            if self.dragon.awake == False:
                self.graphic.fireballSound.play()
                if "sword" in self.invPlayer:
                    self.dragon.updateHealth(self.attackOther("sword", self.dragon.health))
            else:
                self.graphic.roarSound.play()
                self.updateHealth(self.dragon.attackOther("claw", self.health))
            
            if keys[pygame.K_UP]:
                self.y += 50
            elif keys[pygame.K_DOWN]:
                self.y -= 50

            if keys[pygame.K_LEFT]:
                self.x += 50
            elif keys[pygame.K_RIGHT]:
                self.x -= 50
        
        if self.playerRect.colliderect(self.cowRect):
            self.graphic.splashSound.play()
        
            if keys[pygame.K_UP]:
                self.y -= self.speed
            elif keys[pygame.K_DOWN]:
                self.y += self.speed

            if keys[pygame.K_LEFT]:
                self.x += 50
            elif keys[pygame.K_RIGHT]:
                self.x += self.speed

            if "sleep potion" in self.invPlayer:
                self.invPlayer.remove("sleep potion")
            self.cowName = "cow2"
            
        # Allows jumping
        if self.y >= self.graphic.WINDOWHEIGHT - self.playerHeight:
            self.y = self.graphic.WINDOWHEIGHT - self.playerHeight
        elif self.y <= 0:
            self.y = 0

    def draw(self):
        self.playerRect = pygame.Rect(self.x, self.y, self.playerWidth, self.playerHeight)
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, (self.x, self.y, self.playerWidth, self.playerHeight))
        if "sword" in self.invPlayer and "shield" in self.invPlayer:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.personSwordShield, (self.playerWidth, self.playerHeight)), self.playerRect)
        elif "sleep potion" in self.invPlayer:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.personPotion, (self.playerWidth, self.playerHeight)), self.playerRect)
        elif "sword" in self.invPlayer:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.personSword, (self.playerWidth, self.playerHeight)), self.playerRect)
        else:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.person2, (self.playerWidth, self.playerHeight)), self.playerRect)

    def layBait(self):
        self.graphic.mooSound.play()
        if "cow" in self.invPlayer:
            if "shield" in self.invPlayer:
                self.invPlayer.remove("shield")
        else:
            self.graphic.drawDialog("You have no bait", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])

    def drawBait(self):
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.cowRect)
        if self.cowName == "cow":
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.cow, (self.cowRect[2], self.cowRect[3])), self.cowRect)
        elif self.cowName == "cow2":
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.cow2, (self.cowRect[2], self.cowRect[3])), self.cowRect)

    def getEaten(self):
        Flag = True
        if (self.playerRect.colliderect(self.dragon.dragonRect) == False):
            # When bottoms match up
            if (self.dragon.y + self.dragon.size) < (self.y + self.playerHeight):
                self.dragon.y += 1
                self.dragon.draw()
                Flag = False
                pygame.display.update()
            if (self.dragon.x + self.dragon.size) < (self.x):
                self.dragon.x += 1
                self.dragon.draw()
                Flag = False
                pygame.display.update()
            if (self.dragon.y + self.dragon.size) > (self.y + self.playerHeight):
                self.dragon.y -= 1
                self.dragon.draw()
                Flag = False
                pygame.display.update()
            if (self.dragon.x + self.dragon.size) > (self.x):
                self.dragon.x -= 1
                self.dragon.draw()
                Flag = False
                pygame.display.update()

            if Flag:
                self.health = 0
             
    def playAgain(self):
        """ Refresh Play stats """
        self.money = 50
        self.invPlayer = []
        self.name = ' '
        self.health = 200
        self.dragon.x = 0
        self.dragon.y = 0
        self.dragon.health = 300
        self.x, self.y = 1080, 550
        self.cowName == "cow"

class Dragon(Fighter):
    def __init__(self, health, attack, graphic):
        super(Dragon, self).__init__(health, attack, graphic)
        self.halfHealth = health / 2
        self.graphic = graphic
        self.name = "Dragon"
        self.invPlayer = ["claw", "teeth", "fire", "scales"]
        self.money = 50
        self.x, self.y = 0, (300 - self.health)
        self.size = 300
        self.dragonRect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.speed = 4
        self.healthFont = pygame.font.Font(None, 64)
        self.awake = True

    def movement(self):
        """ set new coordinates for dragon rectangle """
        if self.health > self.halfHealth:
            self.y = (300 - self.health)
            
    def draw(self):
        """ Update, and draw rectangle then blit on correct image """
        self.dragonRect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.RED, self.dragonRect)
        if self.health > self.halfHealth:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragon1, (self.size, self.size)) , self.dragonRect)
        elif self.health <= self.halfHealth and self.awake:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragon2, (self.size, self.size)) , self.dragonRect)
        elif self.health <= self.halfHealth and self.awake == False:
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragon3, (self.size, self.size)) , self.dragonRect)  

class Village(Fighter):
    """ Health of the Village """
    def __init__(self, health, attack, graphic):
        super(Village, self).__init__(health, attack, graphic)
            
class Fireball(object):
        def __init__(self, graphic, player, dragon, village):
            self.graphic = graphic
            self.player = player
            self.dragon = dragon
            self.village = village
            self.size = 15
            self.x, self.y = self.dragon.size + self.size, self.dragon.y + 150
            self.speed_x = 14
            self.speed_y = 2            
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            
        def movement(self):
            """ Use this to set new coordinates. Do not update rectangle here. """
            self.x += self.speed_x
            self.y += self.speed_y
            
            #wall col
            if self.y <= 0:
                # bounce off ceiling
                self.speed_y *= -1
            elif self.y >= self.graphic.WINDOWHEIGHT - self.size:
                # bounce off floor (compensates for ball size so it stays on screen)
                self.speed_y *= -1

            if self.x <= 0:
                # resets ball if hits dragon wall, makes sure it doesn't touch the dragon or dragon loses health
                self.x, self.y = self.dragon.size + 1, self.dragon.y + random.randint(150, 200)
                self.speed_x *= -1

            elif self.x >= self.graphic.WINDOWWIDTH - self.size:
                # resets ball if hits village, makes sure it doesn't touch the dragon or dragon loses health
                self.village.updateHealth(self.dragon.attackOther("fire", self.village.health))
                self.x, self.y = self.dragon.size + 1, self.dragon.y + random.randint(150, self.dragon.size)               
        
            if self.rect.colliderect(self.player.playerRect):
                self.graphic.fireballSound.play()
                # deflects ball if hits player
                if "shield" in self.player.invPlayer:
                    # must bounce ball back player width or it gets stuck on player. Reverse speed so it returns.
                    self.x -= (self.player.playerWidth + self.size + self.speed_x)
                    self.speed_x *= -1
                    self.speed_y *= -1
                else:
                    # resets ball if hits player, makes sure it doesn't touch the dragon or dragon loses health
                    self.player.updateHealth(self.dragon.attackOther("fire", self.player.health))
                    self.x, self.y = self.dragon.size + 1, self.dragon.y + random.randint(150, self.dragon.size)
                    self.speed_x += 1
                    self.speed_x *= -1
                    self.speed_y *= -1

            if self.rect.colliderect(self.dragon.dragonRect):
                self.graphic.fireballSound.play()
                # resets ball when it hits the dragon                
                self.dragon.updateHealth(self.player.attackOther("fire", self.dragon.health))
                self.x, self.y = self.dragon.size, self.dragon.y + random.randint(150, self.dragon.size)
                self.speed_x *= -1
                self.speed_y *= -1
                self.speed_x += 1

        def draw(self):
            """ Create and draw new rectangle """
            if (self.village.health > 0) and (self.player.health > 0):
                self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
                pygame.draw.rect(self.graphic.windowSurface, self.graphic.RED, self.rect)
            else:
                self.rect = pygame.Rect(0, 0, self.size, self.size)
                pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.rect)


class GamePlay(object):
    """ This class controls the direction of game play """
    def __init__(self, player1, dragon, farmer, wizard, blacksmith, carpenter, seamstress, graphic):
        self.player1 = player1
        self.dragon = dragon
        self.graphic = graphic
        self.NPC = [farmer, blacksmith, wizard, carpenter, seamstress]
        self.musicPlaying = True
        self.difficulty = 0

    def mainMenu(self):
        """ Controls main menu """
        # Draw background
        while True:
            self.graphic.introSound.play()
            pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
            pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.background, 1)
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.castle, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), self.graphic.background)
            option1 = self.graphic.drawDialogCC("New Game", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[2][0], self.graphic.centerTextBox[2][1])
            option2 = self.graphic.drawDialogCC("Load Game", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[3][0], self.graphic.centerTextBox[3][1])           
            option3 = self.graphic.drawDialogCC("Exit", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[5][0], self.graphic.centerTextBox[5][1])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(option1).contains(click):
                            answer = ' '
                            result = 2
                                                        
                            while answer != 'n':                                
                                self.printIntro()
                                result = self.chooseNPC()
                                answer = self.getResult(result)
                            self.graphic.terminate()
                            
                        elif pygame.Rect(option2).contains(click):
                            self.load()
                            result = self.chooseNPC()
                            answer = self.getResult(result)
                            
                        elif pygame.Rect(option3).contains(click):
                            self.graphic.terminate()

    def settings(self):
        while True:
            # Draw background        
            pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
            pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.background, 1)
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.castle, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), self.graphic.background)
            if self.musicPlaying:
                self.graphic.drawDialogCenter("Sound: On", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[0][0], self.graphic.centerTextBox[0][1])
            else:
                self.graphic.drawDialogCenter("Sound: Off", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[0][0], self.graphic.centerTextBox[0][1])
            mute = self.graphic.drawDialogCC("Mute On/Off", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[1][0], self.graphic.centerTextBox[1][1])
            if self.difficulty == 0:
                self.graphic.drawDialogCenter("Difficulty: Easy", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[3][0], self.graphic.centerTextBox[3][1])
            elif self.difficulty == 1:
                self.graphic.drawDialogCenter("Difficulty: Normal", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[3][0], self.graphic.centerTextBox[3][1])
            easy = self.graphic.drawDialogCC("Easy", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[4][0], self.graphic.centerTextBox[4][1])
            normal = self.graphic.drawDialogCC("Normal", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[5][0], self.graphic.centerTextBox[5][1])
            menu = self.graphic.drawDialogCC("Continue", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[7][0], self.graphic.centerTextBox[7][1])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(mute).contains(click):
                            if self.musicPlaying:
                                pygame.mixer.music.stop()
                            else:
                                pygame.mixer.music.play(-1, 0.0)
                            self.musicPlaying = not self.musicPlaying
                        elif pygame.Rect(easy).contains(click):
                            self.difficulty = 0
                        elif pygame.Rect(normal).contains(click):
                            self.difficulty = 1
                        elif pygame.Rect(menu).contains(click):
                            return

    def printIntro(self):
        """Prints Intro"""
        self.settings()
        # Draw background        
        pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.background, 1)
        self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.castle, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), self.graphic.background)

        # Print Intro part 1
        intro_file = open("dragon_slayer_intro.txt", "r")
        incHeight = 530
        for line in intro_file:
            incHeight -= 30
            new_line = line[:(len(line)-1)]
            self.graphic.drawText(new_line, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, 325, (self.graphic.WINDOWHEIGHT) - incHeight)
        intro_file.close()
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()

        # Draw background
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.background, 1)
        self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.intro, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), self.graphic.background)

        # Print Intro part 2
        self.player1.setName()   
        self.player1.getPlayerInventory()
        self.graphic.drawDialog("Good luck on your quest!", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[0][0], self.graphic.rightTextBox[0][1])
        self.graphic.drawDialog("%s heads into town..." % self.player1.name, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()
        self.graphic.introSound.stop()
        
    #Choose NPC
    def chooseNPC(self):
        # Set up game
        mainClock = pygame.time.Clock()
        moveLeft = moveRight = moveUp = moveDown = False
        
        playerX = 600
        playerY = 300
        playerRect = pygame.Rect(playerX, playerY, 30, 60)

        resourceRewards = [self.NPC[0].need, self.NPC[1].need, self.NPC[3].need]
        result = 2
        pygame.mixer.quit()
        pygame.mixer.init(32100)
        pygame.mixer.music.load('map.wav')
        pygame.mixer.music.play(-1, 0.0)

        #Game Loop
        while result > 1:
            # Draw background
            self.graphic.windowSurface.fill(self.graphic.GREEN)
            save = self.graphic.drawDialogClickable("Save", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, 0, 0)
            setting = self.graphic.drawDialogCC("Settings", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, 455, 0)
            exit1 = self.graphic.drawDialogClickable("Exit", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, 770, 0)
            # Draw houses
            for index in range(len(self.graphic.shopRect)):
                pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.shopRect[index])
                self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.house, (200, 100)), self.graphic.shopRect[index])

            # Draw player
            pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, playerRect, 1)
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.person, (30, 60)), playerRect)

            # Draw Signs
            for index in range(len(self.graphic.signRect)):
                pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.signRect[index])
                self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.signImage[index], (250, 150)), self.graphic.signRect[index])
                pygame.draw.rect(self.graphic.windowSurface, self.graphic.GREEN, self.graphic.signPath[index])

            # farmer, blacksmith, carpenter, wizard, seamstress rectangles
            # Dragon, forest, quarry, swamp
            for shop in range(len(self.graphic.shopRect)):
                if playerRect.colliderect(self.graphic.shopRect[shop]):
                    self.NPC[shop].meetVillager(self.graphic.background, self.graphic.shopImage[shop], self.NPC[shop])
                    playerRect.move_ip(50, 50)
                    moveLeft = moveRight = moveUp = moveDown = False

            if playerRect.colliderect(self.graphic.signPath[3]):
                if self.validateSlayDragon():
                    result = self.slayDragonPart1()
                pygame.mixer.quit()
                pygame.mixer.init(32100)
                pygame.mixer.music.load('map.wav')
                pygame.mixer.music.play(-1, 0.0)
                playerRect.move_ip(50, 50)
                moveLeft = moveRight = moveUp = moveDown = False

            # Mini-Game
            for r in range(0, len(self.graphic.resourceObjects)):
                if playerRect.colliderect(self.graphic.signPath[r]):
                    while True:
                        self.graphic.resourceObjects[r].setUp()

                        # show the "Start" screen
                        self.graphic.resourceObjects[r].Intro()
                        
                        # Set up the start of the game
                        self.graphic.resourceObjects[r].setBoard()
                        self.graphic.resourceObjects[r].setMines()
                        self.graphic.resourceObjects[r].setMineCount()
                        finalResult = self.graphic.resourceObjects[r].chooseSquare()
                        self.graphic.resourceObjects[r].refreshVariables()
                        self.graphic.waitForPlayerToPressKey()
                        break
                    # Draw background
                    pygame.display.set_mode((self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT), 0, 32)
                    self.graphic.windowSurface.fill(self.graphic.GREEN)
                    pygame.display.update()
                    self.graphic.drawText(("Final result: " + str(finalResult)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[0][0], self.graphic.centerTextBox[0][1])
                    self.visitArea(finalResult, self.NPC[r].need)
                    playerRect.move_ip(0, -50)
                    moveLeft = moveRight = moveUp = moveDown = False


            while moveLeft and (playerRect.colliderect(self.graphic.signRect[0]) or playerRect.colliderect(self.graphic.signRect[1]) or playerRect.colliderect(self.graphic.signRect[2]) or playerRect.colliderect(self.graphic.signRect[3])):
                playerRect.move_ip(5, 0)
                moveLeft = False
            while moveRight and (playerRect.colliderect(self.graphic.signRect[0]) or playerRect.colliderect(self.graphic.signRect[1]) or playerRect.colliderect(self.graphic.signRect[2]) or playerRect.colliderect(self.graphic.signRect[3])):
                playerRect.move_ip(-5, 0)
                moveRight = False
            while moveUp and (playerRect.colliderect(self.graphic.signRect[0]) or playerRect.colliderect(self.graphic.signRect[1]) or playerRect.colliderect(self.graphic.signRect[2]) or playerRect.colliderect(self.graphic.signRect[3])):
                playerRect.move_ip(0, 5)
                moveUp = False
            while moveDown and (playerRect.colliderect(self.graphic.signRect[0]) or playerRect.colliderect(self.graphic.signRect[1]) or playerRect.colliderect(self.graphic.signRect[2]) or playerRect.colliderect(self.graphic.signRect[3])):
                playerRect.move_ip(0, -5)
                moveDown = False

            # Gather user input
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.graphic.terminate()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.graphic.terminate()
                    if event.key == K_LEFT:
                        moveLeft = True
                        moveRight = False
                    if event.key == K_RIGHT:
                        moveRight = True
                        moveLeft = False
                    if event.key == K_UP:
                        moveUp = True
                        moveDown = False
                    if event.key == K_DOWN:
                        moveDown = True
                        moveUp = False

                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        moveLeft = False
                    if event.key == K_RIGHT:
                        moveRight = False
                    if event.key == K_UP:
                        moveUp = False
                    if event.key == K_DOWN:
                        moveDown = False

                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(save).contains(click):                           
                            self.save()
                        elif pygame.Rect(setting).contains(click):
                            self.settings()
                        elif pygame.Rect(exit1).contains(click):                            
                            self.end()
                            

            # Move Player
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * self.graphic.PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < self.graphic.WINDOWWIDTH:
                playerRect.move_ip(self.graphic.PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * self.graphic.PLAYERMOVERATE)
            if moveDown and playerRect.bottom < self.graphic.WINDOWHEIGHT:
                playerRect.move_ip(0, self.graphic.PLAYERMOVERATE)
                
            pygame.display.update()

            mainClock.tick(self.graphic.FPS)
        
        return result    

    def save(self):
        file1 = open("Save1.txt", "r")
        name1 = file1.readline()
        name1 = name1[:(len(name1)-1)]
        file1.close()
        file2 = open("Save2.txt", "r")
        name2 = file2.readline()
        name2 = name2[:(len(name2)-1)]
        file2.close()
        file3 = open("Save3.txt", "r")
        name3 = file3.readline()
        name3 = name3[:(len(name3)-1)]
        file3.close() 
        self.graphic.smallerSurface.fill(self.graphic.GREEN)
        self.graphic.drawDialog("Choose save file: ", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
        save1 = self.graphic.drawDialogClickable("One", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        self.graphic.drawDialog(name1, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
        save2 = self.graphic.drawDialogClickable("Two", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
        self.graphic.drawDialog(name2, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.rightTextBox[2][0], self.graphic.rightTextBox[2][1])
        save3 = self.graphic.drawDialogClickable("Three", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[3][0], self.graphic.leftTextBox[3][1])
        self.graphic.drawDialog(name3, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.rightTextBox[3][0], self.graphic.rightTextBox[3][1])
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                    
                if event.type == KEYDOWN:
           
                    if event.key == K_RETURN:
                        pygame.display.update()
                        return

                    elif event.key == QUIT:
                        return

                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(save1).contains(click):
                            save_file = open("Save1.txt", "w")
                            save_file.write(self.player1.name + "\n")
                            save_file.write(str(self.player1.money) + "\n")
                            for item in self.player1.invPlayer:
                                save_file.write(str(item)+ "\n")
                            save_file.close()
                            self.graphic.drawDialog("Saved", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
                            pygame.display.update()
                            self.graphic.waitForPlayerToPressKey()
                            return
                        if pygame.Rect(save2).contains(click):
                            save_file = open("Save2.txt", "w")                            
                            save_file.write(self.player1.name + "\n")
                            save_file.write(str(self.player1.money) + "\n")
                            for item in self.player1.invPlayer:
                                save_file.write(str(item)+ "\n")
                            save_file.close()
                            self.graphic.drawDialog("Saved", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
                            pygame.display.update()
                            self.graphic.waitForPlayerToPressKey()
                            return
                        if pygame.Rect(save3).contains(click):
                            save_file = open("Save3.txt", "w")                            
                            save_file.write(self.player1.name + "\n")
                            save_file.write(str(self.player1.money) + "\n")
                            for item in self.player1.invPlayer:
                                save_file.write(str(item)+ "\n")
                            save_file.close()
                            self.graphic.drawDialog("Saved", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[3][0], self.graphic.leftTextBox[3][1])
                            pygame.display.update()
                            self.graphic.waitForPlayerToPressKey()
                            return

    def load(self):
        file1 = open("Save1.txt", "r")
        name1 = file1.readline()
        name1 = name1[:(len(name1)-1)]
        file1.close()
        file2 = open("Save2.txt", "r")
        name2 = file2.readline()
        name2 = name2[:(len(name2)-1)]
        file2.close()
        file3 = open("Save3.txt", "r")
        name3 = file3.readline()
        name3 = name3[:(len(name3)-1)]
        file3.close() 
        self.graphic.smallerSurface.fill(self.graphic.GREEN)
        self.graphic.drawDialog("Choose Game: ", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
        save1 = self.graphic.drawDialogClickable("One", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        self.graphic.drawDialog(name1, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
        save2 = self.graphic.drawDialogClickable("Two", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
        self.graphic.drawDialog(name2, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.rightTextBox[2][0], self.graphic.rightTextBox[2][1])
        save3 = self.graphic.drawDialogClickable("Three", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[3][0], self.graphic.leftTextBox[3][1])
        self.graphic.drawDialog(name3, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.rightTextBox[3][0], self.graphic.rightTextBox[3][1])
        menu = self.graphic.drawDialogCC("Return to Menu", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[6][0], self.graphic.centerTextBox[6][1])
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                    
                if event.type == KEYDOWN:

                    if event.key == K_RETURN:
                        pygame.display.update()
                        return

                    elif event.key == QUIT:
                        return

                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(save1).contains(click):
                            save_file = open("Save1.txt", "r")
                            self.player1.name = save_file.readline()
                            self.player1.name = self.player1.name[:(len(self.player1.name)-1)]
                            self.player1.money = save_file.readline()
                            self.player1.money = int(self.player1.money[:(len(self.player1.money)-1)])
                            self.player1.invPlayer = save_file.readlines()
                            for i, item in enumerate(self.player1.invPlayer):
                                self.player1.invPlayer[i] = item[:(len(item)-1)]
                            save_file.close()
                            return
                        
                        if pygame.Rect(save2).contains(click):
                            save_file = open("Save2.txt", "r")
                            self.player1.name = save_file.readline()
                            self.player1.name = self.player1.name[:(len(self.player1.name)-1)]
                            self.player1.money = save_file.readline()
                            self.player1.money = int(self.player1.money[:(len(self.player1.money)-1)])
                            self.player1.invPlayer = save_file.readlines()
                            for i, item in enumerate(self.player1.invPlayer):
                                self.player1.invPlayer[i] = item[:(len(item)-1)]
                            save_file.close()
                            return
                        
                        if pygame.Rect(save3).contains(click):
                            save_file = open("Save3.txt", "r")
                            self.player1.name = save_file.readline()
                            self.player1.name = self.player1.name[:(len(self.player1.name)-1)]
                            self.player1.money = save_file.readline()
                            self.player1.money = int(self.player1.money[:(len(self.player1.money)-1)])
                            self.player1.invPlayer = save_file.readlines()
                            for i, item in enumerate(self.player1.invPlayer):
                                self.player1.invPlayer[i] = item[:(len(item)-1)]
                            save_file.close()
                            return
                        if pygame.Rect(menu).contains(click):
                            self.mainMenu()

    def end(self):
        self.graphic.smallerSurface.fill(self.graphic.GREEN)
        self.graphic.drawDialog("Would you like to save your game? ", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
        option1 = self.graphic.drawDialogClickable("Yes", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        option2 = self.graphic.drawDialogClickable("No", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.smallerSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if pygame.Rect(option1).contains(click):                        
                        self.save()
                        pygame.mixer.music.stop()
                        self.player1.playAgain()
                        self.dragon.health = 200
                        pygame.display.update()
                        self.mainMenu()
                    elif pygame.Rect(option2).contains(click):
                        pygame.mixer.music.stop()
                        self.player1.playAgain()
                        pygame.display.update()
                        self.mainMenu()
               
    #Run ResourceQuest Modules
    def visitArea(self, result, reward):
        
        if result > 0:
            self.player1.invPlayer.append(reward)
        else:
            self.graphic.drawDialogCenter(("You were unable to gather any %s." % reward), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[6][0], self.graphic.centerTextBox[6][1])
        self.player1.getPlayerInventory()
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()

    def validateSlayDragon(self):
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, self.graphic.background, 1)
        self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragonIntro, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), self.graphic.background)
        pygame.mixer.quit()
        pygame.mixer.init(48000)
        pygame.mixer.music.load('dragon.wav')
        pygame.mixer.music.play(-1, 0.0)
        result = True
        if 'cow' in self.player1.invPlayer:
            self.graphic.drawDialog("You have the right bait", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
        else:
            self.graphic.drawDialog("You are missing your bait", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
            result = False
        if 'sword' in self.player1.invPlayer:
            self.graphic.drawDialog("You have the right weapon", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        else:
            self.graphic.drawDialog("You are missing the weapon", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
            result = False
        if 'sleep potion' in self.player1.invPlayer:
            self.graphic.drawDialog("You have the right potion", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
        else:
            self.graphic.drawDialog("You are missing the potion", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
            result = False
        if 'shield' in self.player1.invPlayer:
            self.graphic.drawDialog("You have the right protection", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[3][0], self.graphic.leftTextBox[3][1])
        else:
            self.graphic.drawDialog("You are missing the right protection", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[3][0], self.graphic.leftTextBox[3][1])
            result = False        

        # Allow player to face dragon early or with the wrong items
        if self.difficulty > 0:
            self.graphic.drawDialog("Slay the dragon?", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[0][0], self.graphic.rightTextBox[0][1])
            option1 = self.graphic.drawDialogClickable("Yes", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
            option2 = self.graphic.drawDialogClickable("No", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[2][0], self.graphic.rightTextBox[2][1])
            pygame.display.update()
            while True:           
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.graphic.terminate()
                    if event.type == MOUSEBUTTONDOWN:
                        click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                        if event.button == 1:
                            if pygame.Rect(option1).contains(click):
                                result = True
                                return result
                            elif pygame.Rect(option2).contains(click):                            
                                result = False
                                return result
                            
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()
        return result
           
    #Dragon Slayer Function
    def slayDragonPart1(self):
        pygame.display.set_caption("Dragon Battle")
        clock = pygame.time.Clock()
        village = Village(100, 0, self.graphic)
        ball = Fireball(self.graphic, self.player1, self.dragon, village)
        result = 2
        villResult = 0
        self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragonBackground,(self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)),[0,0])
        
        # Breaks loop when dragon health or player health is zero, not village
        while result > 1:
            #process
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragonBackground,(self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)),[0,0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print ("Game exited by user")
                    self.graphic.terminate()

            # Allows for dragon attack scene
            if villResult != 2:
                self.dragon.movement()
                self.player1.movement()
                ball.movement()
                villResult = village.scoring("village")
        
            result = self.player1.scoring("player")

            # Stops the following method from overriding result
            if result != 0:
                result = self.dragon.scoring("dragon")

            self.player1.draw()
            ball.draw()
            self.dragon.draw()

            if self.dragon.health <= self.dragon.halfHealth:
                self.player1.layBait()
                while self.dragon.y < self.dragon.size:
                    self.dragon.y += self.dragon.speed
                    self.dragon.dragonRect = pygame.Rect(self.dragon.x, self.dragon.y, self.dragon.size, self.dragon.size)
                    self.dragon.draw()
                    pygame.display.update()
                result = self.slayDragonPart2()

            if villResult == 2:
                self.player1.getEaten()
                village.health = 100
                
            pygame.display.flip()
            #pygame.time.delay(100)
            clock.tick(self.graphic.FPS)

        return result    

    def slayDragonPart2(self):
        pygame.display.set_caption("Dragon Battle")
        clock = pygame.time.Clock()
        result = 2
        self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragonBackground,(self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)),[0,0])
        while result > 1:
            #process
            self.graphic.windowSurface.blit(pygame.transform.scale(self.graphic.dragonBackground,(self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)),[0,0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print ("Game exited by user")
                    self.graphic.terminate()

            self.player1.drawBait()
            self.dragon.movement()
            self.player1.movement()
            self.dragon.draw()
            self.player1.draw()            
            result = self.player1.scoring("player")
            if result != 0:
                result = self.dragon.scoring("dragon")
            
            while self.player1.cowName == "cow2" and (self.player1.cowRect).colliderect(self.dragon.dragonRect) == False:
                self.dragon.x += self.dragon.speed
                self.dragon.dragonRect = pygame.Rect(self.dragon.x, self.dragon.y, self.dragon.size, self.dragon.size)
                self.dragon.draw()
                pygame.display.update()
            if self.player1.cowRect.colliderect(self.dragon.dragonRect):
                self.dragon.awake = False
            pygame.display.flip()
            clock.tick(self.graphic.FPS)

        return result 
           
    #Print Victory or Death
    def getResult(self, state):
        if state:
           self.graphic.drawDialog("You slayed the dragon! Lali is safe!", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[2][0] - 45, self.graphic.centerTextBox[2][1])
        else:
            self.graphic.drawDialogCenter("The dragon lives. You died.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[2][0] - 45, self.graphic.centerTextBox[2][1])
        self.graphic.drawDialog("Play again?", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[0][0], self.graphic.rightTextBox[0][1])
        option1 = self.graphic.drawDialogClickable("Yes", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
        option2 = self.graphic.drawDialogClickable("No", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[2][0], self.graphic.rightTextBox[2][1])
        pygame.display.update()
        cont = False
        while True:           
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(option1).contains(click):
                            self.player1.playAgain()
                            return 'y'
                        elif pygame.Rect(option2).contains(click):
                            self.graphic.drawDialogCenter("Thanks for playing!", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[7][0] - 45, self.graphic.centerTextBox[7][1])
                            pygame.display.update()
                            self.graphic.waitForPlayerToPressKey()
                            self.graphic.terminate()

        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()
  
#Main Function
def main():
    pygame.init()
    pygame.display.set_caption("Dragon Slayer 2")
    graphic = GraphicClass.Graphics()
    dragon = Dragon(300, 0, graphic)
    player1 = Player(200, 0, graphic, dragon)
    farmer = VillagerClass.Villager("farmer", "oak", ("a", "cow"), ("Just Looking", "eggs", "milk", "cow", "pig"), (0, 1, 10, 25, 15), player1, (1, 2), graphic)
    wizard = VillagerClass.Villager("wizard", "herbs", ("a", "sleep potion"), ("Just Looking", "hemlock", "love potion", "sleep potion"), (0, 5, 30, 30), player1,(3, 4), graphic)
    blacksmith = VillagerClass.Villager("blacksmith", "ore", ("a", "sword"), ("Just Looking", "sword", "shield", "armour", "mace"), (0, 15, 25, 30, 10), player1, (5, 6), graphic)
    carpenter = VillagerClass.Villager("carpenter", "love potion", ("$", "35"), ("Just Looking", "lumber", "firewood", "wooden horse"), (0, 25, 15, 5), player1, (7, 8), graphic)
    seamstress = VillagerClass.Villager("seamstress", "eggs", ("$", "2"), ("Just Looking", "shirt", "pants", "pouch"), (0, 10, 25, 50), player1, (9, 10), graphic)
    game = GamePlay(player1, dragon, farmer, wizard, blacksmith, carpenter, seamstress, graphic)
    game.mainMenu()

    graphic.terminate()
#Call Main Function
main()
