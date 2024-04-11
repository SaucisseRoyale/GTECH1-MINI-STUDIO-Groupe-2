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


res = "projet pygame merge paul zian/img/mouvement/hidl/animation stand1.png"
animations_walk = ["projet pygame merge paul zian/img/mouvement/run/course1.png", "projet pygame merge paul zian/img/mouvement/run/course2.png", "projet pygame merge paul zian/img/mouvement/run/course3.png"]
animations_standing = ["projet pygame merge paul zian/img/mouvement/hidl/animation stand1.png", "projet pygame merge paul zian/img/mouvement/hidl/animation stand2.png", "projet pygame merge paul zian/img/mouvement/hidl/animation stand3.png", "projet pygame merge paul zian/img/mouvement/hidl/animation stand4.png", "projet pygame merge paul zian/img/mouvement/hidl/animation stand5.png"]
animations_air_jump = ["projet pygame merge paul zian/img/mouvement/double jump/double jump1.png", "projet pygame merge paul zian/img/mouvement/double jump/double jump2.png", "projet pygame merge paul zian/img/mouvement/double jump/double jump3.png", "projet pygame merge paul zian/img/mouvement/double jump/double jump4.png"]
animations_jump = ["projet pygame merge paul zian/img/mouvement/run jump/run_jump1.png", "projet pygame merge paul zian/img/mouvement/run jump/run_jump2.png", "projet pygame merge paul zian/img/mouvement/run jump/run_jump3.png", "projet pygame merge paul zian/img/mouvement/run jump/run_jump4.png"]
animations_monte = ["projet pygame merge paul zian/img/mouvement/run jump/run_jump5.png", "projet pygame merge paul zian/img/mouvement/run jump/run_jump6.png"]
animations_falling = ["projet pygame merge paul zian/img/mouvement/run jump/run_jump7.png", "projet pygame merge paul zian/img/mouvement/run jump/run_jump8.png"]
animations_landing = ["projet pygame merge paul zian/img/mouvement/run jump/run_jump9.png", "iprojet pygame merge paul zian/mg/mouvement/run jump/run_jump10.png"]
animations_dash = ["projet pygame merge paul zian/img/mouvement/dash/dash1.png", "projet pygame merge paul zian/img/mouvement/dash/dash2.png",]
animations_start_slide = ["projet pygame merge paul zian/img/mouvement/slide/slide1.png"]
animations_slide = ["projet pygame merge paul zian/img/mouvement/slide/slide2.png", "projet pygame merge paul zian/img/mouvement/slide/slide3.png"]
#define colours

GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

mountain_img = pygame.image.load('projet pygame merge paul zian/World_Editor/LevelEditor-main/img/Background/background_immeubles.png').convert_alpha()
sky_img = pygame.image.load('projet pygame merge paul zian/World_Editor/LevelEditor-main/img/Background/sky_cloud.png').convert_alpha()

from enum import Enum
class FaceCollision(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

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
        for i in range(171):
            
            tile_images[i] = pygame.image.load(f"projet pygame merge paul zian/img/Cutted/{i}.png").convert_alpha()

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
                    mask_image = mask.to_surface()
                    tile_data = (img, img_rect, tile, mask, mask_image)  
                    self.tile_list.append(tile_data)
                col_count += 1
            row_count += 1


    def draw(self, camera):
        for tile in self.tile_list:
            screen.blit(tile[0], camera.apply(tile[1]))

class Player:
    def __init__(self, x, y):
        link_img = "projet pygame merge paul zian/img/mouvement/hidl/animation stand1.png"
        self.img = pygame.image.load(link_img).convert_alpha()
        self.image = pygame.transform.scale(self.img, (40, 40))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = None
        self.col_p = [0,0]
        
        self.walk_speed = 500 #vitesse de marche
        self.speed_multiplication = 1
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.dir_x = 0
        self.dir_y = 0

        self.gravity = 1.1 #force de la gravité
        self.gravity_coefficient = 0.7 #acceleration de la gravité

        self.on_ground = False
        self.on_wall = False

        self.dash_power = 40 #puissance du dash
        self.dash_acceleration = 5 #accélération du dash
        self.dash_duration = 0.1 #durée du dash
        self.dash_speed = 0
        self.dash_timer = 0
        self.dash_direction = 0
        self.dash_allow = True

        self.jump_power = 17 #puissance du saut
        self.maxjump = 2 #nombre de sauts
        self.nbr_jump = 0
        self.space_pressed = False

        self.slide_speed = 4.0 #vitesse du slide (quoeficient d'acceleration de la vitesse)
        self.slide_duration = 0.3 #durée du slide
        self.is_sliding = False
        self.slide_timer = 0

        #listes des annimation
        self.annim_standing = 0
        self.annim_walk = 0
        self.annim_jump = 0
        self.annim_air_jump = 0
        self.annim_monte = 0
        self.annim_falling = 0
        self.annim_falling_landing = 0
        self.annim_dash = 0
        self.annim_start_slide = 0
        self.annim_slide = 0
        
        self.annim_timer = 0
        self.annim_timer_frame = 0.1
        self.nbr_frame = 0
        self.player_oritentation = 1
        self.x_size = 56

    def annimation(self):
        walk = False
        jump = False
        air_jump = False
        falling = False
        dash = False
        slide = False
        monte = False
        nbr_frame_slide = 2
        nbr_frame_saut = 4

        liste_var = [walk, jump, air_jump, monte, falling, dash, slide]
        liste_annim = [self.annim_walk, self.annim_jump, self.annim_air_jump, self.annim_monte, self.annim_falling, self.annim_dash, self.annim_slide]
        self.annim_timer -= dt
        if self.annim_timer <= 0:
            self.annim_timer = self.annim_timer_frame

            if self.dash_timer > 0 : #dash
                dash = True
                res = animations_dash[self.annim_dash]
                self.annim_dash = (self.annim_dash + 1) % (len(animations_dash))
                self.x_size = 40
            
            elif self.is_sliding:
                slide = True
                if self.nbr_frame <= nbr_frame_slide:
                    res = animations_start_slide[self.annim_start_slide]
                    self.annim_start_slide = (self.annim_start_slide + 1) % (len(animations_start_slide))
                    self.nbr_frame += 1
                    self.x_size = 80
                else:
                    res = animations_slide[self.annim_slide]
                    self.annim_slide = (self.annim_slide + 1) % (len(animations_slide))
                    self.x_size = 80

            elif self.space_pressed and self.on_ground and self.nbr_frame <= nbr_frame_saut: #saut
                jump = True
                res = animations_jump[self.annim_jump]
                self.annim_jump = (self.annim_jump + 1) % (len(animations_jump))
                self.nbr_frame += 1
                self.x_size = 40
            
            elif self.space_pressed and not self.on_ground and self.nbr_frame <= nbr_frame_saut: #2eme saut 
                air_jump = True
                res = animations_air_jump[self.annim_air_jump]
                self.annim_air_jump = (self.annim_air_jump + 1) % (len(animations_air_jump))
                self.nbr_frame += 1
                self.x_size = 40

            elif self.current_speed_y < 0 and not self.on_ground: #monté
                monte = True
                res = animations_monte[self.annim_monte]
                self.annim_monte = (self.annim_monte + 1) % (len(animations_monte))
                self.x_size = 40

            elif self.current_speed_y  > 5 : #chute
                res = animations_falling[self.annim_falling]
                self.annim_standing = (self.annim_standing + 1) % (len(animations_falling))
                falling = True
                self.x_size = 40
            
            elif (key[K_d] or key[K_q]) and self.on_ground: #walk 
                res = animations_walk[self.annim_walk]
                self.annim_walk = (self.annim_walk + 1) % (len(animations_walk))
                walk = True
                self.x_size = 75
            
            else:
                res = animations_standing[self.annim_standing]
                self.annim_standing = (self.annim_standing + 1) % (len(animations_standing))
                self.x_size = 40


            for i in liste_var:
                if not liste_var[i]:
                    liste_annim[i] = 0

            if not slide and not jump and not air_jump:
                self.nbr_frame = 0
                    
            self.refresh_img(res)
            

    
    def refresh_img(self, link):
        self.img = pygame.image.load(link).convert_alpha()
        self.image = pygame.transform.scale(self.img, (self.x_size, 40))

    def set_velocity_x(self, dir_x, speed):
        self.current_speed_x = dir_x * speed

    def set_velocity_y(self, dir_y, speed):
        self.current_speed_y = dir_y * speed


    def update(self):
        

        dx = self.current_speed_x * dt
        dy = self.current_speed_y * dt

        self.current_speed_y += self.gravity * self.gravity_coefficient ** dt
        dy += self.current_speed_y

    # Apply gravity
        self.current_speed_y += self.gravity

        if self.current_speed_y > 10:
            self.current_speed_y = 10
        dy += self.current_speed_y
    #end of gravity

    # Check collisions
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if tile[2] == 21:  
                    player.set_velocity_y(-1, player.jump_power)
                    self.on_ground = False
                    break 
                if tile[2] == 0:  
                    print("Death")
                    pygame.quit()
                    break 

            # Gestion des autres collisions
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
            self.player_oritentation = 1
            self.current_speed_x = max(0, self.current_speed_x - ( 2000 * dt  * self.speed_multiplication))
        else:
            self.current_speed_x = min(0, self.current_speed_x + ( 2000 * dt  * self.speed_multiplication))
            self.player_oritentation = -1
    #end of Update player coordinates
    """def get_collision(self, r1: pygame.rect.Rect, r2: pygame.rect.Rect) -> tuple[FaceCollision, int]:
        if r1.right < r2.left:
            return FaceCollision.NONE, 0
        
        if r1.left > r2.right:
            return FaceCollision.NONE, 0
        
        if r1.bottom < r2.top:
            return FaceCollision.NONE, 0
        
        if r1.top > r2.bottom:
            return FaceCollision.NONE, 0

        distances: list[int] = []
        distances.append( abs(r1.right - r2.left) )
        distances.append( abs(r1.left - r2.right) )
        distances.append( abs(r1.bottom - r2.top) )
        distances.append( abs(r1.top - r2.bottom) )

        face = FaceCollision.NONE
        min_distance = 9999
        faces = [FaceCollision.LEFT, FaceCollision.RIGHT, FaceCollision.TOP, FaceCollision.BOTTOM]
        for i in range(0, 4):
            if min_distance > distances[i]:
                face = faces[i]
                min_distance = distances[i]
        
        return face, min_distance"""

    def draw(self, camera):
        if self.player_oritentation == 1:
            screen.blit(self.image, camera.apply(self.rect))
        elif self.player_oritentation == -1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, camera.apply(self.rect))
        if self.mask_image != None:
            screen.blit(self.mask_image, (0,0))
        pygame.draw.rect(screen, (255,0,0), (self.col_p[0],self.col_p[1],1,1))
        #screen.set_at((self.col_p[0], self.col_p[1]), (255,0,0))



file_path = 'projet pygame merge paul zian/map/2map.txt'

with open(file_path, 'r') as file:
    world_data = [list(map(int, line.strip().split(','))) for line in file]
world = World(world_data)
player = Player(500, screen_height - 200)
camera = Camera(world.width, world.height)
run = True
while run:
    start = pygame.time.get_ticks() 

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
        elif not player.space_pressed and player.nbr_jump < player.maxjump and not player.on_ground and not player.on_wall:
            player.nbr_jump += 1
            player.set_velocity_y(-1, player.jump_power)
        player.space_pressed = True
    else:
        player.space_pressed = False
#end of jump

# Dash
    if key[K_LCTRL] and player.dash_timer <= 0 and player.dash_allow and not player.on_ground and not player.space_pressed :
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
        player.speed_multiplication = 0.5
        if player.on_ground and player.slide_timer <= 0 and not player.is_sliding:
            player.current_speed_x *=  player.slide_speed
            player.is_sliding = True
    else:
        player.is_sliding = False
        player.speed_multiplication = 1
 #end of slide

    player.annimation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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