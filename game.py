from cmath import log
from turtle import update
from checker import Checker
from deck import Deck
import grammar
import wait


class Game:
    def __init__(self, dealer, players):
        self.checker = Checker()
        self.deck = Deck()
        self.dealer = dealer
        self.players = players
        self.curr_idx = 0
        self.curr_player = self.players[self.curr_idx]
        self.game_over = False

    def start_game(self):
        while not self.game_over:
            self.start_round()
            self.reset()
            self.update_players()
        print("game over")

    def update_players(self):
        for player in self.players:
            if player.funds <= 0:
                self.game_over = True

    def reset_curr_player(self):
        self.curr_idx = 0
        self.curr_player = self.players[self.curr_idx]

    def start_round(self):
        self.bets()
        if self.openings() == "blackjack":
            return self.curr_player
        
        self.plays()

        while self.curr_idx < 3:
            self.curr_player.make_bet()
            print(f"{self.curr_player.name} betted ${self.curr_player.bet}")
            self.next()

        self.reset_curr_player()
        while self.curr_idx < 3:
            self.opening(self.curr_player)
            self.next()
        self.opening(self.dealer)

        if self.round_ends_with_blackjack():
            return

        self.reset_curr_player()
        while self.curr_idx < 3:
            if self.play(self.curr_player) == "busted":
                return
            self.next()
        if self.play(self.dealer) == "busted":
            return
        
        self.round_ends()

    def play(self, who):
        if who == self.dealer:
            self.announce_hand(who)
            wait.one_second()

        s_suffix = grammar.determine_s(who.name)
        tobe_suffix = grammar.determine_tobe(who.name)
        visible_dealer_hand_score = self.dealer.hand.cards[0].get_score()
        if type(visible_dealer_hand_score) is dict:
            visible_dealer_hand_score = visible_dealer_hand_score["big"]

        action = who.act() if who == self.dealer else who.act(visible_dealer_hand_score)
        while action == "hit":
            print(f"{who.name} hit{s_suffix} and {tobe_suffix} dealt: {self.deal(who)}")
            self.announce_hand(who)
            who.hand.calculate_score()
            if self.round_ends_with_bust(who):
                return "busted"
            wait.one_second()
            action = who.act() if who == self.dealer else who.act(visible_dealer_hand_score)
        print(f"{who.name} stay{s_suffix}")

    def opening(self, who):
        self.deal(who)
        self.deal(who)
        if who.name == "dealer":
            print(
                f"The dealer is dealt: {who.hand.cards[0]}, Unknown")
        else:
            print(
                f"{who.name}: {', '.join([str(card_obj) for card_obj in who.hand.cards])}")
        who.hand.calculate_score()
        wait.two_seconds()

    def deal(self, who):
        if len(self.deck.cards) == 0:
            raise Exception("no cards left in the deck")
        dealt_card = self.deck.cards.pop(0)
        who.hand.add(dealt_card)
        return dealt_card

    def next(self):
        self.curr_idx += 1
        if self.curr_idx > 2: return
        self.curr_player = self.players[self.curr_idx]

    def announce_hand(self, who):
        print(
            f"{who.name}: {', '.join([str(card_obj) for card_obj in who.hand.cards])}")

    def announce_final_results(self):
        for winner in self.checker.winners:
            winner_s_suffix = grammar.determine_s(winner.name)
            print(f"{winner.name} win{winner_s_suffix} ${winner.bet}")
            winner.funds += winner.bet
        for tied in self.checker.ties:
            tied_s_suffix = grammar.determine_s(tied.name)
            print(
                f"{tied.name} tie{tied_s_suffix}. {tied.possessive} bet (${tied.bet}) has been returned")
        for loser in self.checker.losers:
            loser_s_suffix = grammar.determine_s(loser.name)
            print(
                f"The dealer wins, {loser.name} lose{loser_s_suffix} ${loser.bet}.")
            loser.funds -= loser.bet

    def round_ends_with_blackjack(self):
        naturals = self.checker.gets_natural(self.players)
        if len(naturals) == 0:
            return False

        self.announce_hand(self.dealer)
        for player in self.players:
            player_s_suffix = grammar.determine_s(player.name)
            if player in naturals and self.dealer.hand.score != 21:
                print(
                    f"Blackjack! {player.name} win{player_s_suffix} ${player.bet + player.bet / 2}")
                player.funds += player.bet / 2
            elif player in naturals and self.dealer.hand.score == 21:
                print(
                    f"It's a tie. The bet has been returned to {player.name}")

        if len(naturals) == 3:
            return True

        non_naturals = []
        for player in self.players:
            if player not in naturals:
                non_naturals.append(player)
        self.checker.round_ends(non_naturals, self.dealer)
        self.announce_final_results()
        return True

    def round_ends_with_bust(self, who):
        busted = self.checker.busts(who)
        if busted is None:
            return False

        busted_s_suffix = grammar.determine_s(busted.name)
        if busted == self.dealer:
            print("The dealer busts, you all win")
            for player in self.players:
                player_s_suffix = grammar.determine_s(player.name)
                print(f"{player.name} win{player_s_suffix} ${player.bet}.")
                player.funds += player.bet
        else:
            print(
                f"{busted.possessive} hand value is over 21 and {busted.name} lose{busted_s_suffix} ${busted.bet}")
            busted.funds -= busted.bet
            for player in self.players:
                if player == busted:
                    continue
                print(f"{player.possessive} bet (${player.bet}) has been returned")
        return True

    def round_ends(self):
        self.checker.round_ends(self.players, self.dealer)
        self.announce_final_results()

    def reset(self):
        for player in self.players:
            self.deck.cards.extend(player.hand.cards)
            player.hand.empty()
        self.deck.cards.extend(self.dealer.hand.cards)
        self.dealer.hand.empty()
        self.reset_curr_player()
        self.checker.empty()
        self.deck.shuffle()
