import pygame
from pygame.locals import *
import os
import sys
import math

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

sprite_w = 20
sprite_h = 60

y_boundary = 0

ground_y = 293

W, H = 800, 400
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

velocity = list([-9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -2.5, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5])

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([sprite_w, sprite_h])
        self.image.fill(RED)
        # Gets rect object for collision detection
        self.rect = self.image.get_rect()

        # Starting position
        self.x = x
        self.y = y

        # Is it jumping?
        self.jumping = False

        # Setting boundaries
        self.platform_y = ground_y

        # Settings speeds
        self.x_speed = 12
        self.velocity_index = 0

        # Did player cast spell?
        self.castingSpell = False

        all_sprites_list.add(self)

    def do_jump(self):
        if self.jumping:
            # Changing y pos at velocity index speed
            self.y += velocity[self.velocity_index]
            self.velocity_index += 1
            # Minus one bc len() returns 20, velocity list ends at index 19
            # If speed index is > len(list), max speed reached, return index 19
            if self.velocity_index >= len(velocity) - 1:
                self.velocity_index = len(velocity) - 1
            # Stops movement by settings y pos to platform y pos
            if self.y > self.platform_y:
                self.y = self.platform_y
                self.jumping = False
                self.velocity_index = 0

    def do_move(self):
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            self.x += self.x_speed
        if key[K_LEFT]:
            self.x -= self.x_speed

    def playerUpdate(self):
        if self.castingSpell:
            Bullet()

        player.rect.x = self.x
        player.rect.y = self.y
        all_sprites_list.update(player)

    def do_player(self):
        self.do_jump()
        self.do_move()
        self.playerUpdate()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([sprite_w, sprite_h])
        self.image.fill(BLUE)
        # Gets rect object for collision detection
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.vel = 1

        all_sprites_list.add(self)

    def move(self):
        if self.rect.x > player.x:
            self.x -= self.vel
        else:
            self.x += self.vel

    def enemyUpdate(self):
        enemy.rect.x = self.x
        enemy.rect.y = self.y
        all_sprites_list.update(enemy)

    def do_enemy(self):
        self.move()
        self.enemyUpdate()

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([5, 5])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.rect.x = player.rect.center[0]
        self.rect.y = player.rect.center[1]

        self.rect.y -= 3
        all_sprites_list.add(self)


class Background:
    def __init__(self):
        self.bg = pygame.image.load('swamp.png').convert()
        self.bgX = 0
        self.bgX2 = self.bg.get_width()

    def do_scroll(self):
        # THIS WAS THE PROBLEM, movement declaration must be defined each frame, not in init where its run once
        self.bgX -= 1.4  # Move both background images back
        self.bgX2 -= 1.4
        if self.bgX < self.bg.get_width() * -1:  # If our bg is at the -width then reset its position
            self.bgX = self.bg.get_width()
        if self.bgX2 < self.bg.get_width() * -1:
            self.bgX2 = self.bg.get_width()

    def drawBackground(self):
        win.blit(self.bg, (self.bgX, 0))  # draws our first bg image
        win.blit(self.bg, (self.bgX2, 0))  # draws the second bg image
        pygame.display.update()

    def do_background(self):
        self.do_scroll()
        self.drawBackground()
        pygame.display.update()

def keys(self):
    key = pygame.key.get_pressed()
    if key[K_SPACE] and player.jumping == False:
        player.jumping = True
    if key[K_1]:
        player.castingSpell = True

def collisions():
    pygame.sprite.spritecollide(player, enemy_list, True)

# Setting speed
speed = 30
clock = pygame.time.Clock()

pygame.init()


all_sprites_list = pygame.sprite.Group()
# Object instantiation
player = Player(100, ground_y)
background = Background()

enemy_list = pygame.sprite.Group()

enemy_attr = [[250, ground_y],
             [450, ground_y],
             [850, ground_y],
             [1100, ground_y]]

for enemyconfig in enemy_attr:
    enemy = Enemy(*enemyconfig)
    enemy_list.add(enemy)

def gameOver():
    dead_list = pygame.sprite.spritecollide(player, enemy_list, True)
    if len(dead_list) > 0:
        print("YA LOST")


run = True

while run:

    clock.tick(speed)

    background.do_background()

    keys(player)

    for enemy in enemy_list:
        enemy.do_enemy()

    player.do_player()

    all_sprites_list.draw(win)

    gameOver()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()





