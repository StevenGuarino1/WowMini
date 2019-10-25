import pygame
import time
from pygame.locals import *

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

sprite_width = 20
sprite_height = 60

y_boundary = 0

ground_y = 293

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Wow Mini')

jump_speed = list([-9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5, -5,
                   -4.5, -4, -2.5, -1.5, -1, -0.5, 0, 0.5, 1, 1.5,
                   2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5])


class Player(pygame.sprite.Sprite):
    """
    Creates a player instance


    """
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([sprite_width, sprite_height])
        self.image.fill(RED)

        # Gets rect object for collision detection
        self.rect = self.image.get_rect()

        # Starting position
        self.x = x
        self.y = y

        # Is it jumping?
        self.jumping = False

        # Setting boundaries for jumping
        self.platform_y = ground_y

        # Settings speeds
        self.x_speed = 4
        self.speed_index = 0

        all_sprites_list.add(self)

    def do_jump(self):
        if self.jumping:
            # Changing y pos at velocity index speed
            self.y += jump_speed[self.speed_index]
            self.speed_index += 1

            if self.speed_index >= len(jump_speed) - 1:
                self.speed_index = len(jump_speed) - 1

            # Stops movement once boundary hit
            if self.y > self.platform_y:
                self.y = self.platform_y
                self.jumping = False
                # Resets speed index for next jump
                self.speed_index = 0

    def do_move(self):
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            self.x += self.x_speed
        if key[K_LEFT]:
            self.x -= self.x_speed

    def playerUpdate(self):
        player.rect.x = self.x
        player.rect.y = self.y

    def do_player(self):
        self.do_jump()
        self.do_move()
        self.playerUpdate()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([sprite_width, sprite_height])
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
        all_sprites_list.update()

    def do_enemy(self):
        self.move()
        self.enemyUpdate()

class MagicSpell(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()

        self.image = pygame.Surface([20, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.rect.x = start_x
        self.rect.y = start_y

        active_spells.add(self)
        all_sprites_list.add(self)

    def update(self):
        self.rect.x += 2
        print(self.rect.x)

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
        screen.blit(self.bg, (self.bgX, 0))  # draws our first bg image
        screen.blit(self.bg, (self.bgX2, 0))  # draws the second bg image
        pygame.display.update()

    def do_background(self):
        self.do_scroll()
        self.drawBackground()
        pygame.display.update()

def keys(self):
    key = pygame.key.get_pressed()
    if key[K_SPACE] and player.jumping is False:
        player.jumping = True
    if key[K_1] and len(active_spells) < 1:
        MagicSpell(player.rect.centerx, player.rect.centery)


def collisions():
    global run
    global gameOver
    gameOver = pygame.sprite.spritecollide(player, enemy_list, True)
    pygame.sprite.groupcollide(active_spells, enemy_list, True, True)

def draw_text(outcome):
    font = pygame.font.Font('freesansbold.ttf', 32)

    if outcome == "LOSE":
        text = font.render('Quest Failed', True, WHITE, BLACK)
    if outcome == "WIN":
        text = font.render('Quest Completed', True, WHITE, BLACK)

    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)

    screen.blit(text, text_rect)


# Setting speed
speed = 60
clock = pygame.time.Clock()

pygame.init()

# Declaring lists and sprite groups
gameOver = []

all_sprites_list = pygame.sprite.Group()
active_spells = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()

# Object instantiation
player = Player(100, ground_y)
background = Background()

# Attributes to be passed to each enemy
enemy_attr = [[250, ground_y],
             [450, ground_y],
             [850, ground_y],
             [950, ground_y]]

# Generates enemy instances
for enemyconfig in enemy_attr:
    enemy = Enemy(*enemyconfig)
    enemy_list.add(enemy)

run = True

while run:

    clock.tick(speed)

    background.do_background()

    keys(player)

    for enemy in enemy_list:
        enemy.do_enemy()

    player.do_player()

    collisions()

    all_sprites_list.update()

    all_sprites_list.draw(screen)

    pygame.display.update()

    if len(gameOver) > 0:
        draw_text("LOSE")
        pygame.display.update()
        time.sleep(2)
        run = False

    if len(enemy_list) == 0:
        draw_text("WIN")
        pygame.display.update()
        time.sleep(2)
        run = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            #run = False
            # pygame.quit()
            # quit()





