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
        img = pygame.image.load("Antoine/sanic.gif")
        self.icon = pygame.transform.scale(img, (56,56))
        self.rect = self.icon.get_rect()
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
        
        # Appliquer la gravité
        self.velocity += 1 * 0.016 
        if self.velocity > 10:  
            self.velocity = 10

        moveAlongY += self.velocity

        # Vérifier le contact avec le sol
        if self.rect.bottom + moveAlongY > x_screen:
            moveAlongY = y_screen - self.rect.bottom
            self.velocity = 0 
            self.jump_count += 1

        # Mise à jour des coordonnées du joueur
        self.rect.x += moveAlongX
        self.rect.y += moveAlongY
        
        # Affichage
        screen.blit(self.icon, self.rect)



    

# MAIN
def main() :
    # Preparation et lancement de la musique
    pygame.mixer.music.load(filename="Antoine/music.mp3")
    pygame.mixer.music.play(-1)

    # Préparation du fond du niveau
    background = pygame.image.load("Antoine/background.png").convert()

    isRunning : bool = True

    # Variables GLOBALES
    isRunning : bool = True
    gravity : int = 1


    rect_player = Player(520, 340)
    

    # BOUCLE DE JEU
    while isRunning :

        # Initialisation du jeu / décor
        clock.tick(60)
        screen.blit(background, (0,0))
        

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT :
                isRunning = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isRunning = False

        # Actualisation de l'affichage
        rect_player.update()
        pygame.display.flip()
        
        
            
    

    

    # Refaire une partie / Menu du jeu
    pygame.quit()
    

main()
