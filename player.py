from hand import Hand
import abc


class Player(metaclass=abc.ABCMeta):
    def __init__(self):
        self.hand = Hand()
        self.funds = 500
        self.bet = 0

    @abc.abstractmethod
    def act(self):
        raise NotImplementedError

    @abc.abstractmethod
    def make_bet(self):
        raise NotImplementedError
