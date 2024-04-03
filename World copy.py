import pygame
import time
from pygame.locals import *
import pickle

pygame.init()

screen_width = 1000
screen_height = 700
tile_size = 50
move_speed = 5

clock = pygame.time.Clock()
fps = 60
dt = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

bg_img = pygame.image.load("sky-blue-color-solid-background-1920x1080.png").convert()

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
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - screen_width), x)  # right
        y = max(-(self.height - screen_height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)

class World:
    def __init__(self, data):
        self.tile_list = []

        if not data:  # Vérifie si data est vide
            print("world_data est vide!")
            self.width = 0
            self.height = 0
            return  # Sort du constructeur pour éviter d'autres erreurs

        self.width = len(data[0]) * tile_size
        self.height = len(data) * tile_size

        dirt_img = pygame.image.load("dirt.png").convert_alpha()
        grass_img = pygame.image.load("grass.png").convert_alpha()

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
        self.dash = True

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

        # Dash
        if key[K_LSHIFT] and key[K_q] and self.dash:
            dx -= 20
            time.sleep(0.2)
            self.dash = False

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


with open('map/1map.txt', 'r') as file:
    world_data = [list(map(int, line.strip().split(','))) for line in file]

world = World(world_data)
player = Player(100, screen_height - 130)
camera = Camera(world.width, world.height)

run = True
while run:
    start = pygame.time.get_ticks() 
    screen.blit(bg_img, (0, 0))

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
