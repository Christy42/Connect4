from board import BoardGame


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