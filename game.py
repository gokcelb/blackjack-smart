import time


class Game:
    def __init__(self, deck, dealer, player):
        self.deck = deck
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
                time.sleep(1)
                bet = self.ask_bet()
                time.sleep(1)
                self.opening(self.player)
                time.sleep(1)
                self.opening(self.dealer)
                if self.check_for_blackjack(bet):
                    break
                time.sleep(1)
                if self.player_plays(bet) == "busted" or self.dealer_plays(bet) == "busted":
                    break
                self.check_for_winner(bet)
                break

            self.reset()

        print("You've ran out of money. Please restart this program to try again. Goodbye.")

    def opening(self, who):
        who.hand.add(self.dealer.deal())
        who.hand.add(self.dealer.deal())
        who.hand.calculate_score()
        if who == self.player:
            print(f"You are dealt: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")
        else:
            print(f"The dealer is dealt: {who.hand.hand[0]}, Unknown")

    def deal(self, who):
        try:
            dealt_card = self.dealer.deal()
            who.hand.add(dealt_card)
            who.hand.calculate_score()
            return dealt_card
        except Exception as err:
            print(err)

    def announce_hand(self, who):
        if who == self.player:
            print(f"You know have: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")
        else:
            print(f"The dealer has: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")

    def check_for_blackjack(self, bet):
        if self.player.hand.score == 21:
            if self.dealer.hand.score != 21:
                time.sleep(1)
                print(f"Blackjack! You win ${bet + bet / 2}.")
                self.player.funds += bet + bet / 2
            else:
                time.sleep(1)
                print("You tie. Your bet has been returned.")
            return True

    def check_for_busted(self, bet):
        if self.dealer.hand.score > 21:
            time.sleep(1)
            print(f"The dealer busts, you win ${bet}")
            self.player.funds += bet
            return True

        if self.player.hand.score > 21:
            time.sleep(1)
            print(f"Your hand value is over 21 and you lose ${bet}")
            self.player.funds -= bet
            return True

    def check_for_winner(self, bet):
        if self.dealer.hand.score == self.player.hand.score:
            time.sleep(1)
            print("You tie. Your bet has been returned.")
        elif self.dealer.hand.score > self.player.hand.score:
            time.sleep(1)
            print(f"The dealer wins, you lose ${bet}.")
            self.player.funds -= bet
        else:
            time.sleep(1)
            print(f"You win ${bet}!")
            self.player.funds += bet

    def player_plays(self, bet):
        player_action = input("Would you like to hit or stay? ")
        while player_action.lower() != "hit" and player_action.lower() != "stay":
            print("That is not a valid option.")
            time.sleep(1)
            player_action = input("Would you like to hit or stay? ")

        while player_action.lower() == "hit":
            self.deal(self.player)
            self.announce_hand(self.player)
            if self.check_for_busted(bet):
                return "busted"
            time.sleep(1)
            player_action = input("Would you like to hit or stay? ")

    def dealer_plays(self, bet):
        self.announce_hand(self.dealer)
        dealer_action = self.dealer.act()
        while dealer_action == "hit":
            print(f"The dealer hits and is dealt: {self.deal(self.dealer)}")
            time.sleep(2)
            self.announce_hand(self.dealer)
            if self.check_for_busted(bet):
                return "busted"
            dealer_action = self.dealer.act()

        print("The dealer stays.")

    def ask_bet(self):
        bet = int(input("Place your bet: "))
        while bet > self.player.funds:
            print("You do not have sufficient funds.")
            bet = int(input("Place your bet: "))
        return bet

    def reset(self):
        self.dealer.deck.cards.extend(self.dealer.hand.hand + self.player.hand.hand)
        self.dealer.deck.shuffle()
        self.dealer.hand.empty()
        self.player.hand.empty()
