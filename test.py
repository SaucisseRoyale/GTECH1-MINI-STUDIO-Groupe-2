import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))
image = pygame.image.load("tile_0000.png").convert()
clock = pygame.time.Clock()
continuer = True
x = 0
y = 0

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        x -= 1
    if pressed[pygame.K_RIGHT]:
        x += 1
    if pressed[pygame.K_DOWN]:
        y += 1  
    if pressed[pygame.K_UP]:
        y -= 1
    if pressed[pygame.K_SPACE]:
        continuer = False

    screen.fill((0, 0, 0))
    screen.blit(image, (x, y))  
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
