# import pygame
import os
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        self.direction = pygame.math.Vector2()
        self.og_speed = 300
        self.speed = self.og_speed
        self.sprint_speed = self.og_speed * 2

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

        # Sprint command
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.speed = self.sprint_speed
        else:
            self.speed = self.og_speed
    
    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt
    



    def update(self, dt):
        self.input()
        self.move(dt)