class Game:
    def __init__(self, dealer, player):
        self.dealer = dealer
        self.player = player

    def play(self):
        while self.player.funds > 0:
            game_starts = input(
                f"You are starting with {self.player.funds}. Would you like to play a hand? ")
            while game_starts != "no" and game_starts != "yes":
                print("That is not a valid option")
                game_starts = input(
                    f"You are starting with {self.player.funds}. Would you like to play a hand? ")
            if game_starts.lower() == "no":
                return

            while True:
                bet = self.ask_bet()
                self.opening(self.player)
                self.opening(self.dealer)
                self.check_for_blackjack(bet)
                if self.player_plays(bet) == "busted" or self.dealer_plays(bet) == "busted":
                    break
                self.check_for_winner(bet)
                break

            self.reset()

        print("You've ran out of money. Please restart this program to try again. Goodbye.")

    def opening(self, who):
        first_two_cards = [self.dealer.deal(), self.dealer.deal()]
        who.hand.extend(first_two_cards)
        self.calculate_hand_value(who)
        if who == self.player:
            print(f"You are dealt: {', '.join(first_two_cards)}")
        else:
            print(f"The dealer is dealt: {first_two_cards[0]}, Unknown")

    def deal(self, who):
        try:
            dealt_card = self.dealer.deal()
            who.hand.append(dealt_card)
            self.calculate_hand_value(who)
            return dealt_card
        except Exception as err:
            print(err)

    def display_hand(self, who):
        if who == self.player:
            print(f"You know have: {', '.join(who.hand)}")
        else:
            print(f"The dealer has: {', '.join(who.hand)}")

    def calculate_hand_value(self, who):
        total = 0
        aces = []
        for card in who.hand:
            score = self.dealer.deck.scores[card]
            if type(score) is dict:
                aces.append(score)
                continue
            total += score

        for ace in aces:
            score = ace["small"] if ace["big"] + total > 21 else ace["big"]
            total += score

        who.hand_value = total

    def check_for_blackjack(self, bet):
        if self.player.hand_value == 21:
            print(f"Blackjack! You win ${bet + bet / 2}." if self.dealer.hand_value !=
                  21 else "You tie. Your bet has been returned.")
            self.player.funds += bet + bet / 2

    def check_for_busted(self, bet):
        if self.dealer.hand_value > 21:
            print(f"The dealer busts, you win ${bet}")
            self.player.funds += bet
            return True

        if self.player.hand_value > 21:
            print(f"Your hand value is over 21 and you lose ${bet}")
            self.player.funds -= bet
            return True

    def check_for_winner(self, bet):
        if self.dealer.hand_value == self.player.hand_value:
            print("You tie. Your bet has been returned.")
        elif self.dealer.hand_value > self.player.hand_value:
            print(f"The dealer wins, you lose ${bet}.")
            self.player.funds -= bet
        else:
            print(f"You win ${bet}!")
            self.player.funds += bet

    def player_plays(self, bet):
        player_action = input("Would you like to hit or stay? ")
        while player_action.lower() != "hit" and player_action.lower() != "stay":
            print("That is not a valid option.")
            player_action = input("Would you like to hit or stay? ")

        while player_action.lower() == "hit":
            self.deal(self.player)
            self.display_hand(self.player)
            if self.check_for_busted(bet):
                return "busted"
            player_action = input("Would you like to hit or stay? ")

    def dealer_plays(self, bet):
        self.display_hand(self.dealer)
        dealer_action = self.dealer.act()
        while dealer_action == "hit":
            print(f"The dealer hits and is dealt: {self.deal(self.dealer)}")
            self.display_hand(self.dealer)
            if self.check_for_busted(bet):
                return "busted"

        print("The dealer stays.")

    def ask_bet(self):
        bet = int(input("Place your bet: "))
        while bet > self.player.funds:
            print("You do not have sufficient funds.")
            bet = int(input("Place your bet: "))
        return bet

    def reset(self):
        self.dealer.deck.cards.extend(self.dealer.hand + self.player.hand)
        self.dealer.deck.shuffle()

        self.dealer.hand = []
        self.dealer.hand_value = 0
        self.player.hand = []
        self.player.hand_value = 0
