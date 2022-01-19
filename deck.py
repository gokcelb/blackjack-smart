import random
from card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.init()

    def init(self):
        suits = [u"\u2666", u"\u2665", u"\u2663", u"\u2660"]
        faces = ["A", "2", "3", "4", "5", "6",
                 "7", "8", "9", "T", "J", "Q", "K"]

        for suit in suits:
            for face in faces:
                card = Card(face, suit)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)
