from enum_list import *

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

    def update_column(self, col, new_state):
        """Drop a disc into a column. It falls to the LOWEST empty row (gravity)."""
        # Start at the bottom row (6) and work upwards
        for row in range(ROWS, 0, -1):
            if self.squares[(col, row)].symbol == SquareState.Empty:
                self.squares[(col, row)].change_state(new_state)
                return True
        return False  # column is full

    def check_win(self, print_game=False):
        for match in self.winning_combo:
            states = [self.squares[coord].symbol for coord in match]
            if all(state == states[0] and state != SquareState.Empty for state in states):
                if print_game:
                    self.print_board()
                    print("Winning combination:", match)
                    print("Winner:", states[0])
                return states[0]
        if not self.get_valid_columns():
            if print_game:
                self.print_board()
                print("DRAW")
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
