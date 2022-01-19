from deck import Deck
from dealer import Dealer
from player import Player
from game import Game


if __name__ == "__main__":
    deck = Deck()
    dealer = Dealer(deck)
    player = Player()

    game = Game(deck, dealer, player)
    game.play()
