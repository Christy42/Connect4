import pygame
import logging

import game_code
from universal_names import *
# --------------------
# Start Game
# --------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# While developing: show everything
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")
# When training: only show warnings and errors, so debug messages are hidden
# logging.basicConfig(level=logging.WARNING)

game = game_code.Game()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked the x button to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_input(event)
    game.update()
    # fill the screen with a colour to wipe away anything from the last frame

    screen.fill((30, 30, 30))

    game.draw(screen)
    # put game on screen
    pygame.display.flip()
    clock.tick(60) # limit fps to 60

pygame.quit()
