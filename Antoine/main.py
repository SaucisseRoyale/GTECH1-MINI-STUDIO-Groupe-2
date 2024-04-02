import pygame;

pygame.init()
clock = pygame.time.Clock()


# Creation de la fenetre de jeu
x_screen : int = 1080
y_screen : int = 720
pygame.display.set_caption("Python_Game")
screen = pygame.display.set_mode((x_screen,y_screen))



# MAIN
def main() :
    # Preparation et lancement de la musique
    pygame.mixer.music.load(filename="music.mp3")
    pygame.mixer.music.play(-1)

    isRunning : bool = True

    # Variables GLOBALES
    isRunning : bool = True
    gravity : int = 1



    # Variables JOUEUR
    rect_player = pygame.Rect(520,340,20,20)
    jump_force : int = 5
    jump_count : int = 1
    player_speed : int = 5

    # BOUCLE DE JEU
    while isRunning :

        clock.tick(60)
        
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get() : 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isRunning = False



            if keys[pygame.K_q] : # GAUCHE
                if rect_player.x - player_speed >= 0 :
                    rect_player.x -= player_speed

            elif keys[pygame.K_d] : # DROITE
                if rect_player.x + player_speed <= x_screen :
                    rect_player.x += player_speed

            if keys[pygame.K_SPACE] : # SAUT
                if jump_count >= 1 :
                    rect_player.y -= jump_force
                    
    
    # Actualisation de l'affichage
        screen.fill(0)
        pygame.draw.rect(screen, (255,0,0), rect_player)
        pygame.display.flip()

        

    # Refaire une partie / Menu du jeu
    pygame.quit()
    

main()
    
                
