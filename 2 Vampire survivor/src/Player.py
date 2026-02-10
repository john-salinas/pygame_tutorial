# import pygame
import os
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)

        # Movement
        self.direction = pygame.math.Vector2()
        self.og_speed = PLAYER_SPEED
        self.speed = self.og_speed
        self.sprint_speed = self.og_speed * 2

        self.collision_sprites = collision_sprites

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
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        if (self.hitbox_rect.right >= WINDOW_WIDTH):
            self.hitbox_rect.right = WINDOW_WIDTH
        if (self.hitbox_rect.left <= 0):
            self.hitbox_rect.left = 0
        self.collision('horizontal')


        self.hitbox_rect.y += self.direction.y * self.speed * dt
        if (self.hitbox_rect.bottom >= WINDOW_HEIGHT):
            self.hitbox_rect.bottom = WINDOW_HEIGHT
        if (self.hitbox_rect.top <= 0):
            self.hitbox_rect.top = 0
        self.collision('vertical')

        
        self.rect.center = self.hitbox_rect.center
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                elif direction == "vertical":
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.move(dt)