#Define class Villager for Dragon Slayer

import pygame, random, time, ResourceQuest2, sys, GraphicClass
from pygame.locals import *

class Villager(object):
    """ A class that holds all villager interactions """
    def __init__(self, nameIn, needIn, paysIn, inventoryIn, pricesIn, player1, h1, graphic):
        self.name = nameIn
        self.need = needIn
        self.pays = paysIn
        self.inventory = inventoryIn
        self.prices = pricesIn
        self.player1 = player1
        self.hint1 = h1
        self.graphic = graphic
    
    def meetVillager(self, background, image, villager):
        cont = False
        while cont != True:
            pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, background, 1)
            self.graphic.windowSurface.blit(pygame.transform.scale(image, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), background)

            self.graphic.drawDialog(("%s: Hello, %s. How can I help you today?" % (self.name.title(), self.player1.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])      

            self.graphic.drawDialog(("You respond with: "), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[0][0], self.graphic.rightTextBox[0][1])

            option1 = self.graphic.drawDialogClickable(("%s: Do you need any help?" % (self.player1.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
            option2 = self.graphic.drawDialogClickable(("%s: What do you have for sale?" % (self.player1.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[2][0], self.graphic.rightTextBox[2][1])
            option3 = self.graphic.drawDialogClickable(("%s: Just saying hello." % (self.player1.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[3][0], self.graphic.rightTextBox[3][1])
            option4 = self.graphic.drawDialogClickable("Return to Town", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[4][0], self.graphic.rightTextBox[4][1])           
                   
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        if pygame.Rect(option1).contains(click):
                            villager.getHelp(background, image)
                            pygame.display.update()
                        elif pygame.Rect(option2).contains(click):
                            self.player1.getPlayerInventory()                            
                            villager.getStore(background, image)
                            pygame.display.update()
                        elif pygame.Rect(option3).contains(click):
                            self.__getHint()                            
                            pygame.display.update()
                        elif pygame.Rect(option4).contains(click):
                            self.graphic.drawDialog(("It was nice talking to you. Come back again."), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
                            pygame.display.update()
                            cont = True
                        
                            
            pygame.display.update()
            
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()
        

    def getHelp(self, background, image):
        # Refreshes background to store
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, background, 1)
        self.graphic.windowSurface.blit(pygame.transform.scale(image, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), background)
        self.graphic.drawDialog("%s: %s, I really need some %s." % (self.name.title(), self.player1.name, self.need), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])
        self.player1.getPlayerInventory()
        if self.player1.validatePlayerInventory() == False:
            self.graphic.drawDialog("%s: Your inventory is full." %(self.name.title()), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        else:
            self.graphic.drawDialog("%s: Do you have any %s I could have?" %(self.name.title(), self.need), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
            option1 = self.graphic.drawDialogClickable(("%s: Yes" % (self.player1.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[0][0], self.graphic.rightTextBox[0][1])
            option2 = self.graphic.drawDialogClickable(("%s: No" % (self.player1.name)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.rightTextBox[1][0], self.graphic.rightTextBox[1][1])
            cont = False
            # Refreshes Menu
            pygame.display.update()
            while cont != True:           
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.graphic.terminate()
                    if event.type == MOUSEBUTTONDOWN:
                        click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                        if event.button == 1:
                            if pygame.Rect(option1).contains(click):
                                if self.need in self.player1.invPlayer:
                                    self.graphic.drawDialog("%s: Thank you! Here is a %s." % (self.name.title(), self.pays[1]), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
                                    for item in self.player1.invPlayer[:]:
                                        if item == self.need:
                                            self.player1.invPlayer.remove(item)
                                            cont = True
                                    if self.pays[1].isdigit():
                                        self.player1.money += int(self.pays[1])
                                    else:
                                        self.player1.invPlayer.append(self.pays[1])
                                    self.player1.getPlayerInventory()
                                    pygame.display.update()
                                elif not self.need in self.player1.invPlayer:
                                    self.graphic.drawDialog("%s: You don't have any %s. I will pay %s %s for one." % (self.name.title(), self.need, self.pays[0], str(self.pays[1])), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[2][0], self.graphic.leftTextBox[2][1])
                                    pygame.display.update()
                                    cont = True
                                                
                            elif pygame.Rect(option2).contains(click):
                                self.graphic.drawDialog("%s: If you bring me one I will pay you %s %s." % (self.name.title(), self.pays[0], str(self.pays[1])),self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[3][0], self.graphic.leftTextBox[3][1])
                                pygame.display.update()
                                cont = True
                                
            pygame.display.update()
        self.graphic.waitForPlayerToPressKey()

    def getStore(self, background, image):
        # Refreshes background to store
        pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, background, 1)
        self.graphic.windowSurface.blit(pygame.transform.scale(image, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), background)
        pygame.display.update()
        answer = ' '
        while answer != 'n':
            pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, background, 1)
            self.graphic.windowSurface.blit(pygame.transform.scale(image, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), background)
 
            self.graphic.drawDialog("What would you like to buy:", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])            

            itemRect = []
            for item in range(len(self.inventory)):
                string = ' '
                string += "$" + str(self.prices[item]) + " for " + str(self.inventory[item])
                itemRect.append(self.graphic.drawDialogClickable(string, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[item + 1][0], self.graphic.leftTextBox[item + 1][1]))
                self.graphic.drawDialogClickable(string, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[item + 1][0], self.graphic.leftTextBox[item + 1][1])              

            self.graphic.drawDialogCenter(("%s's wallet: $%d" % (self.player1.name, self.player1.money)), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[0][0], self.graphic.centerTextBox[0][1])
            self.graphic.drawDialogCenter(("What would you like to sell: "), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[1][0], self.graphic.centerTextBox[1][1])
            for index, item in enumerate(self.player1.invPlayer):           
                itemRect.append(self.graphic.drawDialogCC(item, self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.centerTextBox[index + 2][0], self.graphic.centerTextBox[index + 2][1]))

            Flag = True
            if self.player1.validatePlayerInventory() == False:
                self.graphic.drawDialog("%s: Your inventory is full." %(self.name.title()), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[7][0], self.graphic.leftTextBox[7][1])
                pygame.display.update()
                Flag = False

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphic.terminate()
                if event.type == MOUSEBUTTONDOWN:
                    click = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if event.button == 1:
                        for index, rectangle in enumerate(itemRect):
                            if pygame.Rect(rectangle).contains(click):
                                if index == 0:
                                    answer = 'n'                                    
                                if index > 0 and index < len(self.inventory) and Flag:
                                    legal = self.__validatePurchase(self.player1.money, self.prices[index])
                                    if legal:
                                        self.player1.invPlayer.append(self.inventory[index])
                                        self.player1.money -= self.prices[index]
                                        self.graphic.coinSound.play(0, 500)
                                    pygame.draw.rect(self.graphic.windowSurface, self.graphic.WHITE, background, 1)
                                    self.graphic.windowSurface.blit(pygame.transform.scale(image, (self.graphic.WINDOWWIDTH, self.graphic.WINDOWHEIGHT)), background)
                                    self.player1.getPlayerInventory()
                                    #Refreshes inventory
                                    pygame.display.update()
                                if index >= len(self.inventory):
                                    item = self.player1.invPlayer[index - len(self.inventory)]
                                    if item in self.inventory:
                                        self.player1.invPlayer.remove(item)
                                    for index, merch in enumerate(self.inventory):
                                        if merch == item:
                                            self.player1.money += self.prices[index]
                                            self.graphic.coinSound.play(0, 500)
                                    
                                    
            # Refreshes all
            pygame.display.update()
                

    def __validatePurchase(self, money, spent):
        flag = True
        if (money - spent) < 0:
            flag = False
            self.graphic.drawDialog("%s: You don't have enough money." % self.name.title(), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[7][0], self.graphic.leftTextBox[7][1])
        elif spent == 0:
            flag = False
            self.graphic.drawDialog("You chose not to buy anything.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[7][0], self.graphic.leftTextBox[7][1])
        else:
            flag = True
        return flag

    def __getHint(self):
        hint = 0
        hint = self.hint1[random.randint(0, 1)]
        self.graphic.drawDialog("%s: Did you know" % self.name.title(), self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[0][0], self.graphic.leftTextBox[0][1])        
        if hint == 1:
            self.graphic.drawDialog("the carpenter was looking for a love potion.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 2:
            self.graphic.drawDialog("the seamstress needed some eggs.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface,self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 3:
            self.graphic.drawDialog("dragons prefer cows over pigs.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface,self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 4:
            self.graphic.drawDialog("swords are the best weapons against dragons.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface,self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 5:
            self.graphic.drawDialog("it's easiest to kill dragon when it's sleeping.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface,self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 6:
            self.graphic.drawDialog("armour is useless against dragons.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface,self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 7:
            self.graphic.drawDialog("feeding eggs to dragons makes them very angry.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 8:
            self.graphic.drawDialog("hemlock isn't poisonous to dragons.", self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        elif hint == 9:
            self.graphic.drawDialog("dragons burn all wood and cloth items." ,self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        else:
            self.graphic.drawDialog("dragons are mean." , self.graphic.smallerFont, self.graphic.BLACK, self.graphic.windowSurface, self.graphic.leftTextBox[1][0], self.graphic.leftTextBox[1][1])
        pygame.display.update()
        self.graphic.waitForPlayerToPressKey()

