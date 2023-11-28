import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

FPS = 30

clock = pygame.time.Clock()
finished = False

while not finished:
    screen.fill(color='white')
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        else:
            print(event.type)

pygame.quit()