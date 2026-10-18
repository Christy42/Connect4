import pygame
from pathlib import Path


WIDTH = 1280
HEIGHT = 720
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20

pygame.init()
pygame.font.init()

button_title_font = pygame.font.SysFont("arial", 60, bold=True)
button_font = pygame.font.SysFont("arial", 32)
