import deck
import dealer
import player
import game

suits = [u"\u2666", u"\u2665", u"\u2663", u"\u2660"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
scores_for_values = {"A": {"small": 1, "big": 11}, "2": 2, "3": 3, "4": 4,
                     "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 10, "Q": 10, "K": 10}

cards = []
for suit in suits:
    for value in values:
        cards.append(value + suit)

scores_for_cards = {}
for card in cards:
    value = card[0]
    scores_for_cards[card] = scores_for_values[value]


if __name__ == "__main__":
    deck = deck.Deck(cards, scores_for_cards)
    deck.shuffle()

    dealer = dealer.Dealer(deck)
    player = player.Player()
    game = game.Game(dealer, player)

    game.play()
