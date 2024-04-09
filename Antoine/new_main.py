import pygame

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


# Creation de la fenetre de jeu

    # Dimensions de la fenêtre de jeu
x_screen : int = 1920
y_screen : int = 1080

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

class Force():
    def __init__(self):
        self.is_active = False
        self.current_speed = 0

    def Start(self, direction, start_speed, end_speed, acceleration):
        self.StartWithDistance(direction, -1, start_speed, end_speed, acceleration)

    def StartWithDistance(self, direction, distance, start_speed, end_speed, acceleration):
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
        # Quand isOnGrond == False :
        self.air_movement : float = 0 # Capacité de déplcament dans l'air
        #
        self.move_x : int = 0 # Déplacement sur l'axe x
        self.move_y : int = 0 # Déplacement sur l'axe y
        #
        self.speed : float = 500 # Vitesse pxl/s

        self.gravity_force = Force()

        # Collisions
        self.isOnGround : bool = True # état sur le sol
        self.isJumping = False

    # ------ Fonctions

    def Move(self, dt : float, direction : int) : # [0] : Gauche / [1] : Droite
        if direction == 0 :
            self.move_x -= self.speed * dt

        if direction == 1 :
            self.move_x += self.speed * dt



    def Jump(self) : # Le personnage saute
        print("La fonction Jump est appellée \n")

        if self.isOnGround == False : # Si le personnage est en l'air / sur un mur, on sort de la fonction
            print("Je ne peux pas sauter \n")
            return
        
        # Sinon on le fait sauter
        self.isOnGround = False
        self.isJumping = True
        
        print("Je saute \n")

        self.gravity_force.StartWithDistance((0,-1), 200, 850, 500, -50)



    def StopJump(self):
        if self.isJumping == False:
            return
        
        self.isJumping = False
        self.gravity_force.Start((0,1), 100, 750, 500)



    def Update(self, dt : float) :
        print("La fonction Update est appellée \n")

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] :
            print("Je vais à gauche \n")
            self.Move(dt, 0)
        if keys[pygame.K_d] :
            print("Je vais à droite \n")
            self.Move(dt, 1)

        gravity_move_x, gravity_move_y  = self.gravity_force.Update(dt)
        if self.gravity_force.IsActive() == False:
            self.StopJump()
        
        if self.isJumping == False and self.isOnGround == False and (self.pos_y + self.move_y) >= ground.top:
            self.isOnGround = True
            self.gravity_force.Stop()

        self.move_x += gravity_move_x
        self.move_y += gravity_move_y

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
                player.Jump()

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE :
                print("Je saute plus\n")
                player.StopJump()



        # Actualisation de l'affichage
        text = arial_font.render(f"{clock.get_fps():.0f} FPS", True, (255,255,255))
        screen.blit(background, (0,0))
        screen.blit(text, (0,0))
        
        player.Update(dt)
        
        pygame.display.flip()

        clock.tick(160) # Tx de rafraîchissement (fps)
        end = pygame.time.get_ticks()
        dt = (end - start) / 1000



    pygame.quit()



    return

main()