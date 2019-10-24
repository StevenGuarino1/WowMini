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

        # Is jumping?
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
        global win, WHITE
        pygame.draw.rect(win, RED, [100, 100, int(self.x), int(self.y)])

    def do_player(self):
        self.do_jump()
        self.do_move()
        self.do_draw()
        pygame.display.update()


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

    def do_bg(self):
        self.do_scroll()
        self.drawBackground()

def keys(self):
    key = pygame.key.get_pressed()
    if key[K_SPACE] and player.jumping == False:
        player.jumping = True







# class Level(object):
#     """ This is a generic super-class used to define a level.
#         Create a child class for each level with level-specific
#         info. """
#
#     def __init__(self, player):
#         """ Constructor. Pass in a handle to player. Needed for when moving
#             platforms collide with the player. """
#         self.platform_list = pygame.sprite.Group()
#         self.enemy_list = pygame.sprite.Group()
#         self.player = player
#
#         # Background image
#         self.background = None
#
#         # How far this world has been scrolled left/right
#         self.world_shift = 0
#         self.level_limit = -1000
#
#     # Update everythign on this level
#     def update(self):
#         """ Update everything in this level after logic on sprites is completed."""
#         self.platform_list.update()
#         self.enemy_list.update()
#
#     def draw(self, screen):
#         """ Draw everything on this level. """
#
#         # Draw the background
#         screen.fill(BLUE)
#
#         # Draw all the sprite lists that we have
#         self.platform_list.draw(screen)
#         self.enemy_list.draw(screen)
#
#     def shift_world(self, shift_x):
#         """ When the user moves left/right and we need to scroll everything:
#         """
#
#         # Keep track of the shift amount
#         self.world_shift += shift_x
#
#         # Go through all the sprite lists and shift
#         for platform in self.platform_list:
#             platform.rect.x += shift_x
#
#         for enemy in self.enemy_list:
#             enemy.rect.x += shift_x
#
# # Create platforms for the level
# class Level_01(Level):
#     """ Definition for level 1. """
#
#     def __init__(self, player):
#         """ Create level 1. """
#
#         # Call the parent constructor
#         Level.__init__(self, player)
#
#         self.level_limit = -1500
#
#         # Array with width, height, x, and y of platform
#         level = [[210, 70, 500, 500],
#                  [210, 70, 800, 400],
#                  [210, 70, 1000, 500],
#                  [210, 70, 1120, 280],
#                  ]
#
#         # Go through the array above and add platforms
#         for platform in level:
#             block = Platform(platform[0], platform[1])
#             block.rect.x = platform[2]
#             block.rect.y = platform[3]
#             block.player = self.player
#             self.platform_list.add(block)
#
#         # Add a custom moving platform
#         block = HorizontalMovingPlatform()
#         block.rect.x = 550
#         block.rect.y = 425
#         block.boundary_left = 500
#         block.boundary_right = 730
#         # block.change_x = 1
#         block.player = self.player
#         block.level = self
#         self.platform_list.add(block)
#
#
# # Create platforms for the level
# class Level_02(Level):
#     """ Definition for level 2. """
#
#     def __init__(self, player):
#         """ Create level 1. """
#
#         # Call the parent constructor
#         Level.__init__(self, player)
#
#         self.level_limit = -1000
#
#         # Array with type of platform, and x, y location of the platform.
#         level = [[210, 70, 500, 550],
#                  [210, 70, 800, 400],
#                  [210, 70, 1000, 500],
#                  [210, 70, 1120, 280],
#                  ]
#
#         # Go through the array above and add platforms
#         for platform in level:
#             block = Platform(platform[0], platform[1])
#             block.rect.x = platform[2]
#             block.rect.y = platform[3]
#             block.player = self.player
#             self.platform_list.add(block)
#
#         # Add a custom moving platform
#         block = MovingPlatform(70, 70)
#         block.rect.x = 550
#         block.rect.y = 425
#         block.boundary_top = 100
#         block.boundary_bottom = 550
#         block.change_y = -1
#         block.player = self.player
#         block.level = self
#         self.platform_list.add(block)




speed = 30
clock = pygame.time.Clock()

pygame.init()

player = Player(100, 100, 400)
background = Background()

run = True

while run:

    clock.tick(speed)

    win.fill(WHITE)

    background.do_bg()

    keys(player)

    player.do_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()





