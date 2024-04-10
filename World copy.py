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
mountain_img = pygame.image.load('World_Editor/LevelEditor-main/img/Background/background_immeubles.png').convert_alpha()
sky_img = pygame.image.load('World_Editor/LevelEditor-main/img/Background/sky_cloud.png').convert_alpha()

def draw_bg():
    width = sky_img.get_width()
    total_width = screen_width + width  
    num_images = total_width // width + 1 
    
    for x in range(num_images):
        # Ajustez ces valeurs pour changer la position en Y
        sky_y_pos_adjustment = 0
        mountain_y_pos_adjustment = 300
        
        sky_x_pos = (x * width) - scroll * 0.5
        mountain_x_pos = (x * width) - scroll * 0.6
        
        screen.blit(sky_img, (sky_x_pos, 0 + sky_y_pos_adjustment))
        screen.blit(mountain_img, (mountain_x_pos, screen_height - mountain_img.get_height() - 300 + mountain_y_pos_adjustment))

        

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.move(self.camera.topleft)

    def update(self, target):
        global scroll 
        
        x = -target.rect.centerx + int(screen_width / 2)
        y = -target.rect.centery + int(screen_height / 2)

        # limit scrolling to map size
        x = min(0, x)  
        y = min(0, y)  
        x = max(-(self.width - screen_width), x) 
        y = max(-(self.height - screen_height), y) 

        self.camera = pygame.Rect(x, y, self.width, self.height)
        scroll = -x  

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

        # Déclaration d'un dictionnaire pour stocker les images des tuiles
        tile_images = {}

        # Boucle pour charger les tuiles de 0 à 155
        for i in range(156):
            
            tile_images[i] = pygame.image.load(f"img/Cutted/{i}.png").convert_alpha()

        # Initialisation de self.tile_images avec le dictionnaire des tuiles chargées
        self.tile_images = tile_images

        # Boucle pour traiter les données des tuiles
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile in self.tile_images:
                    img = pygame.transform.scale(self.tile_images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    mask = pygame.mask.from_surface(img) 
                    tile_data = (img, img_rect, tile, mask)  
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
        self.mask = pygame.mask.from_surface(self.image)
        self.vel_y = 0
        self.on_ground = False
        self.jump_power = 20
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

        if key[K_ESCAPE]:
            QUIT()
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


        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check collisions
        self.rect.x += dx
        self.rect.y += dy

        # Nouvelle gestion des collisions avec les tuiles en utilisant les masques
        for tile in world.tile_list:
            # Obtention de la position relative du joueur par rapport à la tuile pour la vérification des masques
            offset_x = tile[1].x - self.rect.x
            offset_y = tile[1].y - self.rect.y
            
            # Vérification de la collision entre le masque du joueur et celui de la tuile
            collision_point = self.mask.overlap(tile[3], (offset_x, offset_y))
            
            if collision_point:
                # Collision détectée, gérer en fonction de la position et du type de collision
                if dy > 0:  
                    self.rect.y = tile[1].y - self.height
                    dy = 0
                    self.on_ground = True
                    self.vel_y = 0
                elif dy < 0:
                    self.rect.y = tile[1].bottom
                    dy = 0
                    self.vel_y = 0
                if dx > 0:  
                    self.rect.x = tile[1].left - self.width
                    dx = 0
                elif dx < 0:
                    self.rect.x = tile[1].right
                    dx = 0



    def draw(self, camera):
        screen.blit(self.image, camera.apply(self.rect))



file_path = 'map/2map.txt'

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