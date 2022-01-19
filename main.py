from deck import Deck
from dealer import Dealer
from player import Player
from game import Game
from card import Card
from ai import AI


if __name__ == "__main__":
    deck = Deck()
    dealer = Dealer(deck)
    player = Player()
    ai1 = AI()
    ai2 = AI()

    game = Game(deck, dealer, player, ai1, ai2)
    game.play()
