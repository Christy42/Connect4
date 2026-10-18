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


class HeuristicPlayer(Player):
    """Wins if it can, blocks if it must, otherwise prefers the centre columns."""

    def __init__(self, symbol):
        super().__init__(symbol)
        self.type = PlayerType.COMPUTER

    def choose_move(self, board):
        valid = board.get_valid_columns()
        opponent = SquareState.YELLOW if self.symbol == SquareState.RED else SquareState.RED

        # 1. Take an immediate win
        for col in valid:
            if board.would_win(col, self.symbol):
                return col
        # 2. Block the opponent's immediate win
        for col in valid:
            if board.would_win(col, opponent):
                return col
        # 3. Otherwise favour columns nearest the centre (column 4)
        return min(valid, key=lambda c: abs(c - 4))
