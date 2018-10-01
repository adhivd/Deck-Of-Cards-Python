from deckofcards import Card
from deckofcards import Deck
import time
import os
import numbers
import sys

class Game(object):
    def __init__(self, begin=None):
        self.cardGrid = None
        self.score = 0
        self.turns = 1
        begin = self.intro()
        if(begin == "y" or begin == "yes"):
            self.setup()
            self.runGame()
        else:
            print("Goodbye!")
            return

    # Reformats the terminal, clears the output, and introduces game rules
    def intro(self):
        validInputs = ["y","n","yes","no"]
        self.resizeTerminal()
        print("Resizing")
        time.sleep(0.5)
        print("Clearing")
        os.system('cls' if os.name == 'nt' else 'clear')
        begin = input("Hi! Welcome to Memory, the card game. Here are the rules: \n 👉🏼 The game is single player \n 👉🏼 There will a deck of cards spread out, face down, in a 4x13 grid  \n 👉🏼 Each turn, you select two cards to be face up (prompted for each card one at a time) \n 🎉 If the pair of cards has the same suit or value, they are 'matched' and stay face up \n 🚫 Else, they go face down and you move on to the next turn \n Examples: \n K♣️  and K♥️  works ✅  \n K♥️  and 4♥️  works ✅  \n K♣️  and 4♥️  does not ❌  \n 👉🏼 Your goal is to turn all the cards face up in the fewest number of turns possible \n Note: I'd highly suggest widening / heightening your terminal window \n \nWould you like to begin? [y/n] \n")

        while (begin not in validInputs):
            begin = input("Sorry, I didn't catch that. Would you like to begin? [y/n] \n")
        return begin

    # initial setup that creates the grid and Deck object containing the Card objects
    def setup(self):
        print("Grabbing a fresh deck of cards . . .")

        deck = Deck(True) # passing true will make all the cards face down initially
        time.sleep(0.5)
        print("Shuffling . . .")
        deck.shuffle() # randomly order all cards in the deck

        # create the cardGrid and place all the cards one by one into a 4 x 13 2-d list
        self.cardGrid = [[deck.deal() for _ in range(4)] for _ in range(13)]

        # buzz words to impress the VC's
        time.sleep(0.5)
        print("Initializing the blockchain . . .")
        time.sleep(0.5)
        print("Booting up the A.I. . . . \n")
        time.sleep(0.5)
        print("Let's play!")
        time.sleep(1)

    # Runs the game until the user achieves 26 pairs. Each iteration of the while loop is a turn
    def runGame(self):
        # print out instructions
        while self.score != 26:
            # init
            self.showGrid()

            # first card prompt + actions
            firstCard = self.askForRowCol()
            if firstCard == 'god mode':
                self.showGrid(None,None,True)
                continue
            self.showGrid(firstCard)

            # second card prompt + actions
            secondCard = self.askForRowCol(firstCard)
            if secondCard == 'god mode':
                firstCard.flip() # nice try...
                self.showGrid(None,None,True)
                continue
            self.showGrid(firstCard, secondCard)

            # check the cards and move on to the next turn
            self.checkTurn(firstCard, secondCard)
            self.turns += 1
        print("Congratulations! You win 🚀")

    # takes in the user input for row/column. very long since multiple checks have to be made to ensure the correct formatting
    def askForRowCol(self, firstCard=None):
        if not firstCard:
            rowcol = input("Select the row and column of the first card you'd like to turn over. Format: Row/Column (e.g. 8/a) \n")
        else:
            rowcol = input("Found the {}  card! Select the row and column of the next card you'd like to turn over. Format: Row/Column (e.g. 8/a) \n".format(firstCard))

        validInputs = ["a","b","c","d"]
        doneChecking = False
        while not doneChecking:
            if rowcol == "god mode" or rowcol == "exit":
                return rowcol
            if rowcol == "exit":
                self.showGrid(None,None,True)
                return
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
            if firstCard and firstCard == self.getCard(coords):
                rowcol = input("You've inputted the row and column for the first card you flipped over! Please enter another row/column: \n")
                continue
            if coords[0] < 0 or coords[0] > 12:
                rowcol = input("Please check your row number and enter another row/column: \n")
                continue
            if not self.isCardFaceDown(coords):
                rowcol = input("You've already checked that card! Please enter another row/column: \n")
                continue
            doneChecking = True
        return self.getCard(coords)

    # convert from 1-index rows and column letters to 0-index rows/cols
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

    # returns true/false if card is face down / up based on grid coordinates
    def isCardFaceDown(self, coords):
        card = self.getCard(coords)
        return card.faceDown

    # checks if two cards in a turn are equal and deals the appropriate result to the user
    def checkTurn(self, firstCard, secondCard):
        c1 = firstCard
        c2 = secondCard

        if c1.value == c2.value or c1.suit == c2.suit:
            self.score += 1
            print("🎉 Congrats! You've matched the {}  and {}  cards. Moving on to next turn".format(c1,c2))
            time.sleep(3)
        else:
            print("🚫 Incorrect Match! The pair you've selected ({}  and {}  ) will be turned face down in a few seconds . . .".format(c1,c2))
            c1.flip()
            c2.flip()
            time.sleep(4)

    # any time the grid needs to be shown, this method is called
    # firstCard and secondCard parameters are the card objects that should be shown (if passed in)
    # godMode is for when the user would like to see the answers
    def showGrid(self, firstCard=None, secondCard=None, godMode=False):
        # clears the terminal output
        self.clearTerminal()
        row = 1

        # formatting for the top
        print("\n")
        print("      columns")
        print("      a   b   c   d")
        print("row")

        if firstCard and secondCard:
            # first card has already been flipped
            secondCard.flip()
        elif firstCard:
            firstCard.flip()
        for r in self.cardGrid:
            if(row < 10):  # formatting purposes since double digits take up more space
                print('{}     '.format(row), end='')
            else:
                print('{}    '.format(row), end='')
            for c in r:
                if godMode:
                    print("{}  ".format(c.show(True)), end='')
                else:
                    print("{}  ".format(c), end='')
            print("\n")
            row += 1

        print("⮑  Turn {}  | 🎉 Pairs matched: {}  \nType god mode and scroll up to see answers | Type 'exit' to exit\n ".format(self.turns, self.score))

    # Gets a card object based on corrected grid coordinates
    def getCard(self, coords):
        row = coords[0]
        col = coords[1]
        card = self.cardGrid[row][col]
        return card

    # clears the terminal of all previous text + emojis
    def clearTerminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # resizes the terminal for optimal playability
    def resizeTerminal(self):
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=100))

# starts the game
game = Game()
