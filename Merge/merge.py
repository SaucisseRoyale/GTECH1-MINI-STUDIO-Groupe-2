import pygame
import time
from pygame.locals import *
import pickle



pygame.init()

screen_width = 1000
screen_height = 700
tile_size = 50
move_speed = 10
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
level = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

music = pygame.mixer.Sound("assets/son/music.mp3")
music.set_volume(0.55) 


# ------ MENU

import pygame
import sys

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Police de texte
font = pygame.font.Font(None, 36)

# Fonction pour afficher le texte
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Fonction pour le menu principal
def main_menu():
    background_img = pygame.image.load('assets/menu/background2.png')
    title_img = pygame.image.load('assets/menu/titre_du_jeu.png')

    # Redimensionne l'image de fond pour couvrir toute la fenêtre
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Redimensionne l'image du titre proportionnellement à la taille de l'écran
    title_img = pygame.transform.scale(title_img, (int(screen_width * 0.8), int(screen_height * 0.2)))

    title_rect = title_img.get_rect(center=(screen_width/2, screen_height * 0.3))  # Ajuste la position verticale du titre

    while True:
        screen.blit(background_img, (0, 0))  # Affiche l'image de fond
        screen.blit(title_img, title_rect)   # Affiche l'image du titre

        # Ajuste les coordonnées du texte pour le centrer
        text_width, text_height = font.size('Appuyez sur ESPACE pour continuer')
        text_x = (screen_width - text_width) // 2
        text_y = screen_height * 0.5
        draw_text('Appuyez sur ESPACE pour continuer', font, BLACK, screen, text_x, text_y)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Quitte la fonction main_menu() et lance le jeu
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Fonction pour le menu d'options
def options_menu():
    # Charge une image pour le fond du menu d'options
    options_background_img = pygame.image.load('assets/menu/background2.png')
    options_background_img = pygame.transform.scale(options_background_img, (screen_width, screen_height))

    # Position de la barre de volume
    volume_bar_rect = pygame.Rect(100, 300, screen_width - 200, 20)
    volume_bar_color = (100, 100, 100)

    # Volume de la musique (valeur entre 0 et 1)
    music_volume = 0.5

    while True:
        screen.fill(WHITE)
        screen.blit(options_background_img, (0, 0))  # Affiche l'image de fond du menu d'options

        # Dessine la barre de volume
        pygame.draw.rect(screen, volume_bar_color, volume_bar_rect)
        volume_bar_fill = pygame.Rect(volume_bar_rect.left, volume_bar_rect.top, int(volume_bar_rect.width * music_volume), volume_bar_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), volume_bar_fill)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    mouse_x, mouse_y = event.pos
                    if volume_bar_rect.collidepoint(mouse_x, mouse_y):
                        # Change le volume de la musique en fonction de la position de la souris sur la barre
                        volume = (mouse_x - volume_bar_rect.left) / volume_bar_rect.width
                        music_volume = max(0, min(1, volume))  # Assure que le volume reste entre 0 et 1

        pygame.display.update()

# Fonction pour le menu pause
def pause_menu():
    # Chargement des images des boutons
    resume_button_img = pygame.image.load('assets/menu/Resume.png')
    exit_button_img = pygame.image.load('assets/menu/exit.png')
    options_button_img = pygame.image.load('assets/menu/options.png')  # Bouton pour ouvrir le menu d'options

    # Redimensionnement des images des boutons proportionnellement à la taille de l'écran
    button_width = int(screen_width * 0.25)
    button_height = int(screen_height * 0.1)

    resume_button_img = pygame.transform.scale(resume_button_img, (button_width, button_height))
    options_button_img = pygame.transform.scale(options_button_img, (button_width, button_height))
    exit_button_img = pygame.transform.scale(exit_button_img, (button_width, button_height))

    # Positionnement des boutons
    button_padding = 20  # Espacement entre les boutons
    total_button_height = button_height * 3 + button_padding * 2  # Hauteur totale des boutons et de l'espacement
    first_button_y = (screen_height - total_button_height) // 2  # Position y du premier bouton

    resume_button_rect = resume_button_img.get_rect(center=(screen_width/2, first_button_y))
    options_button_rect = options_button_img.get_rect(center=(screen_width/2, first_button_y + button_height + button_padding))
    exit_button_rect = exit_button_img.get_rect(center=(screen_width/2, first_button_y + (button_height + button_padding) * 2))


    while True:
        screen.fill(WHITE)
        screen.blit(resume_button_img, resume_button_rect)
        screen.blit(options_button_img, options_button_rect)
        screen.blit(exit_button_img, exit_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_button_rect.collidepoint(mouse_pos):
                    return  # Quitte la fonction pause_menu() et reprend le jeu
                elif options_button_rect.collidepoint(mouse_pos):
                    options_menu()  # Affiche le menu d'options lorsque le bouton "Options" est cliqué
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


clock = pygame.time.Clock()
fps = 60
dt = 0

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)



pine1_img = pygame.image.load('map_level_editor/img/pine1.png').convert_alpha()
pine2_img = pygame.image.load('map_level_editor/img/pine2.png').convert_alpha()
mountain_img = pygame.image.load('map_level_editor/img/mountain.png').convert_alpha()
sky_img = pygame.image.load('map_level_editor/img/sky_cloud.png').convert_alpha()


def draw_bg():
  screen.fill(GREEN)
  width = sky_img.get_width()
  for x in range(4):
    screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
    screen.blit(mountain_img,
                ((x * width) - scroll * 0.6,
                 screen_height - mountain_img.get_height() - 300))
    screen.blit(pine1_img, ((x * width) - scroll * 0.7,
                            screen_height - pine1_img.get_height() - 150))
    screen.blit(
        pine2_img,
        ((x * width) - scroll * 0.8, screen_height - pine2_img.get_height()))


class Force():

  def __init__(self):
    self.is_active = False
    self.current_speed = 0

  def Start(self, direction, start_speed, end_speed, acceleration):
    self.StartWithDistance(direction, -1, start_speed, end_speed, acceleration)

  def StartWithDistance(self, direction, distance, start_speed, end_speed,
                        acceleration):
    self.direction = direction
    self.distance = distance
    self.start_speed = start_speed
    self.end_speed = end_speed
    self.acceleration = acceleration
    self.acomplished_distance = 0
    self.is_active = True
    self.current_speed = start_speed

    if acceleration < 0:
      self.minOrMax = max
    else:
      self.minOrMax = min

  def Stop(self):
    self.is_active = False

  def Update(self, dt):
    if self.IsActive() == False:
      return 0, 0

    distance = self.current_speed * dt
    move_x = self.direction[0] * distance
    move_y = self.direction[1] * distance

    self.current_speed += (self.acceleration * dt)
    self.current_speed = (self.minOrMax(self.current_speed, self.end_speed))

    if self.distance != -1:
      self.acomplished_distance += distance
      if self.acomplished_distance >= self.distance:
        self.Stop()

    return move_x, move_y

  def IsActive(self):
    return self.is_active


class Camera:

  def __init__(self, width, height):
    self.camera = pygame.Rect(0, 0, width, height)
    self.width = width
    self.height = height

  def apply(self, entity):
    return entity.move(self.camera.topleft)

  def update(self, target):
    x = -target.rect.centerx + int(screen_width / 2)
    y = -target.rect.centery + int(screen_height / 2)

    # limit scrolling to map size
    x = min(0, x)
    y = min(0, y)
    x = max(-(self.width - screen_width), x)
    y = max(-(self.height - screen_height), y)

    self.camera = pygame.Rect(x, y, self.width, self.height)


class World:

  def __init__(self, data):
    self.tile_list = []

    if not data:
      self.width = 0
      self.height = 0
      return

    self.width = len(data[0]) * tile_size
    self.height = len(data) * tile_size

    dirt_img = pygame.image.load("map_level_editor/dirt.png").convert_alpha()
    grass_img = pygame.image.load("map_level_editor/grass.png").convert_alpha()

    row_count = 0
    for row in data:
      col_count = 0
      for tile in row:
        if tile == 1:
          img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        elif tile == 2:
          img = pygame.transform.scale(grass_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        col_count += 1
      row_count += 1

  def draw(self, camera):
    for tile in self.tile_list:
      screen.blit(tile[0], camera.apply(tile[1]))


class Player:

  def __init__(self, x, y):
    img = pygame.image.load("map_level_editor/tile_0000.png").convert_alpha()
    self.image = pygame.transform.scale(img, (56, 56))
    self.rect = self.image.get_rect()
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.rect.x = x
    self.rect.y = y

    self.walk_speed = 500  #vitesse de marche
    self.speed_multiplication = 1
    self.current_speed_x = 0
    self.current_speed_y = 0
    self.dir_x = 0
    self.dir_y = 0

    self.gravity = 1.2  #force de la gravité
    self.gravity_coefficient = 1  #acceleration de la gravité

    self.on_ground = False
    self.on_wall = False

    self.dash_power = 40  #puissance du dash
    self.dash_acceleration = 5  #accélération du dash
    self.dash_duration = 0.1  #durée du dash
    self.dash_speed = 0
    self.dash_timer = 0
    self.dash_direction = 0
    self.dash_allow = True

    self.jump_power = 17  #puissance du saut
    self.maxjump = 2  #nombre de sauts
    self.nbr_jump = 0
    self.space_pressed = False

    self.slide_speed = 4.0  #vitesse du slide (quoeficient d'acceleration de la vitesse)
    self.slide_duration = 0.3  #durée du slide
    self.is_sliding = False
    self.slide_timer = 0

  def set_velocity_x(self, dir_x, speed):
    self.current_speed_x = dir_x * speed

  def set_velocity_y(self, dir_y, speed):
    self.current_speed_y = dir_y * speed

  def update(self):

    dx = self.current_speed_x * dt
    dy = self.current_speed_y * dt

    #gravity
    self.current_speed_y += self.gravity * self.gravity_coefficient**dt
    dy += self.current_speed_y
    #end of gravity

    # Check collisions
    for tile in world.tile_list:
      if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,
                             self.height):
        dx = 0
        self.on_wall = True

      if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
                             self.height):
        if self.current_speed_y < 0:
          dy = tile[1].bottom - self.rect.top
          self.current_speed_y = 0
        elif self.current_speed_y >= 0:
          dy = tile[1].top - self.rect.bottom
          self.current_speed_y = 0
          self.on_ground = True
          self.nbr_jump = 0
  #end of collision check

  # Update player coordinates
    self.rect.x += dx
    self.rect.y += dy

    if self.current_speed_x >= 0:
      self.current_speed_x = max(
          0, self.current_speed_x - (2000 * dt * self.speed_multiplication))
    else:
      self.current_speed_x = min(
          0, self.current_speed_x + (2000 * dt * self.speed_multiplication))

  #end of Update player coordinates

  def draw(self, camera):
    screen.blit(self.image, camera.apply(self.rect))


file_path = 'map_level_editor/map/2map.txt'

with open(file_path, 'r') as file:
  world_data = [list(map(int, line.strip().split(','))) for line in file]
world = World(world_data)
player = Player(100, screen_height - 130)
camera = Camera(world.width, world.height)



main_menu()

# ------ Début de la boucle de jeu du premier niveau

music.play(-1)
run = True
while run:
  start = pygame.time.get_ticks()

  screen.fill(WHITE)
  # Code de ton jeu va ici

  #movement
  key = pygame.key.get_pressed()
  if key[K_q] and (not player.is_sliding or abs(player.current_speed_x) <= 20):
    player.set_velocity_x(-1, player.walk_speed)
  if key[K_d] and (not player.is_sliding or abs(player.current_speed_x) <= 20):
    player.set_velocity_x(1, player.walk_speed)
  #end of movement

  #jump
  if key[K_SPACE] and not player.is_sliding:
    if player.on_ground or player.on_wall:
      player.set_velocity_y(-1, player.jump_power)
      player.on_ground = False
      player.nbr_jump += 1
    elif not player.space_pressed and player.nbr_jump < player.maxjump and (
        not player.on_ground or not player.on_wall):
      player.nbr_jump += 1
      player.set_velocity_y(-1, player.jump_power)
    player.space_pressed = True
  else:
    player.space_pressed = False
  #end of jump

  # Dash
  if key[
      K_LCTRL] and player.dash_timer <= 0 and player.dash_allow and not player.on_ground and not player.space_pressed:
    # Détermination de la direction du dash
    player.dash_direction = 1 if key[K_d] else -1 if key[K_q] else 0

    player.dash_speed += player.dash_acceleration
    if player.dash_speed >= player.dash_power:
      player.dash_speed = player.dash_power
      player.dash_timer = player.dash_duration
      player.dash_allow = False
    player.rect.x += player.dash_speed * player.dash_direction
    player.current_speed_y = 0
  elif player.dash_timer > 0:
    player.dash_timer -= dt
    player.dash_speed = 0
  elif player.on_ground:
    player.dash_allow = True
  #end of dash

  #slide
  if key[K_LSHIFT]:
    if player.on_ground and player.slide_timer <= 0 and not player.is_sliding:
      player.current_speed_x *= player.slide_speed
      player.is_sliding = True
    player.speed_multiplication = 0.5

  else:
    player.is_sliding = False
    player.speed_multiplication = 1
  #end of slide

  draw_bg()

  camera.update(player)
  world.draw(camera)
  player.update()
  player.draw(camera)

  targetTime = 1000 / fps
  if dt < targetTime:
    pygame.time.delay(int(targetTime - dt))
  dt = pygame.time.get_ticks() - start
  dt /= 1000

  # Détecte les événements
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit() 
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
              music.set_volume(0.15)
              pause_menu()  # Affiche le menu pause si la touche Echap est enfoncée
  
  pygame.display.update()


  
pygame.quit()
