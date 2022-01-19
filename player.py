from hand import Hand


class Player:
    def __init__(self):
        self.hand = Hand()
        self.funds = 500
        self.name = "You"

    def __str__(self):
        return f"${self.funds}"
