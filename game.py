import time
from checker import Checker


class Game:
    def __init__(self, deck, dealer, player, ai1, ai2):
        self.checker = Checker()
        self.deck = deck
        self.dealer = dealer
        self.player = player
        self.ai1 = ai1
        self.ai2 = ai2
        self.players = [self.ai1, self.ai2, self.player]
        self.all = [self.ai1, self.ai2, self.player, self.dealer]

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
            time.sleep(1)
            print(f"{self.ai2.name} has entered the game.")

            while True:
                self.ai1.make_bet()
                self.ai2.make_bet()
                print(f"{self.ai1.name} has betted {self.ai1.bet}.")
                time.sleep(1)
                print(f"{self.ai2.name} has betted {self.ai2.bet}.")
                time.sleep(1)
                self.player.bet = self.ask_bet()
                time.sleep(1)
                self.opening()
                if self.round_ends_with_blackjack():
                    break
                time.sleep(1)
                if self.ais_play() == "busted" or self.player_plays() == "busted" or self.dealer_plays() == "busted":
                    break
                self.round_ends()
                break

            self.reset()

        print("You've ran out of money. Please restart this program to try again. Goodbye.")

    def opening(self):
        for who in self.all:
            who.hand.add(self.dealer.deal())
            who.hand.add(self.dealer.deal())
            if who.name == "dealer":
                print(f"The dealer is dealt: {who.hand.hand[0]}, Unknown")
            else:
                print(
                    f"{who.name}: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")
            who.hand.calculate_score()
            time.sleep(2)

    def deal(self, who):
        try:
            dealt_card = self.dealer.deal()
            who.hand.add(dealt_card)
            return dealt_card
        except Exception as err:
            print(err)

    def announce_hand(self, who):
        print(f"{who.name}: {', '.join([str(card_obj) for card_obj in who.hand.hand])}")

    def round_ends_with_blackjack(self):
        naturals = self.checker.gets_natural(self.players)
        if len(naturals) == 0:
            return False

        for player in self.players:
            if player in naturals and self.dealer.hand.score != 21:
                print(f"Blackjack! {player.name} win {player.bet + player.bet / 2}.")
                player.funds += player.bet / 2
            elif player in naturals and self.dealer.hand.score == 21:
                print(f"It's a tie. The bet has been returned to {player.name}.")
 
        return True
        
    def round_ends_with_bust(self, who):
        busted = self.checker.busts(who)
        if busted is None:
            return False

        if busted == self.dealer:
            print("The dealer busts, you all win.")
            for player in self.players:
                if player == self.player:
                    suffix = ""
                else:
                    suffix = "s"
                print(f"{player.name} win{suffix} {player.bet}.")
                player.funds += player.bet
        else:
            print(f"{busted.name}'s hand value is over 21 and {busted.name} lose ${busted.bet}")
            busted.funds -= busted.bet
        return True

    def round_ends(self):
        self.checker.round_ends(self.players, self.dealer)
        for winner in self.checker.winners:
            print(f"{winner.name} wins {winner.bet}")
            winner.funds += winner.bet
        for tied in self.checker.ties:
            print(f"{tied.name} tie. {tied.name} bet has been returned.")
        for loser in self.checker.losers:
            print(f"The dealer wins, {loser.name} lose ${loser.bet}.")
            loser.funds -= loser.bet

    def ais_play(self):
        ais = [self.ai1, self.ai2]
        visible_dealer_hand_score = self.dealer.hand.hand[0].get_score()
        for ai in ais:
            action = ai.act(visible_dealer_hand_score)
            while action == "hit":
                print(f"{ai.name} hits and is dealt: {self.deal(ai)}")
                time.sleep(2)
                self.announce_hand(ai)
                ai.hand.calculate_score()
                print("ai hand score: ", ai.hand.score)
                if self.round_ends_with_bust(ai):
                    return "busted"
                action = ai.act(visible_dealer_hand_score)

            print(f"{ai.name} stays.")

    def player_plays(self):
        action = input("Would you like to hit or stay? ")
        while action.lower() != "hit" and action.lower() != "stay":
            print("That is not a valid option.")
            time.sleep(1)
            action = input("Would you like to hit or stay? ")

        while action.lower() == "hit":
            self.deal(self.player)
            self.announce_hand(self.player)
            self.player.hand.calculate_score()
            if self.round_ends_with_bust(self.player):
                return "busted"
            time.sleep(1)
            action = input("Would you like to hit or stay? ")

    def dealer_plays(self):
        self.announce_hand(self.dealer)
        action = self.dealer.act()
        while action == "hit":
            print(f"The dealer hits and is dealt: {self.deal(self.dealer)}")
            time.sleep(2)
            self.announce_hand(self.dealer)
            self.dealer.hand.calculate_score()
            if self.round_ends_with_bust(self.dealer):
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
        for who in self.all:
            self.dealer.deck.cards.extend(who.hand.hand)
            who.hand.empty()
        self.dealer.deck.shuffle()
