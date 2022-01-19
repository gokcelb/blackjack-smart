import random


class Deck:
    def __init__(self, cards, scores):
        self.cards = cards
        self.scores = scores

    def shuffle(self):
        random.shuffle(self.cards)
