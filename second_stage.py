import os
import sys
import random
import pygame
 
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 1200
HEIGHT = 800

class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(50, 10, 50, 50)
        player_image = pygame.image.load("player.png")
        player_image = pygame.transform.scale(player_image, (50, 50))
        self.surf = player_image
        self.rect = self.surf.get_rect(
            center = (50,50)
        )
 
    def move(self, dx, dy):        
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):      

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: 
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
 
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 25, 25)
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direct, radius):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("enemy.png")
        self.rect = self.surf.get_rect(
            center = (x, y)
        )
        self.basepos = self.rect.copy()
        self.speed = 1
        self.direction = 1
        self.radius = radius
        self.direct = direct

    def update(self):
        dir = 0
        if self.direct == "hor":
            dir = 0
        else:
            dir = 1

        if self.rect.center[dir] < self.basepos.center[dir] - self.radius:
            self.direction = 1

        elif self.rect.center[dir] > self.basepos.center[dir] + self.radius:
            self.direction = -1
        
        if self.direct == "hor":
            self.rect.move_ip(self.direction*self.speed, 0)
        else:
            self.rect.move_ip(0, self.direction*self.speed)
enemies = pygame.sprite.Group()

new_enemy = Enemy(300, 737, "hor", 200)
enemies.add(new_enemy)
new_enemy = Enemy(490, 350, "vert", 150) 
enemies.add(new_enemy)
new_enemy = Enemy(900, 60, "hor", 200)
enemies.add(new_enemy)


pygame.init()
screen = pygame.display.set_mode((1200, 800))
 
clock = pygame.time.Clock()
walls = []
player = Player()
 

level = ['W   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
'W            W           W                     W',
'W            W           W                     W',
'W            W           W                     W',
'W   WWWWWW   W   WWWWW   W   WWWWWWWWW   W   WWW',
'W   W        W       W       W   W       W     W',
'W   W        W       W       W   W       W     W',
'W   W        W       W       W   W       W     W',
'W   W        W       WWWWW   W   W   WWWWW     W',
'W   WWWWWWWWWWWWWW       W       W   W         W',
'W      W         W       W       W   W         W',
'W      W         W       W       W   W         W',
'W      W         W       W       W   WWWWWWWWWWW',
'WWWW   W     WWWWW   W   WWWWWWWWW             W',
'W            W       W       W                 W',
'W            W       W       W                 W',
'W            W       W       W                 W',
'W   WWWWWWWWWW   W   W       W   WWWWWWWWWWW   W',
'W   W            W   WWWWWWWWW             W   W',
'W   W            W       W   W             W   W',
'W   W            W       W   W             W   W',
'W   WWWWWWWWWW   W       W   WWWWWWW   W   W   W',
'W   W   W   W    WWWWWWWWW   W     W   W       W',
'W   W   W   W    W   W       W     W   W       W',
'W   W   W   W    W   W       W     W   W       W',
'W   W   W   W    W   W       W     W   W       W',
'W   W   W   W    W   W   WWWWWWW   W   WWWWWWWWW',
'W   W   W   W    W   W   W                     W',
'W                        W                     W',
'W                        W                     W',
'W                        W                     W',
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW F W'

]
 

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "F":
            end_rect = pygame.Rect(x, y, 25, 25)
        x += 25
    y += 25
    x = 0
 
background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
running = True
while running:
    screen.blit(background_image, [0,0])    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
 

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)
 
    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    enemies.update()

    for wall in walls:
        pygame.draw.rect(screen, (BLACK), wall.rect)
    pygame.draw.rect(screen, (200, 180, 50), end_rect)
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)
    screen.blit(player.surf, player.rect)
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.quit()
        sys.exit()
    pygame.display.flip()
    clock.tick(360)
 
pygame.quit()