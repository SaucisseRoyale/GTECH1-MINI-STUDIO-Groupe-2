import pygame

pygame.init()


screen = pygame.display.set_mode((1792, 1024))


image = pygame.image.load("tile_0000.png").convert_alpha() 
background = pygame.image.load("fond.webp").convert()
image = pygame.transform.scale(image, (96, 96))
rect = image.get_rect()

clock = pygame.time.Clock()
continuer = True
x = 0
y = 0
moveSpeed = 6

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT] and rect.left > 0:
        rect.x -= moveSpeed
    if pressed[pygame.K_RIGHT] and rect.right < 1792:
        rect.x += moveSpeed
    if pressed[pygame.K_DOWN] and rect.bottom < 1024:
        rect.y += moveSpeed
    if pressed[pygame.K_UP] and rect.top > 0:
        rect.y -= moveSpeed
    if pressed[pygame.K_SPACE]:
        continuer = False

   
    screen.blit(background, (0, 0))
    

    screen.blit(image, (rect))
    

    pygame.display.flip()
    
   
    clock.tick(60)

pygame.quit()
