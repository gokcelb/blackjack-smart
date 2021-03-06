import random
from player import Player


class AIPlayer(Player):
    instances = 0

    def __init__(self):
        super().__init__()
        AIPlayer.instances += 1
        self.name = f"player{str(AIPlayer.instances)}"
        self.possessive = f"{self.name}'s"

    def make_bet(self):
        coefficients = [1, 1/2, 1/3, 1/4, 1/5, 2/3, 3/4, 2/5, 3/5, 4/5]
        self.bet = round(self.funds * random.choice(coefficients), 2)
        
    def act(self, dealer_hand_score):
        has_ace = False
        for card in self.hand.cards:
            if type(card.get_score()) is dict:
                has_ace = True

        hand_type = "hard"
        if has_ace:
            hand_type = "soft"

        return self.check_hand(hand_type, dealer_hand_score)

    def check_hand(self, hand_type, dealer_hand_score):
        if 2 <= dealer_hand_score <= 6:
            return self.low_dealer_hand(hand_type)
        else:
            return self.high_dealer_hand(hand_type)

    def low_dealer_hand(self, hand_type):
        if hand_type == "hard":
            return "hit" if 4 <= self.hand.score <= 11 else "stay"
        else:
            return "hit" if 13 <= self.hand.score <= 18 else "stay"

    def high_dealer_hand(self, hand_type):
        if hand_type == "hard":
            return "hit" if 4 <= self.hand.score <= 16 else "stay"
        else:
            return "hit" if 13 <= self.hand.score <= 18 else "stay"
