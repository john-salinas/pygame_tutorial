import pygame
import os

import src.settings as settings



class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.diplay_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption("2 - Monster Battle")
        self.running = True
        self.clock = pygame.time.Clock()

        # Imports
        self.player_surf = pygame.image.load(os.path.join(""))


    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.diplay_surface.fill('black')

            pygame.display.update()




if __name__ == "__main__":
    game = Game()
    game.run()