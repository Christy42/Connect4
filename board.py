from enum_list import *
import numpy as np

# Connect 4 dimensions
COLUMNS = 7
ROWS = 6


class Square:
    def __init__(self, x, y):
        self.x = x          # column, 1..7 (left to right)
        self.y = y          # row, 1..6 (1 = TOP row, 6 = BOTTOM row, matching how it is drawn)
        self.symbol = SquareState.Empty

    def change_state(self, new_state):
        if self.symbol == SquareState.Empty:
            self.symbol = new_state


def build_winning_lines():
    """Generate every possible line of 4 on a 7x6 board (replaces the hard-coded 3x3 list)."""
    lines = []
    # Direction vectors: right, down, down-right diagonal, down-left diagonal
    for dx, dy in [(1, 0), (0, 1), (1, 1), (-1, 1)]:
        for x in range(1, COLUMNS + 1):
            for y in range(1, ROWS + 1):
                # End point of a 4-long line starting at (x, y)
                end_x, end_y = x + 3 * dx, y + 3 * dy
                if 1 <= end_x <= COLUMNS and 1 <= end_y <= ROWS:
                    lines.append([(x + i * dx, y + i * dy) for i in range(4)])
    return lines


class BoardGame:
    winning_combo = build_winning_lines()

    def __init__(self):
        self.squares = {(x, y): Square(x, y)
                        for x in range(1, COLUMNS + 1)
                        for y in range(1, ROWS + 1)}
        self.last_move = None # (col, row, symbol) of the last move made, for win-checking optimization
        self.move_history = []  # every (col, row, symbol) played, in order

    def to_array(self, perspective):
        """board as a ROWS x COLUMNS array from one player's point of view.
        +1 = a disc belonging to `perspective`, -1 = the opponent's disc, 0 = empty.
        Row 0 is the TOP row, matching how the board is drawn."""
        arr = np.zeros((ROWS, COLUMNS), dtype=np.int8)
        for (x, y), square in self.squares.items():
            if square.symbol == SquareState.Empty:
                continue
            # x and y are 1-based, array indices are 0-based
            arr[y - 1, x - 1] = 1 if square.symbol == perspective else -1
        return arr

    def update_column(self, col, new_state):
        """Drop a disc into a column. It falls to the LOWEST empty row (gravity)."""
        # Start at the bottom row (6) and work upwards
        for row in range(ROWS, 0, -1):
            if self.squares[(col, row)].symbol == SquareState.Empty:
                self.squares[(col, row)].change_state(new_state)
                self.last_move = (col, row, new_state) # remember where last move landed
                self.move_history.append(self.last_move) # record history
                return row # will return true
        return False  # column is full

    def undo_move(self):
        """ take back the most recent move (exact reverse of update_column)."""
        if not self.move_history:
            return
        col, row, _ = self.move_history.pop()
        # Set directly: change_state() deliberately refuses to overwrite a disc
        self.squares[(col, row)].symbol = SquareState.Empty
        # Restore last_move to the move before, so check_win() stays correct
        self.last_move = self.move_history[-1] if self.move_history else None

    def would_win(self, col, symbol):
        """would dropping `symbol` in `col` win immediately? Board is left unchanged."""
        row = self.update_column(col, symbol)
        if not row:  # column was full
            return False
        won = self.check_win_from(col, row, symbol)
        self.undo_move()          # put everything back exactly as it was
        return won

    def check_win_from(self, col, row, symbol):
        """Only the lines through the last-placed disc can have just become a win."""
        for dx, dy in [(1, 0), (0, 1), (1, 1), (-1, 1)]:
            count = 1
            # Count in both directions along this axis
            for sign in (1, -1):
                x, y = col + sign * dx, row + sign * dy
                while (1 <= x <= COLUMNS and 1 <= y <= ROWS
                       and self.squares[(x, y)].symbol == symbol):
                    count += 1
                    x += sign * dx
                    y += sign * dy
            if count >= 4:
                return True
        return False

    def check_win(self, print_game=False):
        if self.last_move is not None:
            col, row, symbol = self.last_move
            if self.check_win_from(col, row, symbol):
                if print_game:
                    self.print_board()
                return symbol
        if not self.get_valid_columns():
            if print_game:
                self.print_board()
            return GameResult.DRAW
        return None

    def can_play_column(self, col):
        """A column is playable if its TOP square is still empty."""
        if self.squares[(col, 1)].symbol == SquareState.Empty:
            return True, ""
        return False, "Column is full"

    def get_valid_columns(self):
        """Columns a player may legally choose (useful for AI / random moves)."""
        return [col for col in range(1, COLUMNS + 1) if self.can_play_column(col)[0]]

    def get_state(self):
        # Now covers the whole 7x6 board instead of just 3x3
        return tuple(
            self.squares[(x, y)].symbol.value
            for x in range(1, COLUMNS + 1)
            for y in range(1, ROWS + 1)
        )

    def make_move(self, col, symbol):
        """Play a disc in a column (was: play a specific square). Returns False if column full."""
        return self.update_column(col, symbol)

    def reset(self):
        for square in self.squares.values():
            square.symbol = SquareState.Empty
        self.last_move = None # to avoid a move from a previous game getting checked
        self.move_history = [] # reset history

    def print_board(self):
        print("\nFinal board:")
        for y in range(1, ROWS + 1):
            row = []
            for x in range(1, COLUMNS + 1):
                symbol = self.squares[(x, y)].symbol
                if symbol == SquareState.RED:
                    row.append("R ")
                elif symbol == SquareState.YELLOW:
                    row.append("Y ")
                else:
                    row.append("- ")
            print("".join(row))
        print()
