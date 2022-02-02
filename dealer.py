from hand import Hand


class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.name = "dealer"
        self.possessive = f"{self.name}'s"

    def act(self):
        return "stay" if self.hand.score >= 17 else "hit"
