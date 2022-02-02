class Checker:
    def __init__(self):
        self.winners = []
        self.losers = []
        self.ties = []

    def gets_natural(self, players):
        naturals = []
        for player in players:
            if player.hand.score == 21:
                naturals.append(player)
        return naturals

    def busts(self, who):
        if who.hand.score > 21:
            return who

    def round_ends(self, players, dealer):
        for player in players:
            if player.hand.score == dealer.hand.score:
                self.ties.append(player)
            elif player.hand.score > dealer.hand.score:
                self.winners.append(player)
            else:
                self.losers.append(player)
        
    def empty(self):
        self.winners = []
        self.losers = []
        self.ties = []