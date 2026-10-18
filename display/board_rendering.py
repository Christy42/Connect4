import pygame

from display.button import SquareButton, Button
from universal_names import *

from board import COLUMNS, ROWS

CELL_SIZE = 100
BOARD_WIDTH = COLUMNS * CELL_SIZE
BOARD_LEFT = (WIDTH - BOARD_WIDTH) // 2  # 290
BOARD_TOP = 100


def square_rect(square):
    """Pixel rectangle for a square. x and y are 1-based, so subtract 1."""
    return pygame.Rect(BOARD_LEFT + (square.x - 1) * CELL_SIZE,
                       BOARD_TOP + (square.y - 1) * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE)


def draw_grid(screen, squares):
    """Shared by the in-game board and the end-game screen. Returns the buttons it drew."""
    buttons = [SquareButton(sq, square_rect(sq)) for sq in squares.values()]
    for button in buttons:
        button.draw(screen, button_title_font)
    return buttons


class Board:
    def __init__(self, board_state):
        self.state = board_state
        self.square_buttons = []

    def draw(self, screen, current_colour=None):
        self.square_buttons = draw_grid(screen, self.state.squares)

        # Optional: show a "hovering" disc above the column the mouse is over,
        # so the player can see where they're about to drop.
        if current_colour is not None:
            col = self.column_from_x(pygame.mouse.get_pos()[0])
            if col is not None:
                centre = ((col - 1) * CELL_SIZE + CELL_SIZE // 2, BOARD_TOP // 2)
                pygame.draw.circle(screen, current_colour, centre, CELL_SIZE // 2 - 8)

    @staticmethod
    def column_from_x(x):
        """Convert a mouse x-position into a column number (1-7), or None if outside."""
        col = (x - BOARD_LEFT) // CELL_SIZE + 1
        return col if 1 <= col <= COLUMNS else None

    def handle_event(self, event):
        # In Connect 4 you click a COLUMN, not a single square.
        # Returns the column number, which the game loop can pass to board.update_column().
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.column_from_x(event.pos[0])
        return None


class BoardEndGame:
    def __init__(self, board, statement):
        self.board = board
        self.statement = statement
        self.x = BOARD_LEFT + (BOARD_WIDTH - BUTTON_WIDTH) // 2
        self.start_y = 25
        self.buttons = [Button("Main Menu", (self.x, self.start_y, BUTTON_WIDTH, BUTTON_HEIGHT))]


    def draw(self, screen):

        for button in self.buttons:
            button.draw(screen, button_font)

        # Result text, centred on the board (e.g. "Red wins!")
        font = pygame.font.Font(None, 80)
        text = font.render(self.statement, True, "white")
        rect = text.get_rect(center=(BOARD_LEFT + BOARD_WIDTH // 2, BOARD_TOP + 3 * CELL_SIZE))
        # Dark backing box so the text stays readable over the blue board
        pygame.draw.rect(screen, (0, 0, 0), rect.inflate(30, 20), border_radius=10)
        screen.blit(text, rect)

    def handle_event(self, event):
        if self.buttons[0].clicked(event):
            return "main_menu"
        return None
