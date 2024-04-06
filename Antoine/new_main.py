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
        self.jump_force : int = 45 # Force de saut
        #
        self.air_movement : float = 0 # Capacité de déplcament dans l'air
        #
        self.move_x : int = 0 # Déplacement sur l'axe x
        self.move_y : int = 0 # Déplacement sur l'axe y
        #
        self.speed : float = 0.1 # Vitesse
        self.velocity : float = 1 # élan
        self.gravity : float = 1 # Force de chute
        
        # Collisions
        self.isOnGround : bool = True

    # ------ Fonctions

    def Move(self, direction : int) : # [0] : Gauche / [1] : Droite
        if direction == 0 :
            self.move_x -= 10 * self.speed

        if direction == 1 :
            self.move_x += 10 * self.speed



    def Gravity(self) : # Le personnage subit les effets de la gravité
        print("La fonction Gravity est appellée \n")
        while self.pos_y + self.move_y < ground.top :
            self.move_y += (self.gravity * (clock.get_fps()) / 60) # On fait descendre le joueur de plus en plus vite
            print("pos : ", self.pos_y," | move : ", self.move_y," | gravity : ",  self.gravity)
            self.pos_y -= self.move_y



    def Jump(self) : # Le personnage saute
        if self.isOnGround == False : # Si le personnage est en l'air / sur un mur, on sort de la fonction
            return 
        elif self.isOnGround == True :
            # Faire une augmentation progressive de la hauteur / descente progressive
            isReached : int = 1
            
            while isReached < 10 :

                self.move_y += self.jump_force * (isReached / 2)
                isReached += 1

            self.Gravity()




            

    def Update(self) :
        print("La fonction Update est appellée \n")

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q] :
            self.Move(0)
        if keys[pygame.K_d] :
            self.Move(1)

        if pygame.K_SPACE :
            self.Jump()

        if self.pos_y > ground.y :
            self.Gravity()    
            print("Je suis au niveau du sol", self.move_y, " \n")
            self.isOnGround == True

        # Actualisation de la position
        self.pos_x += self.move_x 
        self.pos_y += self.move_y

        self.move_x = 0
        self.move_y = 0

        self.rect = (self.pos_x, self.pos_y)
        print("Je suis en ", self.rect, "\n")
        screen.blit(self.icon, self.rect) # Rafraîchissement de l'affichage




    

    






def main() :

    player : Player = Player(640, 640)
    clock.tick(60)




    


    isRunning : bool = True

    while isRunning : # Boucle de jeu

        for event in pygame.event.get() : # On parcourt les évènements

            if event.type == pygame.QUIT : # Si on ferme la fenêtre
                isRunning = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Si on appuie sur échap
                isRunning = False
        
        
        

        # Actualisation de l'affichage
        screen.blit(background, (0,0))
        player.Update()
        pygame.display.flip()




    pygame.quit()



    return

main()