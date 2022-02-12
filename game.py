import sys, pygame

pygame.init()
SIZE = WIDTH , HEIGHT = 320, 240
screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

def welcome():
    background = pygame.image.load("welcome.png").convert()
    background = pygame.transform.scale(background, SIZE)
    while True:
        screen.blit(background, (0,0))
        clock.tick(10)
        pygame.display.update()


def setupPlayerDetails():
    pass


functions = [welcome, setupPlayerDetails]
i = 0
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if i == 0 and keys[pygame.
        
    functions[i]() 