import pygame
from random import randint

import src


class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((src.settings.WINDOW_WIDTH, src.settings.WINDOW_HEIGHT))
        pygame.display.set_caption("2 - Vampire Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Player
        self.player = src.Player((src.settings.WINDOW_WIDTH / 2, src.settings.WINDOW_HEIGHT / 2), self.all_sprites, self.collision_sprites)
        for i in range(6):
            x, y = randint(0, src.settings.WINDOW_WIDTH), randint(0, src.settings.WINDOW_HEIGHT)
            w, h = randint(60, 100), randint(50, 100)
            src.sprites.CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))


    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            
            # Updating
            self.all_sprites.update(dt)
            
            # Draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()