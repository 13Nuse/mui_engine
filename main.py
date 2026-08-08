"""
main.py

Wires core, backend, and frontend together into one game loop.

"""

import sys
import pygame
import settings
import controls

from __future__ import annotations
from dataclasses import dataclass
from frontend.menu.main_menu import MainMenu


@dataclass
class Game:
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_icon(settings.GAME_ICON) # will set an icon once made
    pygame.display.set_caption(settings.GAME_NAME)
    clock = pygame.time.Clock()
    running = True
    state = settings.GameState.WORLD
    menu = MainMenu(screen)

    # Main game loop
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

    # Handle user input and events
    def handle_events(self) -> None:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        if self.state == "menu":
            action = self.menu.handle_events(events)
            if action == "start":
                self.state = "playing"
                self.new_game()
            elif action == "quit":
                self.running = False
        elif self.state == "playing":
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"

           
    def update(self):
        if self.state == "playing":
            return None

    def draw(self):
        if self.state == "menu":
            self.menu.draw()
        else:
            self.screen.fill((18, 33, 51))
            self.draw_playing_screen()

        pygame.display.flip()

    def draw_playing_screen(self) -> None:
        self.draw_label("Game Scene", settings.get_title_font(settings.FONT_TITLE_SIZE), settings.WHITE, (40, 40))
        self.draw_label("The main gameplay view.", settings.get_body_font(settings.FONT_BODY_SIZE), settings.LIGHT_GRAY, (40, 95))
        self.draw_label("Press Esc to return to the main menu.", settings.get_small_font(settings.FONT_SMALL_SIZE), settings.GRAY, (40, 140))

    def draw_label(self, text: str, font, color, position: tuple[int, int]) -> None:
        surface = font.render(text, True, color)
        self.screen.blit(surface, position)

    def new_game(self):
        return None

    def game_intro(self):
        self.state = "menu"

    def quit(self) :
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
    game.quit()

