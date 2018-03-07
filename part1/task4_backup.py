#! /usr/bin/env python

import sys,abc,random

class Weapon(object):
    def __init__(self,range,damage,owner):
        self.range = range
        self.effect = damage
        self.owner = owner
    def getEffect(self):
        return self.effect
    def getRange(self):
        return self.range
    @abc.abstractmethod
    def action(self,posx,posy):
        return
    def enhance(self):
        return



class Wand(object):
    _WAND_RANGE = 5
    _WAND_INIT_EFFECT = 10
    def __init__(self,owner):
        self.range = Wand._WAND_RANGE
        self.effect = Wand._WAND_INIT_EFFECT
        self.owner = owner
    def enhance(self):
        self.effect+=5
    def getEffect(self):
        return self.effect
    def getRange(self):
        return self.range
    def action(self,posx,posy):
        print("You are using Wand healing " + str(posx) + " " + str(posy) + ".")
        if self.owner.pos.distance(posx,posy) <= self.range:
            player = self.owner.game.getPlayer(posx, posy)
            if player == None:
                print("You heal nothing")
            elif not isinstance(player,self.owner.__class__):
                print("You cannot heal your opponent!")
            else:
                if isinstance(player,self.owner.__class__):
                    player.increaseHealth(self.effect)
        else:
            print("Out of reach.")
        return


class Axe(Weapon):
    _AXE_RANGE = 1
    _AXE_INIT_DAMAGE = 40

    def __init__(self,owner):
        super(Axe,self).__init__(Axe._AXE_RANGE,Axe._AXE_INIT_DAMAGE,owner)
        return

    def enhance(self):
        self.effect+=10

    def action(self,posx,posy):
        print("You are using axe attacking " + str(posx) + " " + str(posy) + ".")
        if self.owner.pos.distance(posx,posy) <= self.range:
            player = self.owner.game.getPlayer(posx, posy)
            if player != None:
                if not isinstance(player,self.owner.__class__):
                    player.decreaseHealth(self.effect)
                else:
                    print("You cannot attack your own race!")
        else:
            print("Out of reach.")
        return

class Rifle(Weapon):
    _RIFLE_RANGE = 4
    _RIFLE_INIT_DAMAGE = 10;
    _AMMO_LIMIT = 6;
    _AMMO_RECHARGE = 3;

    def __init__(self,owner):
        super(Rifle,self).__init__(Rifle._RIFLE_RANGE,Rifle._RIFLE_INIT_DAMAGE,owner)
        self._ammo = Rifle._AMMO_LIMIT
        return

    def enhance(self):
        self._ammo = min(Rifle._AMMO_LIMIT,self._ammo+Rifle._AMMO_RECHARGE)
        return

    def action(self,posx,posy):
        print("You are using rifle attacking " + str(posx) + " " + str(posy) + ".")
        print("Type how many ammos you want to use.")
        ammoToUse = int(raw_input())
        if ammoToUse > self._ammo:
            print("You don't have that ammos.")
            return
        if(self.owner.pos.distance(posx, posy) <= self.range):
            # search for all targets with target coordinates.
            player = self.owner.game.getPlayer(posx, posy)
            if player != None:
                if not isinstance(player,self.owner.__class__):
                    player.decreaseHealth(self.effect * ammoToUse)
                    self.ammo -= ammoToUse
                else:
                    print("You cannot attack your own race!")
        else:
            print("Out of reach.")

    def getAmmo(self):
        return self._ammo

class Player(object):



    def __init__(self,healthCap,mob,posx,posy,index,game):
        self._HEALTH_CAP = healthCap
        self._MOBILITY = mob
        self.pos = Pos(posx,posy)
        self.index = index
        self.game = game
        self.health = healthCap
        self.myString = None
        self.equipment = None

    def getPos(self):
        return self.pos

    def teleport(self):
        randx = random.randint(0,game.D-1)
        randy = random.randint(0,game.D-1)
        while game.positionOccupied(randx, randy):
            randx = random.randint(0,game.D-1)
            randy = random.randint(0,game.D-1)
        self.pos.setPos(randx,randy)
        return

    def increaseHealth(self,h):
        dead = False
        if self.health<0:
            dead = True
        self.health += h
        self.health = min(self.health,self._HEALTH_CAP)
        if self.health>0 and dead:
            self.myString = self.myString[1] + str(self.index)
        return

    def decreaseHealth(self,h):
        self.health -= h
        if self.health <= 0:
            self.myString = 'C'+self.myString[0]
        return

    def getName(self):
        return self.myString

    def askForMove(self):
        print("Your health is " + str(self.health)+". Your position is (%d,%d). Your mobility is %d."%(self.pos.getX(),self.pos.getY(),self._MOBILITY))
        print("You now have following options: \n1. Move\n2. Attack\n3. End the turn")
        a = int(raw_input())
        if a == 1:
            print("Specify your target position (Input 'x y').")
            posx,posy = map(int,raw_input().split(' '))
            if self.pos.distance(posx, posy) > self.MOBILITY:
                print("Beyond your reach. Staying still.")
            elif self.game.positionOccupied(posx, posy):
                print("Position occupied. Cannot move there.")
            else:
                self.pos.setPos(posx, posy)
                self.game.printBoard()
                print("You can now \n1.attack\n2.End the turn")
                if int(raw_input()) == 1:
                    print("Input position to attack. (Input 'x y')")
                    attx,atty = map(int,raw_input().split(' '))
                    if(self.game.getPlayer(attx,atty)==None):
                        print("You attack nothing")
                    elif(isinstance(self.game.getPlayer(attx,atty),self.__class__)):
                        print("You cannot attack your comrade!")
                    else:
                        self.equipment.action(attx, atty)
        elif a == 2:
            print("Input position to attack.")
            attx, atty = map(int,raw_input().split(' '))
            if(self.game.getPlayer(attx,atty)==None):
                print("You attack nothing")
            elif(isinstance(self.game.getPlayer(attx,atty),self.__class__)):
                print("You cannot attack your comrade!")
            else:
                self.equipment.action(attx, atty)
        elif a== 3:
            return

    def askLast(self):
        print("Your health is " + str(self.health)+". Your position is (%d,%d). Your mobility is %d."%(self.pos.getX(),self.pos.getY(),self.MOBILITY))
        print("You now have following options: \n1. Move\n2. Heal\n3. End the turn")
        a = int(raw_input())
        if a == 1:
            print("Specify your target position (Input 'x y').")
            posx,posy = map(int,raw_input().split(' '))
            if self.pos.distance(posx, posy) > self.MOBILITY:
                print("Beyond your reach. Staying still.")
            elif self.game.positionOccupied(posx, posy):
                print("Position occupied. Cannot move there.")
            else:
                self.pos.setPos(posx, posy)
                self.game.printBoard()
                print("You can now \n1.heal\n2.End the turn")
                if int(raw_input()) == 1:
                    print("Input position to heal. (Input 'x y')")
                    healx,healy = map(int,raw_input().split(' '))
                    self.equipment.action(healx, healy)
        elif a == 2:
            print("Input position to heal.")
            healx,healy = map(int,raw_input().split(' '))
            self.equipment.action(healx, healy)
        elif a== 3:
            return

class Human(Player):
    def __init__(self,posx,posy,index,game):
        super(Human,self).__init__(80,2,posx,posy,index,game)
        self.myString = 'H' + str(index)
        self.equipment = Rifle(self)
    def teleport(self):
        super(Human,self).teleport()
        self.equipment.enhance()

    def distance(self):
        return

    def askForMove(self):
        if isinstance(self.equipment,Rifle):
            print("You are a human (H%d) using Rifle. (Range: %d, Ammo #: %d, Damage per shot: %d)"%(self.index,self.equipment.getRange(),self.equipment.getAmmo(),self.equipment.getEffect() ))
            super(Human,self).askForMove()
        elif isinstance(self.equipment,Wand):
            print("You are a human (H%d) using Wand. (Range: %d, Effect: %d )"%(self.index,self.equipment.getRange(),self.equipment.getEffect()))
            super(Human,self).askLast()


    def equipWand(self):
        self.equipment = Wand(self)

class Chark(Player):
    def __init__(self,posx,posy,index,game):
        super(Chark,self).__init__(100,4,posx,posy,index,game)
        self.myString = 'C' + str(index)
        self.equipment = Axe(self)

    def teleport(self):
        super(Chark,self).teleport()
        self.equipment.enhance()

    def distance(self):
        return

    def askForMove(self):
        if isinstance(self.equipment,Axe):
            print("You are a Chark (C%d) using Axe. (Range: %d, Damage: %d)"%(self.index,self.equipment.getRange(),self.equipment.getEffect() ))
            super(Chark,self).askForMove()
        elif isinstance(self.equipment,Wand):
            print("You are a Chark (C%d) using Wand. (Range: %d, Effect: %d )"%(self.index,self.equipment.getRange(),self.equipment.getEffect()))
            super(Chark,self).askLast()


    def equipWand(self):
        self.equipment = Wand(self)


class Obstacle(object):
    def __init__(self,posx,posy,index,game):
        self.pos = Pos(posx,posy)
        self.index = index
        self.game = game

    def getPos(self):
        return self.pos

    def teleport(self):
        randx = random.randint(0,self.game.D-1)
        randy = self.game.D - randx - 1
        while self.game.positionOccupied(randx, randy):
            randx = random.randint(0,self.game.D-1)
            randy = self.game.D - randx - 1
        self.pos.setPos(randx,randy)

class Pos(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def distance(self,*args):
        if len(args)==1 and isinstance(args[0],Pos):
            another = args[0]
            return abs(self.x - another.x) + abs(self.y - another.y)
        elif len(args)==2 and isinstance(args[0],int) and isinstance(args[1],int):
            x1 = args[0]
            y1 = args[1]
            return abs(self.x - x1) + abs(self.y - y1)



    def setPos(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class SurvivalGame(object):
    D = 10
    O = 2
    def __init__(self):
        self.n = None
        self.teleportObjects = []

    def printBoard(self):
        # init printObject
        printObject = [["  " for i in range(SurvivalGame.D)] for j in range(SurvivalGame.D)]

        for i in range(self.n):
            pos = self.teleportObjects[i].getPos()
            printObject[pos.getX()][pos.getY()] = (self.teleportObjects[i]).getName()

        for i in range(self.n,self.n+SurvivalGame.O):
            pos = (self.teleportObjects[i]).getPos()
            printObject[pos.getX()][pos.getY()] = "O" + str(i-self.n)

        firstLine = " "+"".join(["| %d  "%i for i in range(SurvivalGame.D)])+"|"
        print(firstLine)
        print("".join([ "-" for i in range(int(SurvivalGame.D*5.5))]))
        for row in range(SurvivalGame.D):
            row_str = str(row)+''.join(['| %s '%(printObject[row][i]) for i in range(SurvivalGame.D)])+'|'
            print(row_str)
            print("".join([ "-" for i in range(int(SurvivalGame.D*5.5))]))

    def positionOccupied(self,randx,randy):
        for o in self.teleportObjects:
            pos = o.getPos()
            if pos.getX() == randx and pos.getY() == randy:
                return True
        return False

    def getPlayer(self,randx,randy):
        for o in self.teleportObjects:
            if isinstance(o,Player):
                pos = o.getPos()
                if pos.getX() == randx and pos.getY() == randy:
                    return o
        return None

    def init(self):
        print("Welcome to Kafustrok. Light blesses you. \nInput number of players: (a even number)")
        self.n = int(raw_input())
        no_obj = self.n + SurvivalGame.O
        self.teleportObjects = [None for i in range(no_obj)]
        for i in range(0,(self.n)/2):
            self.teleportObjects[i] = Human(0,0,i,self)
            self.teleportObjects[i+(self.n)/2] = Chark(0,0,i,self)
        # enhanced feature, last one holds Wand
        self.teleportObjects[(self.n)/2-1].equipWand()
        self.teleportObjects[self.n-1].equipWand()


        for i in range(SurvivalGame.O):
            self.teleportObjects[i+self.n] = Obstacle(0,0,i,self)

    def reachEnd(self):
        HumanAllDead = True
        CharkAllDead = True
        for i in range(self.n/2):
            #print("%d's health is %d"%(i,self.teleportObjects[i].health))
            if self.teleportObjects[i].health > 0:
                HumanAllDead = False
                break

        if HumanAllDead:
            return True

        for i in range(self.n/2):
            #print("%d's health is %d"%(i,self.teleportObjects[i].health))
            if self.teleportObjects[i+self.n/2].health > 0:
                CharkAllDead = False
                break

        return CharkAllDead

    def gameStart(self):
        turn = 0
        numOfAlivePlayers = self.n
        while not self.reachEnd():
            # teleport after every N turns
            if turn == 0:
                for obj in self.teleportObjects:
                    obj.teleport()
                print("Everything gets teleported..")
            self.printBoard()
            t = self.teleportObjects[turn]
            if t.health > 0:
                t.askForMove()
                print("")
            turn = (turn + 1) % self.n
            numOfAlivePlayers = 0
            for i in range(self.n):
                if self.teleportObjects[i].health > 0:
                    numOfAlivePlayers += 1
        print("Game over.")
        self.printBoard()

game = SurvivalGame()
game.init()
game.gameStart()
