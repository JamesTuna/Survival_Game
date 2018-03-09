#! /usr/bin/env python
from __future__ import print_function
import sys,abc,random
class Gomoku(object):
    # class variable storing all 140 win patterns
    win_patterns = []
    # class method generate all 140 win patterns
    def generate_pattern(cls):
        pattern_list=[]
        # in row:
        for row in range(0,9):
            for col in range(0,5):
                pattern_list.append([(row,col+i) for i in range(0,5)])
        # in column:
        for col in range(0,9):
            for row in range(0,5):
                pattern_list.append([(row+i,col) for i in range(0,5)])
        # in diagnal \:
        for row in range(0,5):
            for col in range(0,5):
                pattern_list.append([(row+i,col+i) for i in range(0,5)])
        # in diagnal /:
        for row in range(4,9):
            for col in range(4,9):
                pattern_list.append([(row-i,col-i) for i in range(0,5)])
        return pattern_list

    def match_pattern(self,symbol):
        for pattern in self.win_patterns:
            matched = True
            for x,y in pattern:
                if not self.gameBoard[x][y] == symbol:
                    matched = False
                    break
            if matched:
                return pattern
        return []

    def __init__(self):
        # initialize class variable win_patterns
        self.win_patterns = self.generate_pattern()
        # initialize gameBoard
        self.gameBoard = [[' ' for row in range(1,10)] for col in range(1,10)]
        # create two players
        while(True):
            print("Please choose player 1 (O):\n1. Human\n2. Computer Player")
            choice = raw_input("Your choice is: ")
            choice = int(choice)
            if not choice == 1 and not choice == 2:
                print("invalid input")
                continue
            if choice == 1:
                print("Player O is Human.\n")
            else:
                print("Player O is Computer.\n")
            self.player1 = self.createPlayer('O',choice)
            break

        while(True):
            print("Please choose player 2 (X):\n1. Human\n2. Computer Player")
            choice = raw_input("Your choice is: ")
            choice = int(choice)
            if not choice == 1 and not choice == 2:
                print("invalid input")
                continue
            if choice == 1:
                print("Player X is Human.\n")
            else:
                print("Player X is Computer.\n")
            self.player2 = self.createPlayer('X',choice)
            break
        # initialize first turn as player O
        self.turn = self.player1

    # Create a player with symbol='O' or 'X'
    # playerNum = 1 --> Human
    # playerNum = 2 --> Computer
    def createPlayer(self,symbol,playerNum):
        if playerNum == 1:
            return Human(symbol,self.gameBoard)
        elif playerNum == 2:
            return Computer(symbol,self.gameBoard)


    # Start a new game and play until winning/losing or draw
    def startGame(self):

        while(self.checkWin()==False and self.checkTie() == False):
            self.printGameBoard()
            print("")
            self.turn.nextMove()
            self.switchTurn()
        self.printGameBoard()

        if self.checkWin():
            self.switchTurn()
            print("%s wins!"%(self.turn))
        else:
            print("Draw game!")
        line = self.match_pattern(self.turn.symbol)
        line = [str((x+1,y+1)) for x,y in line]
        print("line: "+' '.join(line))
        return


    def printGameBoard(self):
        # Print out the game board in the command line window
        dash_sep = '-'*38
        for row in range(0,10):
            if row == 0:
                row_str = ' | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |'
                print(row_str)
                print(dash_sep)
            else:
                row_str = str(row)+'| '+' | '.join(self.gameBoard[row-1])+' |'
                print(row_str+"\n"+dash_sep)
        return

    def checkWin(self):
        # Check if any player has won the game
        if self.match_pattern('O') or self.match_pattern('X'):
            return True
        return False


    def checkTie(self):
        # Check if the game is ending in a tie
        if self.checkWin() == True:
            return False
        for row in range(0,9):
            for col in range(0,9):
                if self.gameBoard[row][col] == ' ':
                    return False
        return True

    def switchTurn(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1
        return

class Player(object):
    def __init__(self,symbol,gameBoard):
        self.symbol = symbol
        self.gameBoard = gameBoard
    def __str__(self):
        return "Player "+str(self.symbol)
    @abc.abstractmethod
    def nextMove(self):
        # abstract method, implemented by subclasses
        return
class Human(Player):
    def nextMove(self):
        # Human class implementation of nextMove method
        print("Player %c's turn!"%self.symbol)
        while(True):
            x,y = map(int,raw_input("Type the row and col to put the disc: ").split(' '))
            if 0 < x and x < 10 and 0 < y and y < 10:
                if self.gameBoard[x-1][y-1] == ' ':
                    self.gameBoard[x-1][y-1] = self.symbol
                    print('Player %c place at %d %d'%(self.symbol,x,y))
                    return
            print("invalid position, please enter agin!")


class Computer(Player):
    def nextMove(self):
        print("Player %c's turn!"%self.symbol)
        # Computer class implementation of nextMove method
        can_place = []
        for row in range(0,9):
            for col in range(0,9):
                if self.gameBoard[row][col] == ' ':
                    can_place.append((row,col))
        choice = random.randint(0,len(can_place)-1)
        x,y = can_place[choice]
        self.gameBoard[x][y] = self.symbol
        print('Player %c place at %d %d'%(self.symbol,x+1,y+1))
        return

game = Gomoku()
game.startGame()
