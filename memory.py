from deckofcards import Card
from deckofcards import Deck
import time
import os
import numbers

# myDeck = Deck()
# myDeck.shuffle()
# myDeck.show()

class Game(object):
    def __init__(self):
        self.answerGrid = None
        self.score = 0
        self.turns = 1
        begin = self.intro()
        if(begin == "y" or begin == "yes"):
            self.setup()
            self.start()
        else:
            print("Goodbye!")
            return

    def intro(self):
        validInputs = ["y","n","yes","no"]
        os.system('cls' if os.name == 'nt' else 'clear')
        begin = input("Hi! Welcome to Memory. Would you like to begin? [y/n] \n")

        while (begin not in validInputs):
            begin = input("Sorry, I didn't catch that. Would you like to begin? [y/n] \n")
        return begin

    def setup(self):
        print("Grabbing a fresh deck of cards . . .")
        deck = Deck()
        time.sleep(0.5)
        print("Shuffling . . .")
        deck.shuffle()

        self.answerGrid = [[deck.deal() for _ in range(4)] for _ in range(13)]
        # print(self.answerGrid)
        self.userGrid = [["🃏" for _ in range(4)] for _ in range(13)]
        # self.showGrid()

        time.sleep(0.5)
        print("Initializing the blockchain . . .")
        time.sleep(0.5)
        print("Booting up the A.I. . . . \n")
        time.sleep(0.5)
        print("Let's play!")
        time.sleep(1)

    def start(self):
        # print out instructions
        while self.score != 26:
            self.showGrid()
            firstCard = self.askForRowCol()
            self.showGrid(firstCard)
            secondCard = self.askForRowCol(firstCard)
            self.showGrid(firstCard, secondCard)
            self.checkTurn(firstCard, secondCard)
            self.turns += 1

    def askForRowCol(self, firstCard=None):
        rowcol = input("Select the row and column of the first card you'd like to turn over. Format: Row/Column (e.g. 8/a) \n")
        validInputs = ["a","b","c","d"]
        doneChecking = False
        while not doneChecking:
            if "/" not in rowcol[:]:
                rowcol = input("Please make sure to include a / in your format between Row and Column (e.g. 8/a) \n")
                continue
            row = rowcol.split("/")[0]
            col = rowcol.split("/")[1]
            try:
                row = int(row)
            except:
                rowcol = input("Please enter a number for your row (e.g. Row 8 and Column a would be 8/a) \n")
                continue
            if not isinstance(row, numbers.Number) or col not in validInputs:
                rowcol = input("Sorry, I didn't catch that! Please format your row column selection as Row/Column (e.g. Row 8 and Column a would be 8/a) \n")
                continue
            coords = self.convertRowColIntoCoordinates(int(row), col)
            if firstCard and firstCard == coords:
                rowcol = input("You've inputted the row and column for the first card you flipped over! Please enter another row/column: \n")
                continue
            if coords[0] < 0 or coords[0] > 12:
                rowcol = input("Please check your row number and enter another row/column: \n")
                continue
            if self.isCardFlipped(coords):
                rowcol = input("You've already checked that card! Please enter another row/column: \n")
                continue
            doneChecking = True
        return coords

    def convertRowColIntoCoordinates(self, row, col):

        r = row - 1
        if col == "a":
            c = 0
        elif col == "b":
            c = 1
        elif col =="c":
            c = 2
        else:
            c = 3

        return [r,c]

    def isCardFlipped(self, coords):
        if self.userGrid[coords[0]][coords[1]] == "🃏":
            return False
        else:
            return True

    def checkTurn(self, firstCard, secondCard):
        c1 = self.answerGrid[firstCard[0]][firstCard[1]]
        c2 = self.answerGrid[secondCard[0]][secondCard[1]]

        if c1.value == c2.value or c1.suit == c2.suit:
            print("🎉 Congrats! You've matched the {} and {} cards. Moving on to next turn".format(c1,c2))
            self.score += 1
            time.sleep(3)
        else:
            print("🚫 Incorrect Match! The pair you've selected will be turned face down in a few seconds . . .")
            self.userGrid[firstCard[0]][firstCard[1]] = "🃏"
            self.userGrid[secondCard[0]][secondCard[1]] = "🃏"
            time.sleep(4)


    def showGrid(self, firstCard=None, secondCard=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Turn {}  |  Pairs matched: {} ".format(self.turns, self.score))
        row = 1
        col = 1
        # for c in range(4):
        #     print
        print("      col")
        print("row   a  b  c  d")
        if firstCard:
            self.userGrid[firstCard[0]][firstCard[1]] = self.answerGrid[firstCard[0]][firstCard[1]]
        if secondCard:
            self.userGrid[secondCard[0]][secondCard[1]] = self.answerGrid[secondCard[0]][secondCard[1]]
        # self.userGrid[2][1] = "A♥️"
        # self.userGrid[2][2] = "A♥️"
        for r in self.userGrid:
            if(row < 10):
                print('{}     '.format(row), end='')
            else:
                print('{}    '.format(row), end='')

            for c in r:
                if(c == "🃏"):
                    print("{}  ".format(c), end='')
                else:
                    print("{}  ".format(c), end='')
            print("\n")
            row += 1






game = Game()
