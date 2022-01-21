from hand import Hand


class Dealer:
    def __init__(self, deck):
        self.deck = deck
        self.hand = Hand()
        self.name = "dealer"

    def deal(self):
        if len(self.deck.cards) == 0:
            raise Exception("no cards left in the deck")
        return self.deck.cards.pop(0)

    def act(self):
        return "stay" if self.hand.score >= 17 else "hit"
