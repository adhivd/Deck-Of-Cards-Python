from deckofcards import Card
from deckofcards import Deck
import time
import os
import numbers
import sys

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

        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=35, cols=100))
        print("Resizing")
        time.sleep(0.5)
        print("Clearing")
        os.system('cls' if os.name == 'nt' else 'clear')
        begin = input("Hi! Welcome to Memory, the card game. Here are the rules: \n 👉🏼 The game is single player \n 👉🏼 There will a deck of cards spread out, face down, in a 4x13 grid  \n 👉🏼 Each turn, you select two cards to be face up (prompted for each card one at a time) \n 🎉 If the pair of cards has the same suit or value, they are 'matched' and stay face up \n 🚫 Else, they go face down and you move on to the next turn \n Examples: \n K♣️  and K♥️  works ✅  \n K♥️  and 4♥️  works ✅  \n K♣️  and 4♥️  does not ❌  \n 👉🏼 Your goal is to turn all the cards face up in the fewest number of turns possible \n Note: I'd highly suggest widening / heightening your terminal window \n \nWould you like to begin? [y/n] \n")

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
            if firstCard == 'god mode':
                self.showAnswerGrid()
                continue
            if firstCard == 'exit':
                self.showAnswerGrid()
                return
            self.showGrid(firstCard)
            secondCard = self.askForRowCol(firstCard)
            if secondCard == 'god mode':
                self.showAnswerGrid()
                continue
            if secondCard == 'exit':
                self.showAnswerGrid()
                return
            self.showGrid(firstCard, secondCard)
            self.checkTurn(firstCard, secondCard)
            self.turns += 1
        print("Congratulations! You win 🚀")

    def askForRowCol(self, firstCard=None):
        if not firstCard:
            rowcol = input("Select the row and column of the first card you'd like to turn over. Format: Row/Column (e.g. 8/a) \n")
        else:
            rowcol = input("Found the {}  card! Select the row and column of the next card you'd like to turn over. Format: Row/Column (e.g. 8/a) \n".format(self.answerGrid[firstCard[0]][firstCard[1]]))

        validInputs = ["a","b","c","d"]
        doneChecking = False
        while not doneChecking:
            if rowcol == "god mode" or rowcol == "exit":
                return rowcol
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
            print("🎉 Congrats! You've matched the {}  and {}  cards. Moving on to next turn".format(c1,c2))
            self.score += 1
            time.sleep(3)
        else:
            print("🚫 Incorrect Match! The pair you've selected ({}  and {}  ) will be turned face down in a few seconds . . .".format(c1,c2))
            self.userGrid[firstCard[0]][firstCard[1]] = "🃏"
            self.userGrid[secondCard[0]][secondCard[1]] = "🃏"
            time.sleep(4)


    def showGrid(self, firstCard=None, secondCard=None):
        os.system('cls' if os.name == 'nt' else 'clear')

        row = 1
        # for c in range(4):
        #     print
        print("      columns")
        print("row   a   b   c   d")
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

        print("Turn {}  |  Pairs matched: {}  \nType 'god mode' to see the answers | Type 'exit' to exit \n ".format(self.turns, self.score))

    def showAnswerGrid(self):
        row = 1

        print("      columns")
        print("row   a  b  c  d")
        for r in self.answerGrid:
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
