class Player:
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.funds = 500

    def __str__(self):
        return f"${self.funds}"
