import pygame
import os
from random import randint, uniform

class Player(pygame.sprite.Sprite):
  def __init__(self, groups, surface):
    super().__init__(groups)
    self.image = surface
    self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    self.direction = pygame.math.Vector2()
    self.speed = 300

    # cooldown logic
    self.can_shoot = True
    self.laser_shoot_time = 0
    self.cooldown_duration = 100 # ms

  def laser_timer(self):
    if not self.can_shoot:
      current_time = pygame.time.get_ticks()
      if current_time - self.laser_shoot_time >= self.cooldown_duration:
        self.can_shoot = True


  def update(self, dt):
    keys = pygame.key.get_pressed()
  
    # "Sprint" command
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
      self.speed = 600
    else:
      self.speed = 300

    # Keyboard input
    self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    self.direction = self.direction.normalize() if self.direction else self.direction
    self.rect.center += self.direction * self.speed * dt #type: ignore

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE] and self.can_shoot:
      Laser(laser_surf, self.rect.midbottom, (all_sprites, laser_sprites)) #type: ignore


      self.can_shoot = False
      self.laser_shoot_time = pygame.time.get_ticks()

    self.laser_timer()

class Star(pygame.sprite.Sprite):
  def __init__(self, groups, surface):
    super().__init__(groups)
    self.image = surface
    self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Meteor(pygame.sprite.Sprite):
  def __init__(self, surface, pos, groups):
    super().__init__(groups)
    self.og_surface = surface
    self.image = self.og_surface
    self.rect = self.image.get_frect(center = pos)
    self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
    
    self.rotation = 0
    self.rotation_speed = randint(10, 100)

    self.speed = randint(100, 500)


  def update(self, dt):
    # Continuous rotation
    self.rotation += self.rotation_speed * dt
    self.image = pygame.transform.rotozoom(self.og_surface, self.rotation, 1)
    self.rect = self.image.get_frect(center = self.rect.center)

    # Random movement
    self.rect.center += self.direction * self.speed * dt #type: ignore
    if self.rect.top > WINDOW_HEIGHT: #type: ignore
      self.kill() 

class Laser(pygame.sprite.Sprite):
  def __init__(self, surface, pos, groups):
    super().__init__(groups)
    self.image = surface
    self.rect = self.image.get_frect(midbottom = pos)
    self.speed = 600

  def update(self, dt):
    self.rect.centery -= self.speed * dt #type: ignore

    if self.rect.bottom < 0: #type: ignore
      self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
  def __init__(self, frames, pos, groups):
    super().__init__(groups)
    self.frames = frames
    self.frame_index = 0
    self.image = self.frames[self.frame_index]
    self.rect = self.image.get_frect(center = pos)
  
  def update(self, dt):
    self.frame_index += 50 * dt
    if self.frame_index < len(self.frames):
      self.image = self.frames[int(self.frame_index) % len(self.frames)]
    else:
      self.kill()


def collisions():
  global running

  # Checking if the player hits a meteor and closing the game if it happens
  # collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
  # if collision_sprites:
    # running = False

  # Checking for collisions between laser and meteor. Kills all sprites in related condition
  for laser in laser_sprites:
    collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)

    if collided_sprites:
      laser.kill()
      AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

def display_score(display_surface):
  current_time = pygame.time.get_ticks() // 100
  text_surf = font.render(str(current_time), True, (235, 52, 210))
  text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
  display_surface.blit(text_surf, text_rect)

  pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20,20).move(0, -8), 5, 10)


# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()


# Imports
star_surf = pygame.image.load(os.path.join("..", "space 1 setup", "images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(os.path.join("..", "space 1 setup", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(os.path.join("..", "space 1 setup", "images", "laser.png")).convert_alpha()
player_surf = pygame.image.load(os.path.join("..", "space 1 setup", "images", "player.png")).convert_alpha()
font = pygame.font.Font(os.path.join("..", "space 1 setup", "images", "Oxanium-Bold.ttf"), 40)
explosion_frames = [pygame.image.load(os.path.join("..", "space 1 setup", "images", "explosion", f'{i}.png')).convert_alpha() for i in range(0, 21)]


# Sprite creation
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
  Star(all_sprites, star_surf)
player = Player(all_sprites, player_surf)


# Custom events
# Interval timer
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


# Game loop
while running:
  dt = clock.tick() / 1000

  # Event loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == meteor_event:
      x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
      Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

  # Updating the game
  all_sprites.update(dt)

  # Collision checking  
  collisions()

  display_surface.fill('#3a2e3f')
  all_sprites.draw(display_surface)

  # displaying text
  display_score(display_surface)

  pygame.display.update()

pygame.quit()