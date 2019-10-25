import pygame
from pygame.locals import *
import os
import sys
import math

RED = [255, 0, 0]
BLUE = [0, 255, 0]
GREEN = [0, 0, 255]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

y_boundary = 0

W, H = 800, 400
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

velocity = list([-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5])

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, py):
        super().__init__()

        # Starting position
        self.x = x
        self.y = y

        # Is it jumping?
        self.jumping = False

        # Setting boundaries
        self.platform_y = py

        # Settings speeds
        self.x_speed = 12
        self.velocity_index = 0

    def do_jump(self):
        global velocity
        velocity = list([-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5])

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

    def do_draw(self):
        pygame.draw.rect(win, RED, [int(self.x), int(self.y), 20, 60])

    def do_player(self):
        self.do_jump()
        self.do_move()
        self.do_draw()
        pygame.display.update()


class Enemy:
    walkRight = pygame.image.load('place_holder.png')
    walkLeft = pygame.image.load('place_holder.png')

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.end = end
        self.path = [self.x, self.end]

        self.vel = 3

    def move(self):
        # Makes all enemies move at speed of background
        self.x -= 1.4

        if self.vel > 0:
            # If not at end keep going right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                # if at end go left by velocity
                self.vel = self.vel * -1
        # if velocity is negative
        else:
            # If more than starting position go right
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                # If not go keep going left
                self.vel = self.vel * -1

    def draw(self):
        self.move()
        pygame.draw.rect(win, RED, [int(self.x), int(self.y), self.width, self.height])



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

def keys(self):
    key = pygame.key.get_pressed()
    if key[K_SPACE] and player.jumping == False:
        player.jumping = True

# Setting speed
speed = 30
clock = pygame.time.Clock()

pygame.init()

# Object instantiation
player = Player(100, 100, 200)
background = Background()

enemy_list = []

enemy_attr = [[500, 310, 20, 60, 345],
             [540, 350, 20, 60, 385],
             [580, 390, 20, 60, 425],
             [620, 430, 20, 60, 480]]

for i in range(5):
    enemy = Enemy(enemy_attr[i])
    enemy_list.append(enemy)

run = True

while run:

    clock.tick(speed)

    win.fill(WHITE)

    background.do_background()

    keys(player)

    enemy.draw()

    player.do_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()





