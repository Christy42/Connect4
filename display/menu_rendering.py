from universal_names import *
from display.button import *


class MainMenu:
    def __init__(self, width, height):
        self.start_y = height // 2
        self.x = (width - BUTTON_WIDTH) // 2
        self.buttons = []

    def handle_event(self, event):
        return NotImplementedError

    def draw(self, screen):

        screen.fill((25, 25, 35))

        title = button_title_font.render("Connect 4", True, (240, 230, 170))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 140))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen, button_font)


class MainMenuOrder(MainMenu):

    def __init__(self, width, height):
        super().__init__(width, height)

        self.buttons = [
            Button("Random", (self.x, self.start_y, BUTTON_WIDTH, BUTTON_HEIGHT)),
            Button("Player Goes First", (self.x, self.start_y + (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)),
            Button("Player Goes Second", (self.x, self.start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)),
        ]


    def handle_event(self, event):
        if self.buttons[0].clicked(event):
            return "random"

        if self.buttons[1].clicked(event):
            return "player_goes_first"

        if self.buttons[2].clicked(event):
            return "player_goes_second"
        return None


class MainMenuPlayer(MainMenu):

    def __init__(self, width, height):
        super().__init__(width, height)

        self.buttons = [
            Button("Player Vs Computer", (self.x, self.start_y, BUTTON_WIDTH, BUTTON_HEIGHT)),
            Button("Player Vs Player", (self.x, self.start_y + (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)),
            Button("Computer Vs Computer", (self.x, self.start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)),
        ]

    def handle_event(self, event):

        if self.buttons[0].clicked(event):
            return "player_vs_computer"

        if self.buttons[1].clicked(event):
            return "player_vs_player"

        if self.buttons[2].clicked(event):
            return "computer_vs_computer"
        return None


class MainMenuStyle(MainMenu):

    def __init__(self, width, height):
        super().__init__(width, height)

        self.buttons = [
            Button("Player 1 Uses RED", (self.x, self.start_y, BUTTON_WIDTH, BUTTON_HEIGHT)),
            Button("Player 1 Uses YELLOW", (self.x, self.start_y + (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)),
        ]


    def handle_event(self, event):

        if self.buttons[0].clicked(event):
            return "RED"

        if self.buttons[1].clicked(event):
            return "YELLOW"
        return None
