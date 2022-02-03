from player import Player


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.name = "you"
        self.possessive = "your"

    def make_bet(self):
        self.bet = int(input("Place your bet: $"))
        while self.bet > self.funds:
            print("You do not have sufficient funds")
            self.bet = int(input("Place your bet: $"))

    def act(self, dealer_hand_score):
        action = input("Would you like to hit or stay? ")
        while action.lower() != "hit" and action.lower() != "stay":
            print("That is not a valid option.")
            action = input("Would you like to hit or stay? ")
        return action
