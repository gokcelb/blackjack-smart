from deck import Deck
from dealer import Dealer
from human_player import HumanPlayer
from game import Game
from ai_player import AIPlayer


if __name__ == "__main__":
    deck = Deck()
    dealer = Dealer()
    human = HumanPlayer()
    ai1 = AIPlayer()
    ai2 = AIPlayer()
    players = [ai1, ai2, human]

    game = Game(dealer, players)
    game.start_game()
