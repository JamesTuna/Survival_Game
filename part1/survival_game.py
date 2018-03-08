#! /usr/bin/env python

import sys,abc,random

class Weapon(object):
    def __init__(self,range,damage,owner):
        self._range = range
        self._effect = damage
        self._owner = owner
    '''
    @property
    def range(self):
        return self._range
    @property
    def effect(self):
        return self._effect
    @property
    def owner(self):
        return self._owner
    @range.setter
    def range(self,range):
        self._range = range
    @effect.setter
    def effect(self,effect):
        self._effect = effect
    @owner.setter
    def owner(self,owner):
        self._owner = owner
    '''
    def getEffect(self):
        return self._effect
    def getRange(self):
        return self._range
    @abc.abstractmethod
    def action(self,posx,posy):
        return
    def enhance(self):
        return



class Axe(Weapon):
    __AXE_RANGE = 1
    __AXE_INIT_DAMAGE = 40

    def __init__(self,owner):
        super(Axe,self).__init__(Axe.__AXE_RANGE,Axe.__AXE_INIT_DAMAGE,owner)
        return

    def enhance(self):
        self._effect+=10

    def action(self,posx,posy):
        print("You are using axe attacking " + str(posx) + " " + str(posy) + ".")
        if self._owner._pos.distance(posx,posy) <= self._range:
            player = self._owner._game.getPlayer(posx, posy)
            if player != None:
                player.decreaseHealth(self._effect)
        else:
            print("Out of reach.")
        return

class Rifle(Weapon):
    __RIFLE_RANGE = 4
    __RIFLE_INIT_DAMAGE = 10;
    __AMMO_LIMIT = 6;
    __AMMO_RECHARGE = 3;

    def __init__(self,owner):
        super(Rifle,self).__init__(Rifle.__RIFLE_RANGE,Rifle.__RIFLE_INIT_DAMAGE,owner)
        self.__ammo = Rifle.__AMMO_LIMIT
        return
    '''
    @property
    def ammo(self):
        return self.__ammo
    @ammo.setter
    def ammo(self,ammo):
        self.__ammo = ammo
    '''
    def enhance(self):
        self.__ammo = min(Rifle.__AMMO_LIMIT,self.__ammo+Rifle.__AMMO_RECHARGE)
        return

    def action(self,posx,posy):
        print("You are using rifle attacking " + str(posx) + " " + str(posy) + ".")
        print("Type how many ammos you want to use.")
        ammoToUse = int(raw_input())
        if ammoToUse > self.__ammo:
            print("You don't have that ammos.")
            return
        if(self._owner._pos.distance(posx, posy) <= self._range):
            # search for all targets with target coordinates.
            player = self._owner._game.getPlayer(posx, posy)
            if player != None:
                player.decreaseHealth(self._effect * ammoToUse)
                self.__ammo -= ammoToUse
        else:
            print("Out of reach.")

    def getAmmo(self):
        return self.__ammo

class Player(object):



    def __init__(self,healthCap,mob,posx,posy,index,game):
        self.__mobility = mob
        self._pos = Pos(posx,posy)
        self._index = index
        self._game = game
        self._health = healthCap
        self._myString = None
        self._equipment = None
    '''
    @property
    def mobility(self):
        return self.__mobility
    @mobility.setter
    def mobility(self,mobility):
        self.__mobility = mobility
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self,new):
        self._pos = new
    @property
    def index(self):
        return self._index
    @index.setter
    def index(self,new):
        self._index = new
    @property
    def game(self):
        return self._game
    @game.setter
    def game(self,new):
        self._game = new
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self,new):
        self._health = new
    @property
    def myString(self):
        return self._myString
    @myString.setter
    def myString(self,new):
        self._myString = new
    @property
    def equipment(self):
        return self._equipment
    @equipment.setter
    def equipment(self,new):
        self._equipment = new
    '''

    def getPos(self):
        return self._pos

    def teleport(self):
        randx = random.randint(0,self._game.D-1)
        randy = random.randint(0,self._game.D-1)
        while self._game.positionOccupied(randx, randy):
            randx = random.randint(0,self._game.D-1)
            randy = random.randint(0,self._game.D-1)
        self._pos.setPos(randx,randy)
        return

    def increaseHealth(self,h):
        self._health += h
        return

    def decreaseHealth(self,h):
        self._health -= h
        if self._health <= 0:
            self._myString = 'C'+self._myString[0]
        return

    def getName(self):
        return self._myString

    def askForMove(self):
        print("Your health is " + str(self._health)+". Your position is (%d,%d). Your mobility is %d."%(self._pos.getX(),self._pos.getY(),self.__mobility))
        print("You now have following options: \n1. Move\n2. Attack\n3. End the turn")
        a = int(raw_input())
        if a == 1:
            print("Specify your target position (Input 'x y').")
            posx,posy = map(int,raw_input().split(' '))
            if self._pos.distance(posx, posy) > self.__mobility:
                print("Beyond your reach. Staying still.")
            elif self._game.positionOccupied(posx, posy):
                print("Position occupied. Cannot move there.")
            else:
                self._pos.setPos(posx, posy)
                self._game.printBoard()
                print("You can now \n1.attack\n2.End the turn")
                if int(raw_input())==1:
                    print("Input position to attack. (Input 'x y')")
                    attx,atty = map(int,raw_input().split(' '))
                    self._equipment.action(attx, atty)
        elif a == 2:
            print("Input position to attack.")
            attx, atty = map(int,raw_input().split(' '))
            self._equipment.action(attx, atty)
        elif a== 3:
            return

class Human(Player):
    def __init__(self,posx,posy,index,game):
        super(Human,self).__init__(80,2,posx,posy,index,game)
        self._myString = 'H' + str(index)
        self._equipment = Rifle(self)
    def teleport(self):
        super(Human,self).teleport()
        self._equipment.enhance()
    def askForMove(self):
        print("You are a human (H%d) using Rifle. (Range %d, Ammo #: %d, Damage per shot: %d)"%(self._index,self._equipment.getRange(),self._equipment.getAmmo(),self._equipment.getEffect() ))
        super(Human,self).askForMove()

class Chark(Player):
    def __init__(self,posx,posy,index,game):
        super(Chark,self).__init__(100,4,posx,posy,index,game)
        self._myString = 'C' + str(index)
        self._equipment = Axe(self)

    def teleport(self):
        super(Chark,self).teleport()
        self._equipment.enhance()

    def askForMove(self):
        print("You are a Chark (C%d) using Axe. (Range: %d, Damage: %d)"%(self._index,self._equipment.getRange(),self._equipment.getEffect() ))
        super(Chark,self).askForMove()

class Obstacle(object):
    def __init__(self,posx,posy,index,game):
        self.__pos = Pos(posx,posy)
        self.index = index
        self.__game = game
    '''
    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self,pos):
        self.__pos = pos
    @property
    def game(self):
        return self.__game
    @game.setter
    def game(self,new):
        self.__game = new
    '''
    def getPos(self):
        return self.__pos

    def teleport(self):
        randx = random.randint(0,self.__game.D-1)
        randy = self.__game.D - randx - 1
        while self.__game.positionOccupied(randx, randy):
            randx = random.randint(0,self.__game.D-1)
            randy = self.__game.D - randx - 1
        self.__pos.setPos(randx,randy)

class Pos(object):
    def __init__(self,x,y):
        self.__x = x
        self.__y = y
    '''
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,x):
        self.__x = x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,y):
        self.__y = y
    '''
    def distance(self,*args):
        if len(args)==1 and isinstance(args[0],Pos):
            another = args[0]
            return abs(self.__x - another.getX()) + abs(self.__y - another.getY())
        elif len(args)==2 and isinstance(args[0],int) and isinstance(args[1],int):
            x1 = args[0]
            y1 = args[1]
            return abs(self.__x - x1) + abs(self.__y - y1)



    def setPos(self,x,y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

class SurvivalGame(object):
    D = 10
    __O = 2
    def __init__(self):
        self.__n = None
        self.__teleportObjects = []
    '''
    @property
    def n(self):
        return self.__n
    @n.setter
    def n(self,n):
        self.__n = n
    @property
    def O(self):
        return self.__O
    @O.setter
    def O(self,O):
        self.__O = O
    @property
    def teleportObjects(self):
        return self.__teleportObjects
    @teleportObjects.setter
    def teleportObjects(self,new):
        self.__teleportObjects = new

    '''
    def printBoard(self):
        # init printObject
        printObject = [["  " for i in range(SurvivalGame.D)] for j in range(SurvivalGame.D)]

        for i in range(self.__n):
            pos = self.__teleportObjects[i].getPos()
            printObject[pos.getX()][pos.getY()] = (self.__teleportObjects[i]).getName()

        for i in range(self.__n,self.__n+SurvivalGame.__O):
            pos = (self.__teleportObjects[i]).getPos()
            printObject[pos.getX()][pos.getY()] = "O" + str(i-self.__n)

        firstLine = " "+"".join(["| %d  "%i for i in range(SurvivalGame.D)])+"|"
        print(firstLine+"\n"+"-"*int(SurvivalGame.D*5.5))
        for row in range(SurvivalGame.D):
            row_str = str(row)+''.join(['| %s '%(printObject[row][i]) for i in range(SurvivalGame.D)])+'|'
            print(row_str+"\n"+"-"*int(SurvivalGame.D*5.5))

    def positionOccupied(self,randx,randy):
        for o in self.__teleportObjects:
            pos = o.getPos()
            if pos.getX() == randx and pos.getY() == randy:
                return True
        return False

    def getPlayer(self,randx,randy):
        for o in self.__teleportObjects:
            if isinstance(o,Player):
                pos = o.getPos()
                if pos.getX() == randx and pos.getY() == randy:
                    return o
        return None

    def init(self):
        print("Welcome to Kafustrok. Light blesses you. \nInput number of players: (a even number)")
        self.__n = int(raw_input())
        no_obj = self.__n + SurvivalGame.__O
        self.__teleportObjects = [None for i in range(no_obj)]
        for i in range(0,(self.__n)/2):
            self.__teleportObjects[i] = Human(0,0,i,self)
            self.__teleportObjects[i+(self.__n)/2] = Chark(0,0,i,self)
        for i in range(SurvivalGame.__O):
            self.__teleportObjects[i+self.__n] = Obstacle(0,0,i,self)

    def gameStart(self):
        turn = 0
        numOfAlivePlayers = self.__n
        while numOfAlivePlayers > 1:
            # teleport after every N turns
            if turn == 0:
                for obj in self.__teleportObjects:
                    obj.teleport()
                print("Everything gets teleported..")
            self.printBoard()
            t = self.__teleportObjects[turn]
            if t._health > 0:
                t.askForMove()
                print("")
            turn = (turn + 1) % self.__n
            numOfAlivePlayers = 0
            for i in range(self.__n):
                if self.__teleportObjects[i]._health > 0:
                    numOfAlivePlayers += 1
        print("Game over.")
        self.printBoard()
game = SurvivalGame()
game.init()
game.gameStart()
