import pygame

from enum_list import SquareState

# Disc / board colours
BOARD_BLUE = (30, 60, 200)
HOLE_COLOUR = (15, 15, 40)       # colour showing through an empty slot
RED_DISC = (220, 30, 30)
YELLOW_DISC = (250, 220, 20)


class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = pygame.Rect(rect)

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        colour = (90, 90, 120) if hovered else (60, 60, 80)

        pygame.draw.rect(screen, colour, self.rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), self.rect, 2, border_radius=8)

        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class SquareButton(Button):
    """One cell of the Connect 4 grid: a blue tile with a circular slot in it."""

    def __init__(self, square, rect):
        super().__init__("", rect)
        self.square = square

    def draw(self, screen, font=None):
        # Blue board tile
        pygame.draw.rect(screen, BOARD_BLUE, self.rect)

        # Pick the disc colour based on the square's state (empty slots show the dark background)
        if self.square.symbol == SquareState.RED:
            colour = RED_DISC
        elif self.square.symbol == SquareState.YELLOW:
            colour = YELLOW_DISC
        else:
            colour = HOLE_COLOUR

        # Radius leaves a small gap so neighbouring discs don't touch
        radius = self.rect.width // 2 - 8
        pygame.draw.circle(screen, colour, self.rect.center, radius)

        # Thin darker outline gives the discs some definition
        pygame.draw.circle(screen, (0, 0, 0), self.rect.center, radius, 2)
