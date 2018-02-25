# Graphic methods for Dragon Slayer Game

import pygame, sys, ResourceQuest2
from pygame.locals import *

class Graphics(object):
    
    def __init__(self):
        self.WINDOWWIDTH = 1200
        self.WINDOWHEIGHT = 600
        self.SMALLWIDTH = 440
        self.SMALLHEIGHT = 440
        self.TEXTCOLOR = (255, 255, 255)
        self.BACKGROUNDCOLOR  = (0, 0, 0)
        self.FPS = 60
        self.PLAYERMOVERATE = 4
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (34, 177, 76)
        self.BLUE = (0, 0, 225)
        self.WHITE = (225, 225, 225)
        self.letters = []
        self.rows = []
        self.printSq = []
        self.windowSurface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), 0, 32)
        self.smallerSurface = pygame.display.set_mode((self.SMALLWIDTH, self.SMALLHEIGHT), 0, 32)
        self.basicFont = pygame.font.SysFont(None, 48) # set up fonts
        self.smallerFont = pygame.font.SysFont(None, 24)
        self.smallestFont = pygame.font.SysFont(None, 12)

        self.introSound = pygame.mixer.Sound('intro.wav')
        self.mapSound = pygame.mixer.Sound('map.wav')
        self.dragonSound = pygame.mixer.Sound('dragon.wav')
        self.coinSound = pygame.mixer.Sound('Coin_Drop.wav')
        self.roarSound = pygame.mixer.Sound('Dragon Roaring.wav')
        self.mooSound = pygame.mixer.Sound('moo.wav')
        self.splashSound = pygame.mixer.Sound('Splash.wav')               
        self.fireballSound = pygame.mixer.Sound('Fireball.wav')

        # Rectangles
        self.background = pygame.Rect(0,0, self.WINDOWWIDTH, self.WINDOWHEIGHT)
        self.playerRect = pygame.Rect(300, 450, 60, 90)

        # Intro Images
        self.castle = pygame.image.load('castle.png').convert_alpha()
        self.intro = pygame.image.load('intro.png').convert()
        self.dragonIntro = pygame.image.load('dragonIntro.png').convert()
        self.dragonBackground = pygame.image.load('dragonBackground.png').convert()

        # Fighter Images
        self.person = pygame.image.load('player.png').convert()
        self.person2 = pygame.image.load('player2.png').convert()
        self.personSword = pygame.image.load('playerSword.png').convert()
        self.personSwordShield = pygame.image.load('playerSwordandShield.png').convert()
        self.personPotion = pygame.image.load('playerSwordPotion.png').convert()
        self.dragon1 = pygame.image.load('dragonFighter.png').convert()
        self.dragon2 = pygame.image.load('dragonLanded.png').convert()
        self.dragon3 = pygame.image.load('dragonAsleep.png').convert()
        self.cow = pygame.image.load('Cow.png').convert()
        self.cow2 = pygame.image.load('CowAsleep.png').convert()

        self.house = pygame.image.load('house.png').convert()
        
        # forest, quarry, swamp, dragon
        self.signImage = [pygame.image.load('forestSign.png').convert(), pygame.image.load('quarrySign.png').convert(), pygame.image.load('swampSign.png').convert(), pygame.image.load('dragonSign.png').convert()]
        self.signRect = [pygame.Rect(350, 450, 250, 150), pygame.Rect(950, 450, 250, 150), pygame.Rect(650, 450, 250, 150), pygame.Rect(450, 50, 250, 150)]
        self.signPath = [pygame.Rect(467, 439, 47, 10), pygame.Rect(1067, 439, 47, 10), pygame.Rect(767, 439, 47, 10), pygame.Rect(564, 201, 50, 10)] 

        # farmer, blacksmith, wizard, carpenter, seamstress rectangles
        self.shopImage = [pygame.image.load('farmershop.png').convert(), pygame.image.load('smithshop.png').convert(), pygame.image.load('wizshop.png').convert(), pygame.image.load('carpshop.png').convert(), pygame.image.load('seamshop.png').convert()]
        self.shopRect = [pygame.Rect(10, 50, 200, 100), pygame.Rect(10, 220, 200, 100), pygame.Rect(10, 400, 200, 100), pygame.Rect(710, 50, 200, 100), pygame.Rect(1010, 50, 200, 100)]
        
        self.leftTextBox = ((0, 50), (0, 110), (0, 170), (0, 230), (0, 290), (0, 350), (0, 410), (0, 470), (0, 530))
        self.centerTextBox = ((475, 50), (475, 110), (475, 170), (475, 230), (475, 290), (475, 350), (475, 410), (475, 470), (475, 530), (475, 550))
        self.rightTextBox = ((815, 50), (815, 110), (815, 170), (815, 230), (815, 290), (815, 350), (815, 410), (815, 470), (815, 530)) 

        self.resourceName = ["oak", "ore", "herbs"]
        self.resourceArea = ["forest", "quarry", "swamp"]
        self.resourceCount = [7, 14, 28]
        self.resourceImage = [pygame.image.load('Oak.png').convert(), pygame.image.load('Ore.png').convert(), pygame.image.load('Herbs.png').convert()]
        self.resourceImage2 =[pygame.image.load('Oak2.png').convert(), pygame.image.load('Ore2.png').convert(), pygame.image.load('Herbs2.png').convert()]
        forest = ResourceQuest2.ResourceArea(self.resourceName[0], self.resourceArea[0], self.resourceCount[0], self.resourceImage[0], self.resourceImage2[0], self)
        quarry = ResourceQuest2.ResourceArea(self.resourceName[1], self.resourceArea[1], self.resourceCount[1], self.resourceImage[1], self.resourceImage2[1], self)
        swamp = ResourceQuest2.ResourceArea(self.resourceName[2], self.resourceArea[2], self.resourceCount[2], self.resourceImage[2], self.resourceImage2[2], self)
        self.resourceObjects = [forest, quarry, swamp]
        self.flagImage = pygame.image.load('flag.png')
        self.zeroImage = pygame.image.load('zero.png')
        self.blankImage = pygame.image.load('blank.png')
        
    def terminate(self):
        pygame.quit()
        sys.exit()

    def waitForPlayerToPressKey(self):
        self.drawDialogCenter("Press Enter to continue...", self.smallerFont, self.BLACK, self.windowSurface, self.centerTextBox[9][0], self.centerTextBox[9][1])
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    if event.key == K_RETURN:
                        return
                if event.type == MOUSEBUTTONDOWN:
                    return

    def drawText(self, text, font, color, surface, x = 0, y = 0):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def drawDialog(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width, text_height = font.size(text)
        textRect = pygame.Rect(x, y, 430,  50) 
        textPos = pygame.Rect(x + ((430 - text_width) / 2), y + 20, text_width, text_height)
        pygame.draw.rect(surface, self.BLUE, (textRect.left, textRect.top, 430, 50))
        pygame.draw.rect(surface, self.BLUE, (textPos.left, textPos.top, textPos.width, textPos.height))
        surface.blit(textobj, textPos)

    def drawDialogClickable(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width, text_height = font.size(text)
        textRect = pygame.Rect(x, y, 430,  50)
        textPos = pygame.Rect(x + ((430 - text_width) / 2), y + 20, text_width, text_height)
        pygame.draw.rect(surface, self.WHITE, (textRect.left, textRect.top, 430, 50))
        pygame.draw.rect(surface, self.WHITE, (textPos.left, textPos.top, textPos.width, textPos.height))
        surface.blit(textobj, textPos)

        return textRect

    def drawDialogCenter(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width, text_height = font.size(text)
        textRect = pygame.Rect(x, y, 295,  50)
        textPos = pygame.Rect(x + ((295 - text_width) / 2), y + 20, text_width, text_height)
        pygame.draw.rect(surface, self.GREEN, (textRect.left, textRect.top, 295, 50))
        pygame.draw.rect(surface, self.GREEN, (textPos.left, textPos.top, textPos.width, textPos.height))
        surface.blit(textobj, textPos)

    def drawDialogCC(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_width, text_height = font.size(text)
        textRect = pygame.Rect(x, y, 295,  50)
        textPos = pygame.Rect(x + ((295 - text_width) / 2), y + 20, text_width, text_height)
        pygame.draw.rect(surface, self.WHITE, (textRect.left, textRect.top, 295, 50))
        pygame.draw.rect(surface, self.WHITE, (textPos.left, textPos.top, textPos.width, textPos.height))
        surface.blit(textobj, textPos)

        return textRect
