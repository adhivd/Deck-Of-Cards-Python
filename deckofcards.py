import random

class Card(object):
    def __init__(self, suit, val, faceDown=False):
        self.suit = suit
        self.value = val
        self.faceDown = faceDown

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()

    # showFace = True will show the real value of a card
    def show(self, showFace=False):
        if self.faceDown and not showFace:
            return "🃏"
        if self.value == 1:
            val = "A"
        elif self.value == 11:
            val = "J"
        elif self.value == 12:
            val = "Q"
        elif self.value == 13:
            val = "K"
        else:
            val = self.value

        return "{}{}".format(val, self.suit)

    def flip(self):
        self.faceDown = not self.faceDown


class Deck(object):
    def __init__(self,faceDown=False):
        self.cards = []
        self.build(faceDown)

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print(card.show())

    # Generate 52 cards
    def build(self,faceDown=False):
        self.cards = []
        for suit in ['♥️', '♣️', '♦️', '♠️']:
            for val in range(1,14):
                self.cards.append(Card(suit, val, faceDown))

    # Shuffle the deck
    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
            # You can also use the build in shuffle method
            # random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        return self.cards.pop()

# Test making a Card
# card = Card('Spades', 6)
# print card
