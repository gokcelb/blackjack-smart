class Hand:
    def __init__(self):
        self.hand = []
        self.score = 0

    def calculate_score(self):
        self.score = 0
        aces = []
        for card in self.hand:
            value = card.get_score()
            if type(value) is dict:
                aces.append(value)
                continue
            self.score += value

        for ace in aces:
            value = ace["small"] if ace["big"] + self.score > 21 else ace["big"]
            self.score += value

    def add(self, dealt_card):
        self.hand.append(dealt_card)

    def empty(self):
        self.hand = []
        self.score = 0
