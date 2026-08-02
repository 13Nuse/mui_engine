import pygame
import sys

from dataclasses import dataclass
import settings


@dataclass
class Game:
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption(settings.GAME_NAME)
    clock = pygame.time.Clock()
    running = True

    # Main game loop
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

    # Handle user input and events
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass  # Update game state here

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        pygame.display.flip()  # Update the display

    def new_game(self):
        # Reset game state for a new game
        pass  # Implement new game logic here

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
    game.quit()

