import pygame
import time
from pygame.locals import *
import pickle

pygame.init()

screen_width = 1000
screen_height = 700
tile_size = 50
move_speed = 5
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
level = 0


clock = pygame.time.Clock()
fps = 60
dt = 0

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

pine1_img = pygame.image.load('img/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/sky_cloud.png').convert_alpha()

def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - scroll * 0.6, screen_height - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - scroll * 0.7, screen_height - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - scroll * 0.8, screen_height - pine2_img.get_height()))

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
            print("world_data est vide!")
            self.width = 0
            self.height = 0
            return 

        self.width = len(data[0]) * tile_size
        self.height = len(data) * tile_size

        dirt_img = pygame.image.load("img/grass/0.png").convert_alpha()
        grass_img = pygame.image.load("img/grass/1.png").convert_alpha()
        left_grass_corner_img = pygame.image.load("img/grass/2.png").convert_alpha()
        right_grass_corner_img = pygame.image.load("img/grass/3.png").convert_alpha()
        left_grass_img = pygame.image.load("img/grass/4.png").convert_alpha()
        right_grass_img = pygame.image.load("img/grass/5.png").convert_alpha()
        dirt2_img = pygame.image.load("img/grass/6.png").convert_alpha()
        left_bottom_grass_corner_img = pygame.image.load("img/grass/7.png").convert_alpha()
        right_bottom_grass_corner_img = pygame.image.load("img/grass/8.png").convert_alpha()
        left10 = pygame.image.load("img/grass/9.png").convert_alpha()
        right11 = pygame.image.load("img/grass/10.png").convert_alpha()
        jsp12 = pygame.image.load("img/grass/11.png").convert_alpha()
        tile13 = pygame.image.load("img/grass/12.png").convert_alpha()
        tile14 = pygame.image.load("img/grass/13.png").convert_alpha()
        tile15 = pygame.image.load("img/grass/14.png").convert_alpha()
        tile16 = pygame.image.load("img/grass/15.png").convert_alpha()
        tile17 = pygame.image.load("img/grass/16.png").convert_alpha()
        tile18 = pygame.image.load("img/grass/17.png").convert_alpha()
        tile19 = pygame.image.load("img/grass/18.png").convert_alpha()
        tile20 = pygame.image.load("img/grass/19.png").convert_alpha()
        tile21 = pygame.image.load("img/grass/20.png").convert_alpha()

        tile_images = {
            0: dirt_img,
            1: grass_img,
            2: left_grass_corner_img,
            3: right_grass_corner_img,
            4: left_grass_img,
            5: right_grass_img,
            6: dirt2_img,
            7: left_bottom_grass_corner_img,
            8: right_bottom_grass_corner_img,
            9: left10, 
            10: right11,
            11: jsp12,
            12 : tile13,
            13 : tile14,
            14 : tile15,
            15 : tile16,
            16 : tile17,
            17 : tile18,
            18 : tile19,
            19 : tile20,
            20 : tile21,
        }

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # Sélectionnez l'image basée sur le type de tuile en utilisant le dictionnaire
                if tile in tile_images:
                    img = pygame.transform.scale(tile_images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_data = (img, img_rect)
                    self.tile_list.append(tile_data)
                col_count += 1
            row_count += 1

    def draw(self, camera):
        for tile in self.tile_list:
            screen.blit(tile[0], camera.apply(tile[1]))

class Player:
    def __init__(self, x, y):
        img = pygame.image.load("tile_0000.png").convert_alpha()
        self.image = pygame.transform.scale(img, (56, 56))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.jump_power = 15
        self.gravity = 1
        self.dash_power = 40
        self.dash_speed = 0
        self.dash_acceleration = 5
        self.dash_duration = 0.1  # Durée du dash en secondes
        self.dash_timer = 0
        self.allow_dash = True
        self.dash_direction = 0  # Ajout de la direction du dash

    def update(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[K_q]:
            dx -= move_speed
        if key[K_d]:
            dx += move_speed

        # Jump
        if key[K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

        if key[K_LSHIFT] and self.dash_timer <= 0 and self.allow_dash and not self.on_ground:
            # Détermination de la direction du dash
            self.dash_direction = 1 if key[K_d] else -1 if key[K_q] else 0

            self.dash_speed += self.dash_acceleration
            if self.dash_speed >= self.dash_power:
                self.dash_speed = self.dash_power
                self.dash_timer = self.dash_duration
                self.allow_dash = False
            # Mettre à jour la position du joueur en fonction de la vitesse de dash et de la direction
            self.rect.x += self.dash_speed * self.dash_direction
            self.vel_y = 0
        elif self.dash_timer > 0:
            self.dash_timer -= dt
            self.dash_speed = 0
        elif self.on_ground:
            self.allow_dash = True

        # Dash
        # Supprimer cette partie de code liée au dash que vous avez commentée

        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check collisions
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True

        # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, camera):
        screen.blit(self.image, camera.apply(self.rect))



file_path = 'C:/Users/zcolucci/Documents/GitHub/GTECH1-MINI-STUDIO-Groupe-2/map/2map.txt'

with open(file_path, 'r') as file:
    world_data = [list(map(int, line.strip().split(','))) for line in file]
world = World(world_data)
player = Player(100, screen_height - 130)
camera = Camera(world.width, world.height)

run = True
while run:
    start = pygame.time.get_ticks() 
    draw_bg()

    camera.update(player)
    world.draw(camera)
    player.update()
    player.draw(camera)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    targetTime = 1000 / fps
    if dt < targetTime:
        pygame.time.delay(int(targetTime - dt))
    dt = pygame.time.get_ticks() - start
    dt /= 1000 



    pygame.display.update()
    

pygame.quit()
