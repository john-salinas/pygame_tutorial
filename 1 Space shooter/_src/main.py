import pygame
import os
from random import randint

class Player(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.img_path = os.path.join("..\\", "space 1 setup", "images", "player.png")
    self.image = pygame.image.load(self.img_path).convert_alpha()
    self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    self.direction = pygame.math.Vector2()
    self.speed = 300

  def update(self, dt):
    keys = pygame.key.get_pressed()
  
    # "Sprint" command
    if keys[pygame.K_LSHIFT]:
      self.speed = 600
    else:
      self.speed = 300

    # Keyboard input
    self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    self.direction = self.direction.normalize() if self.direction else self.direction
    self.rect.center += self.direction * self.speed * dt #type: ignore

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
      print("fire laser")


class Star(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.img_path = os.path.join("..\\", "space 1 setup", "images", "star.png")
    self.image = pygame.image.load(self.img_path).convert_alpha()
    self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))



# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# Plain Surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

# Sprite init
all_sprites = pygame.sprite.Group()
for i in range(20):
  Star(all_sprites)
player = Player(all_sprites)




meteor_img_path = os.path.join("..\\", "space 1 setup", "images", "meteor.png")
meteor_surf = pygame.image.load(meteor_img_path).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_img_path = os.path.join("..\\", "space 1 setup", "images", "laser.png")
laser_surf = pygame.image.load(laser_img_path).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT-20))



while running:
  # Setting the frame rate
  dt = clock.tick() / 1000

  # Event loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  all_sprites.update(dt)



  display_surface.fill('darkgray')
  # Meteor
  display_surface.blit(meteor_surf, meteor_rect)

  # laser
  display_surface.blit(laser_surf, laser_rect)

  all_sprites.draw(display_surface)

  pygame.display.update()

pygame.quit()