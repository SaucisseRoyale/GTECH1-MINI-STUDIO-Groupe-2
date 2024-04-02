import pygame

pygame.init()
clock = pygame.time.Clock()


# Creation de la fenetre de jeu
x_screen : int = 1080
y_screen : int = 720
pygame.display.set_caption("Python_Game")
screen = pygame.display.set_mode((x_screen,y_screen))

class Player :
    # Variables JOUEUR
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect(520,340,20,20)
        self.jump_force : int = 5
        self.jump_count : int = 1
        self.velocity : float = 0
        self.speed : int = 1
        self.rect.x = x
        self.rect.y = y

    def update(self) :
        moveAlongX = 0
        moveAlongY = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q] : # GAUCHE
            moveAlongX -= self.speed

        elif keys[pygame.K_d] : # DROITE
            moveAlongX += self.speed 

        if keys[pygame.K_SPACE] : # SAUT

            self.jump_count -= 1 # On enleve un saut du compteur (=/= 0 en vue du double saut)
            moveAlongY -= 2
        
        # Condition qui, dans le cadre d'une collision avec le sol, 
        #self.jump_count += 1
        
        # Appliquer la gravité
        self.velocity += 1 * 0.016 
        if self.velocity > 10:  
            self.velocity = 10

        moveAlongY += self.velocity

        # Vérifier le contact avec le sol
        if self.rect.bottom + dy > x_screen:
            dy = y_screen - self.rect.bottom
            self.velocity = 0 
            self.jumped = False

        # Mise à jour des coordonnées du joueur
        self.rect.x += moveAlongX
        self.rect.y += moveAlongY

        pygame.draw.rect(screen, (255,0,0), self.rect)
        pygame.display.flip()
        
        screen.blit(screen, self.rect)




                

    

# MAIN
def main() :
    # Preparation et lancement de la musique
    pygame.mixer.music.load(filename="music.mp3")
    pygame.mixer.music.play(-1)

    isRunning : bool = True

    # Variables GLOBALES
    isRunning : bool = True
    gravity : int = 1



    

    # BOUCLE DE JEU
    while isRunning :

        clock.tick(60)
        
        
        
        for event in pygame.event.get() : 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isRunning = False



            
    
    rect_player = Player(520, 340)


    # Actualisation de l'affichage
    screen.fill(0)
    
    

    

    # Refaire une partie / Menu du jeu
    pygame.quit()
    

main()
    
                
