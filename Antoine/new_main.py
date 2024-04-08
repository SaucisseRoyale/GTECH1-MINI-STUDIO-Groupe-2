import pygame

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


# Creation de la fenetre de jeu

    # Dimensions de la fenêtre de jeu
x_screen : int = 1280 
y_screen : int = 720

    # Caractéristiques de la fenêtre de jeu
pygame.display.set_caption("Python_Game")
screen = pygame.display.set_mode((x_screen,y_screen))

# Initialisation Niveau

# ------ Préparation du fond du niveau
background = pygame.image.load("Antoine/assets/background.png").convert()
background = pygame.transform.scale(background, (x_screen, y_screen))

# ------ Création du sol du niveau
ground = pygame.rect.Rect(0, 620, 1280, 100)
pygame.draw.rect(background, (0,0,0), ground)

# ------ Création d'une zone de texte
arial_font = pygame.font.SysFont("arial", 10)

# ------ Classes

class Player():
    
    def __init__(self, x, y) -> None:

        # Position du joueur
        self.pos_x : int = x
        self.pos_y : int = y

        # Affichage du joueur
        self.img = pygame.image.load("Antoine/assets/sanic.gif")
        self.icon = pygame.transform.scale(self.img, (56,56))
        self.rect = self.icon.get_rect() # Variable qui permet l'étude des collisions du joueur
        
        # Forces qui s'appliquent au joueur
        self.jump_force : int = 1000 # Force de saut
        #
        self.air_movement : float = 0 # Capacité de déplcament dans l'air
        #
        self.move_x : int = 0 # Déplacement sur l'axe x
        self.move_y : int = 0 # Déplacement sur l'axe y
        #
        self.speed : float = 150 # Vitesse p/s

        self.vertical_speed = 0
        self.vertical_acceleration = 0
        self.vertical_distance_accomplished = 0

        self.jump_speed_min = 100
        self.jump_speed_max = 500
        self.jump_deceleration = 50
        self.jump_distance = 100

        self.gravity_speed_min = 100
        self.gravity_speed_max = 500
        self.gravity_acceleration = 250

        # Collisions
        self.isOnGround : bool = True # état sur le sol

    # ------ Fonctions

    def Move(self, dt : float, direction : int) : # [0] : Gauche / [1] : Droite
        if direction == 0 :
            self.move_x -= self.speed * dt

        if direction == 1 :
            self.move_x += self.speed * dt



    def Jump(self, dt : float) : # Le personnage saute
        print("La fonction Jump est appellée \n")
        if self.isOnGround == False : # Si le personnage est en l'air / sur un mur, on sort de la fonction
            print("Je ne peux pas sauter \n")
            return
        
         # Si le personnage est sur le sol, on le fait sauter
        self.isOnGround = False
        print("Je saute \n")
        # [A FAIRE]  -->  Faire une augmentation progressive de la hauteur / descente progressive

        self.vertical_speed = -self.jump_speed_max
        self.vertical_acceleration = self.jump_deceleration
        self.vertical_distance_accomplished = 0


    def Update(self, dt : float) :
        print("La fonction Update est appellée \n")

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] :
            print("Je vais à gauche \n")
            self.Move(dt, 0)
        if keys[pygame.K_d] :
            print("Je vais à droite \n")
            self.Move(dt, 1)

        if self.isOnGround == False:
            self.move_y += self.vertical_speed * dt
            self.vertical_speed += self.vertical_acceleration * dt

            if self.vertical_speed < 0:
                self.vertical_speed = min(-self.jump_speed_min, self.vertical_speed)
                self.vertical_distance_accomplished += abs(self.move_y)
                if self.vertical_distance_accomplished >= self.jump_distance:
                    self.vertical_speed = self.gravity_speed_min
                    self.vertical_acceleration = self.gravity_acceleration

            else:
                self.vertical_speed = min(self.gravity_speed_max, self.vertical_speed)
                if (self.pos_y + self.move_y) >= ground.top:
                    self.isOnGround = True

        # Actualisation de la position
        self.pos_x += self.move_x 
        self.pos_y += self.move_y
        #
        self.rect = (self.pos_x, self.pos_y)

        # Réinitialisation des variables de déplacement
        self.move_x = 0
        self.move_y = 0
        
        print("Je suis en ", self.rect, "\n")

        screen.blit(self.icon, self.rect) # Rafraîchissement de l'affichage



def main() :

    player : Player = Player(640, 640)
    

    isRunning : bool = True


    dt = 0
    while isRunning : # Boucle de jeu
        start = pygame.time.get_ticks()

        for event in pygame.event.get() : # On parcourt les évènements

            if event.type == pygame.QUIT : # Si on ferme la fenêtre
                isRunning = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Si on appuie sur échap
                isRunning = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                print("Je saute \n")
                player.Jump(dt)




        # Actualisation de l'affichage
        text = arial_font.render(f"{clock.get_fps():.2f} FPS", True, (255,255,255))
        screen.blit(background, (0,0))
        screen.blit(text, (0,0))
        
        
        player.Update(dt)
        
        pygame.display.flip()

        clock.tick(60) # Tx de rafraîchissement (fps)
        end = pygame.time.get_ticks()
        dt = (end - start) / 1000



    pygame.quit()



    return

main()