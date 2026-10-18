from enum import Enum, auto


class Turn(Enum):
    PLAYER_1 = auto()
    PLAYER_2 = auto()


class InputState(Enum):
    NEW_GAME = auto()
    NORMAL = auto()
    MAIN_MENU_PLAYER = auto()
    MAIN_MENU_ORDER = auto()
    MAIN_MENU_STYLE = auto()
    GAME_OVER = auto()


class SquareState(Enum):
    RED = auto()
    YELLOW = auto()
    Empty = auto()

class GameResult(Enum):
    DRAW = auto()


class PlayerType(Enum):
    USER = auto()
    COMPUTER = auto()


class GameType(Enum):
    COMPUTER_VS_COMPUTER = auto()
    COMPUTER_VS_PLAYER = auto()
    PLAYER_VS_PLAYER = auto()