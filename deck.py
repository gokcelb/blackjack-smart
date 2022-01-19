import random


class Deck:
    def __init__(self):
        self.cards = []
        self.scores = {}
        self.init()

    def init(self):
        suits = [u"\u2666", u"\u2665", u"\u2663", u"\u2660"]
        values = ["A", "2", "3", "4", "5", "6",
                  "7", "8", "9", "T", "J", "Q", "K"]
        scores_for_values = {"A": {"small": 1, "big": 11}, "2": 2, "3": 3, "4": 4,
                             "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 10, "Q": 10, "K": 10}

        for suit in suits:
            for value in values:
                self.cards.append(value + suit)

        for card in self.cards:
            value = card[0]
            self.scores[card] = scores_for_values[value]

    def shuffle(self):
        random.shuffle(self.cards)
