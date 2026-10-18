from board import BoardGame
from enum_list import SquareState, GameResult


# trainer.py
def play_game(player_red, player_yellow):
    board = BoardGame()
    players = [player_red, player_yellow]
    turn = 0
    while True:
        move = players[turn].choose_move(board)
        board.make_move(move, players[turn].symbol)
        result = board.check_win()
        if result is not None:
            return result           # no pygame involved at all
        turn = 1 - turn
        

def evaluate(make_player_a, make_player_b, games=200):
    """Play many headless games and report results from player A's point of view.
    make_player_x is a function like `lambda symbol: RandomPlayer(symbol)`."""
    a_wins = b_wins = draws = 0
    for i in range(games):
        # Alternate colours so neither player gets a permanent first-move advantage
        if i % 2 == 0:
            a, b = make_player_a(SquareState.RED), make_player_b(SquareState.YELLOW)
            result = play_game(a, b)                 # a plays first
        else:
            b, a = make_player_b(SquareState.RED), make_player_a(SquareState.YELLOW)
            result = play_game(b, a)                 # b plays first

        if result == GameResult.DRAW:
            draws += 1
        elif result == a.symbol:
            a_wins += 1
        else:
            b_wins += 1
    print(f"A wins: {a_wins}  B wins: {b_wins}  Draws: {draws}")