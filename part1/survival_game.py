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



class Axe(Weapon):
    AXE_RANGE = 1
    AXE_INIT_DAMAGE = 40

    def __init__(self,owner):
        super(Axe,self).__init__(Axe.AXE_RANGE,Axe.AXE_INIT_DAMAGE,owner)
        return

    def enhance(self):
        self.effect+=10

    def action(self,posx,posy):
        print("You are using axe attacking " + str(posx) + " " + str(posy) + ".")
        if self.owner.pos.distance(posx,posy) <= self.range:
            player = self.owner.game.getPlayer(posx, posy)
            if player != None:
                player.decreaseHealth(self.effect)
        else:
            print("Out of reach.")
        return

class Rifle(Weapon):
    RIFLE_RANGE = 4
    RIFLE_INIT_DAMAGE = 10;
    AMMO_LIMIT = 6;
    AMMO_RECHARGE = 3;

    def __init__(self,owner):
        super(Rifle,self).__init__(Rifle.RIFLE_RANGE,Rifle.RIFLE_INIT_DAMAGE,owner)
        self._ammo = Rifle.AMMO_LIMIT
        return

    @property
    def ammo(self):
        return self._ammo
    @ammo.setter
    def ammo(self,ammo):
        self._ammo = ammo

    def enhance(self):
        self._ammo = min(Rifle.AMMO_LIMIT,self._ammo+Rifle.AMMO_RECHARGE)
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
                player.decreaseHealth(self.effect * ammoToUse)
                self._ammo -= ammoToUse
        else:
            print("Out of reach.")

    def getAmmo(self):
        return self._ammo

class Player(object):



    def __init__(self,healthCap,mob,posx,posy,index,game):
        self.HEALTH_CAP = healthCap
        self._mobility = mob
        self.pos = Pos(posx,posy)
        self.index = index
        self.game = game
        self.health = healthCap
        self.myString = None
        self.equipment = None
    @property
    def mobility(self):
        return self._mobility
    @mobility.setter
    def mobility(self,mobility):
        self._mobility = mobility

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
        self.health += h
        return

    def decreaseHealth(self,h):
        self.health -= h
        if self.health <= 0:
            self.myString = 'C'+self.myString[0]
        return

    def getName(self):
        return self.myString

    def askForMove(self):
        print("Your health is " + str(self.health)+". Your position is (%d,%d). Your mobility is %d."%(self.pos.getX(),self.pos.getY(),self._mobility))
        print("You now have following options: \n1. Move\n2. Attack\n3. End the turn")
        a = int(raw_input())
        if a == 1:
            print("Specify your target position (Input 'x y').")
            posx,posy = map(int,raw_input().split(' '))
            if self.pos.distance(posx, posy) > self._mobility:
                print("Beyond your reach. Staying still.")
            elif self.game.positionOccupied(posx, posy):
                print("Position occupied. Cannot move there.")
            else:
                self.pos.setPos(posx, posy)
                self.game.printBoard()
                print("You can now \n1.attack\n2.End the turn")
                if int(raw_input())==1:
                    print("Input position to attack. (Input 'x y')")
                    attx,atty = map(int,raw_input().split(' '))
                    self.equipment.action(attx, atty)
        elif a == 2:
            print("Input position to attack.")
            attx, atty = map(int,raw_input().split(' '))
            self.equipment.action(attx, atty)
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
    def askForMove(self):
        print("You are a human (H%d) using Rifle. (Range %d, Ammo #: %d, Damage per shot: %d)"%(self.index,self.equipment.getRange(),self.equipment.getAmmo(),self.equipment.getEffect() ))
        super(Human,self).askForMove()

class Chark(Player):
    def __init__(self,posx,posy,index,game):
        super(Chark,self).__init__(100,4,posx,posy,index,game)
        self.myString = 'C' + str(index)
        self.equipment = Axe(self)

    def teleport(self):
        super(Chark,self).teleport()
        self.equipment.enhance()

    def askForMove(self):
        print("You are a Chark (C%d) using Axe. (Range: %d, Damage: %d)"%(self.index,self.equipment.getRange(),self.equipment.getEffect() ))
        super(Chark,self).askForMove()

class Obstacle(object):
    def __init__(self,posx,posy,index,game):
        self._pos = Pos(posx,posy)
        self.index = index
        self.game = game

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self,pos):
        self._pos = pos

    def getPos(self):
        return self._pos

    def teleport(self):
        randx = random.randint(0,self.game.D-1)
        randy = self.game.D - randx - 1
        while self.game.positionOccupied(randx, randy):
            randx = random.randint(0,self.game.D-1)
            randy = self.game.D - randx - 1
        self._pos.setPos(randx,randy)

class Pos(object):
    def __init__(self,x,y):
        self._x = x
        self._y = y
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,x):
        self._x = x
    @property
    def y(self):
        return self._y
    @x.setter
    def y(self,y):
        self._y = y

    def distance(self,*args):
        if len(args)==1 and isinstance(args[0],Pos):
            another = args[0]
            return abs(self._x - another.x) + abs(self._y - another.y)
        elif len(args)==2 and isinstance(args[0],int) and isinstance(args[1],int):
            x1 = args[0]
            y1 = args[1]
            return abs(self._x - x1) + abs(self._y - y1)



    def setPos(self,x,y):
        self._x = x
        self._y = y

    def getX(self):
        return self._x

    def getY(self):
        return self._y

class SurvivalGame(object):
    D = 10
    _O = 2
    def __init__(self):
        self._n = None
        self._teleportObjects = []
    @property
    def n(self):
        return self._n
    @n.setter
    def n(self,n):
        self._n = n
    @property
    def O(self):
        return self._O
    @O.setter
    def O(self,O):
        self._O = O
    @property
    def teleportObjects(self):
        return self._teleportObjects


    def printBoard(self):
        # init printObject
        printObject = [["  " for i in range(SurvivalGame.D)] for j in range(SurvivalGame.D)]

        for i in range(self.n):
            pos = self._teleportObjects[i].getPos()
            printObject[pos.getX()][pos.getY()] = (self._teleportObjects[i]).getName()

        for i in range(self.n,self.n+SurvivalGame._O):
            pos = (self._teleportObjects[i]).getPos()
            printObject[pos.getX()][pos.getY()] = "O" + str(i-self.n)

        firstLine = " "+"".join(["| %d  "%i for i in range(SurvivalGame.D)])+"|"
        print(firstLine+"\n"+"-"*int(SurvivalGame.D*5.5))
        for row in range(SurvivalGame.D):
            row_str = str(row)+''.join(['| %s '%(printObject[row][i]) for i in range(SurvivalGame.D)])+'|'
            print(row_str+"\n"+"-"*int(SurvivalGame.D*5.5))

    def positionOccupied(self,randx,randy):
        for o in self._teleportObjects:
            pos = o.getPos()
            if pos.getX() == randx and pos.getY() == randy:
                return True
        return False

    def getPlayer(self,randx,randy):
        for o in self._teleportObjects:
            if isinstance(o,Player):
                pos = o.getPos()
                if pos.getX() == randx and pos.getY() == randy:
                    return o
        return None

    def _init(self):
        print("Welcome to Kafustrok. Light blesses you. \nInput number of players: (a even number)")
        self.n = int(raw_input())
        no_obj = self.n + SurvivalGame._O
        self._teleportObjects = [None for i in range(no_obj)]
        for i in range(0,(self.n)/2):
            self._teleportObjects[i] = Human(0,0,i,self)
            self._teleportObjects[i+(self.n)/2] = Chark(0,0,i,self)
        for i in range(SurvivalGame._O):
            self._teleportObjects[i+self.n] = Obstacle(0,0,i,self)

    def _gameStart(self):
        turn = 0
        numOfAlivePlayers = self.n
        while numOfAlivePlayers > 1:
            # teleport after every N turns
            if turn == 0:
                for obj in self._teleportObjects:
                    obj.teleport()
                print("Everything gets teleported..")
            self.printBoard()
            t = self._teleportObjects[turn]
            if t.health > 0:
                t.askForMove()
                print("")
            turn = (turn + 1) % self.n
            numOfAlivePlayers = 0
            for i in range(self.n):
                if self._teleportObjects[i].health > 0:
                    numOfAlivePlayers += 1
        print("Game over.")
        self.printBoard()
game = SurvivalGame()
game._init()
game._gameStart()
