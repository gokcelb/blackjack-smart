import time


class Game:
    def __init__(self, deck, dealer, player, ai1, ai2):
        self.deck = deck
        self.dealer = dealer
        self.player = player
        self.ai1 = ai1
        self.ai2 = ai2
        self.players = [self.ai1, self.ai2, self.player, self.dealer]

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

            print(f"{self.ai1.name} has entered the game.")
            print(f"{self.ai2.name} has entered the game.")

            while True:
                ai1_bet = self.ai1.bet()
                ai2_bet = self.ai2.bet()
                print(f"{self.ai1.name} has betted {ai1_bet}.")
                time.sleep(1)
                print(f"{self.ai2.name} has betted {ai2_bet}.")
                time.sleep(1)
                bet = self.ask_bet()
                time.sleep(1)
                self.opening()
                if self.check_for_blackjack(bet):
                    break
                time.sleep(1)
                if self.ai_plays(self.ai1, ai1_bet) == "busted" or self.ai_plays(self.ai2, ai2_bet) == "busted" or self.player_plays(bet) == "busted" or self.dealer_plays(bet) == "busted":
                    break
                self.check_for_winner(bet)
                break

            self.reset()

        print("You've ran out of money. Please restart this program to try again. Goodbye.")

    def opening(self):
        for who in self.players:
            who.hand.add(self.dealer.deal())
            who.hand.add(self.dealer.deal())
            who.hand.calculate_score()
            if who.name == "Dealer":
                print(f"The dealer is dealt: {who.hand.hand[0]}, Unknown")
            else:
                print(
                    f"{who.name}: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")
            time.sleep(2)

    def deal(self, who):
        try:
            dealt_card = self.dealer.deal()
            who.hand.add(dealt_card)
            who.hand.calculate_score()
            return dealt_card
        except Exception as err:
            print(err)

    def announce_hand(self, who):
        print(f"{who.name}: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")

    def check_for_blackjack(self, bet):
        for who in self.players:
            if who == self.dealer:
                continue
            if who.hand.score == 21:
                if self.dealer.hand.score != 21:
                    time.sleep(1)
                    print(f"Blackjack! {who.name} win ${bet + bet / 2}.")
                    who.funds += bet + bet / 2
                else:
                    time.sleep(1)
                    print("It's a tie. The bet has been returned to {who.name}.")
                return True

    def check_for_busted(self, bet):
        if self.ai1.hand.score > 21:
            time.sleep(1)
            print(f"{self.ai1.name}'s hand value is over 21 and they lose ${bet}")
            self.ai1.funds -= bet
            return True
        elif self.ai2.hand.score > 21:
            time.sleep(1)
            print(f"{self.ai2.name}'s hand value is over 21 and they lose ${bet}")
            self.ai2.funds -= bet
            return True
        elif self.player.hand.score > 21:
            time.sleep(1)
            print(f"Your hand value is over 21 and you lose ${bet}")
            self.player.funds -= bet
            return True
        elif self.dealer.hand.score > 21:
            time.sleep(1)
            print(f"The dealer busts, you win ${bet}")
            self.player.funds += bet
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

    def ai_plays(self, who, bet):
        action = who.act(self.dealer.hand.score)
        while action == "hit":
            print(f"{who.name} hits and is dealt: {self.deal(who)}")
            time.sleep(2)
            self.announce_hand(who)
            if self.check_for_busted(bet):
                return "busted"
            action = self.dealer.act()

        print(f"{who.name} stays.")

    def player_plays(self, bet):
        action = input("Would you like to hit or stay? ")
        while action.lower() != "hit" and action.lower() != "stay":
            print("That is not a valid option.")
            time.sleep(1)
            action = input("Would you like to hit or stay? ")

        while action.lower() == "hit":
            self.deal(self.player)
            self.announce_hand(self.player)
            if self.check_for_busted(bet):
                return "busted"
            time.sleep(1)
            action = input("Would you like to hit or stay? ")

    def dealer_plays(self, bet):
        self.announce_hand(self.dealer)
        action = self.dealer.act()
        while action == "hit":
            print(f"The dealer hits and is dealt: {self.deal(self.dealer)}")
            time.sleep(2)
            self.announce_hand(self.dealer)
            if self.check_for_busted(bet):
                return "busted"
            action = self.dealer.act()

        print("The dealer stays.")

    def ask_bet(self):
        bet = int(input("Place your bet: "))
        while bet > self.player.funds:
            print("You do not have sufficient funds.")
            bet = int(input("Place your bet: "))
        return bet

    def reset(self):
        for who in self.players:
            self.dealer.deck.cards.extend(who.hand.hand)
            who.hand.empty()
        self.dealer.deck.shuffle()
