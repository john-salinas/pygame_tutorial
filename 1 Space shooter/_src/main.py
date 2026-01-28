import pygame
import os
from random import randint

 
# General setup
# This is a test
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

# Imports
player_surf_img_path = os.path.join("..\\", "space 1 setup", "images", "player.png")
player_surf = pygame.image.load(player_surf_img_path).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2()
player_speed = 300

star_surf_img_path = os.path.join("..\\", "space 1 setup", "images", "star.png")
star_surf = pygame.image.load(star_surf_img_path).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

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

    '''
    if event.type == pygame.KEYDOWN:
      print(event.key)

    if event.type == pygame.MOUSEMOTION:
      player_rect.center = event.pos
    '''
  
  # pygame.mouse.get_pos()
  keys = pygame.key.get_pressed()
  
  # "Sprint" command
  if keys[pygame.K_LSHIFT]:
    player_speed = 600
  else:
    player_speed = 300

  # Keyboard input
  player_direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
  player_direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
  player_direction = player_direction.normalize() if player_direction else player_direction
  player_rect.center += player_direction * player_speed * dt

  recent_keys = ""


  display_surface.fill('darkgray')


  # Stars
  for pos in star_positions:
    display_surface.blit(star_surf, pos)

  # Meteor
  display_surface.blit(meteor_surf, meteor_rect)

  # laser
  display_surface.blit(laser_surf, laser_rect)
  
  # Player
  display_surface.blit(player_surf, player_rect)




  pygame.display.update()

pygame.quit()