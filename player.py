import pickle


from enum_list import PlayerType, SquareState
from random import choice, random


class Player:

    def __init__(self, symbol):
        self.symbol = symbol
        self.type = None

    def choose_move(self, board):
        return None

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.type = PlayerType.USER



class RandomPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.type = PlayerType.COMPUTER

    def choose_move(self, board):
        return choice(board.get_valid_columns())
