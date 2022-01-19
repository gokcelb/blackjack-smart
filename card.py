class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit
        
    def get_score(self):
        tens = ["T", "J", "Q", "K"]
        if self.face == "A":
            return {"small": 1, "big": 11}
        elif self.face in tens:
            return 10
        else:
            return int(self.face)

    def __str__(self):
        return self.face + self.suit