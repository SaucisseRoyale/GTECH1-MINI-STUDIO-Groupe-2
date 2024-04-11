import pygame

pygame.init()

music = pygame.mixer.Sound("Antoine/assets/music.mp3")
music.set_volume(0.55) 
music.play()

# Quand on entre dans le menu, baisser le son 
 
music.set_volume(0.15)

# Quand on sort du menu, remettre le volume à sa valeur initiale

music.set_volume(0.55) 



# Dans la boucle de jeu
if music.get_length() == len(music) :
    music.fadeout(90000)
    music.play()