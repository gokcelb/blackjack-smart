from player import Player


class AI(Player):
    instances = 0

    def __init__(self, hand, funds):
        super().__init__(hand, funds)
        AI.instances += 1
        self.name = f"player{str(AI.instances)}"

    def act(self, dealer_hand):
        has_ace = False
        for card in self.hand:
            if type(card.get_score()) is dict:
                has_ace = True

        hand_type = "hard"
        if has_ace:
            hand_type = "soft"

        self.check_hand(hand_type, dealer_hand)

    def check_hand(self, hand_type, dealer_hand):
        if 2 <= dealer_hand.calculate_score() <= 6:
            return self.low_dealer_hand(hand_type)
        else:
            return self.high_dealer_hand(hand_type)

    def low_dealer_hand(self, hand_type):
        score = self.hand.calculate_score()
        if hand_type == "hard":
            return "hit" if 4 <= score <= 11 else "stay"
        else:
            return "hit" if 13 <= score <= 18 else "stay"

    def high_dealer_hand(self, hand_type):
        score = self.hand.calculate_score()
        if hand_type == "hard":
            return "hit" if 4 <= score <= 16 else "stay"
        else:
            return "hit" if 13 <= score <= 18 else "stay"

    def bet(self):
        if 0 < self.funds < 800:
            return self.funds / 2
        elif 800 <= self.funds <= 1500:
            return self.funds
        else:
            return self.funds / 3 * 2
        
