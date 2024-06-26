import pygame

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


# Creation de la fenetre de jeu
x_screen : int = 1080
y_screen : int = 720

tile_size = 50

pygame.display.set_caption("Python_Game")
screen = pygame.display.set_mode((x_screen,y_screen))

font = pygame.font.SysFont('Consolas', 30)


# Initialisation des différents effets sonores utilisés
pygame.mixer.init()
# Saut
jump_sound = pygame.mixer.Sound("Antoine/assets/jump.wav")
jump_sound.set_volume(50)
# Saut mural
wallJump_sound = pygame.mixer.Sound("Antoine/assets/wall_jump.wav")
wallJump_sound.set_volume(50)
# Mort/chute dans le vide
fallVoid_sound = pygame.mixer.Sound("Antoine/assets/fall_void.wav")
fallVoid_sound.set_volume(50)



class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load("Antoine/assets/tile_0001.png").convert_alpha()
        grass_img = pygame.image.load("Antoine/assets/tile_0002.png").convert_alpha()

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])



class Player :
    # Variables JOUEUR
    def __init__(self, x, y) -> None:
        img = pygame.image.load("Antoine/assets/sanic.gif")
        self.icon = pygame.transform.scale(img, (56,56))
        self.rect = self.icon.get_rect()
        self.width = self.icon.get_width()
        self.height = self.icon.get_height() 
        self.jump_force : int = 15
        self.jump_count : int = 0
        self.velocity : float = 0
        self.speed : int = 5
        self.rect.x = x
        self.rect.y = y

        # Variables wall jump
        self.canWallJump : bool = False
        self.wallJumpForce : float = 10



    def update(self) :
        self.moveAlongX = 0
        self.moveAlongY = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q] : # GAUCHE
            # Son de déplacement
            self.moveAlongX -= self.speed

        elif keys[pygame.K_d] : # DROITE
            # Son de déplacement
            self.moveAlongX += self.speed 

        

        # Vérifier le contact avec les bords de l'écran
        if self.rect.bottom + self.moveAlongY > x_screen:
            self.moveAlongY = y_screen - self.rect.bottom
            self.velocity = 0 
            self.jump_count += 1

        # Vérifier les collisions avec des pans de murs verticaux
        #if self.rect.left 


        world_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        world = World(world_data)


        # Vérifier les collisions avec le sol
        for tile in world.tile_list:

            if tile[1].colliderect((self.rect.x + self.moveAlongX, self.rect.y), (self.width, self.height)):
                self.moveAlongX = 0

            if tile[1].colliderect((self.rect.x, self.rect.y + self.moveAlongY), (self.width, self.height)):
                
                if self.velocity < 0:
                    self.moveAlongY = tile[1].bottom - self.rect.top
                    self.velocity = 0

                elif self.velocity >= 0:
                    self.moveAlongY = tile[1].top - self.rect.bottom
                    self.velocity = 0

                    if self.jump_count == 0 :
                        self.jump_count += 1

    
        
        # Appliquer la gravité
        self.velocity += 1 * 0.016 
        if self.velocity > 10:  
            self.velocity = 10

        self.moveAlongY += self.velocity





        # Mise à jour des coordonnées du joueur
        self.rect.x += self.moveAlongX
        self.rect.y += self.moveAlongY
        
        # Affichage
        world.draw()
        screen.blit(self.icon, self.rect)


def jump(player : Player):
    jump_sound.play(0) 
    player.jump_count -= 1 # On enleve un saut du compteur (=/= 0 en vue du double saut)
    player.moveAlongY -= 100


    

# MAIN
def main() :
    # Preparation et lancement de la musique
    pygame.mixer.music.load(filename="Antoine/assets/music.mp3")
    pygame.mixer.music.play(-1)

    # Préparation du fond du niveau
    background = pygame.image.load("Antoine/assets/background.png").convert()
    background = pygame.transform.scale(background, (x_screen, y_screen))

    # Variables GLOBALES
    isRunning : bool = True
    gravity : int = 1

    rect_player = Player(520, 340)

    # BOUCLE DE JEU
    while isRunning :

        # Initialisation du jeu / décor

        

        clock.tick(120)
        screen.blit(background, (0,0))
        screen.blit(font.render(str(rect_player.jump_count), True, (0,0,0) ), (0,0)) # Déboguage variable : compteur de sauts

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT :
                isRunning = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isRunning = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                jump(rect_player)

        # Actualisation de l'affichage
       
        rect_player.update()
        pygame.display.flip()
        
        
            
    

    

    # Refaire une partie / Menu du jeu
    pygame.quit()
    

main()
