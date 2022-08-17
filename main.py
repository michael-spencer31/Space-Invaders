import math
import random
import pygame
from pygame import mixer
from sys import exit 
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

# load in and then scale background image
background_img = pygame.image.load("space.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (800, 600))

title_img = pygame.image.load("player.png").convert_alpha()
title_img = pygame.transform.scale(title_img, (800, 600))

# load in and play background music
mixer.music.load("background.mp3")
mixer.music.play(-1)

# set title
pygame.display.set_caption("Invaders, Featuring Space!")

# load in the player image and size
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

score_value = 0 
level_value = 1
level_holder = 1

# declare variables for enemies 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

# these represent "faster" speedy enemies
senemyImg = []
senemyX = []
senemyY = []
senemyX_change = []
senemyY_change = []
num_of_senemies = 2

# create and start a clock 
clock = pygame.time.Clock()
start_ticks=pygame.time.get_ticks() #starter tick
enemy_ticks = pygame.time.get_ticks()

# add pictures and x,y for both types of enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ufo_normal.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

for i in range(num_of_senemies):
    senemyImg.append(pygame.image.load("ufo_speed.png"))
    senemyX.append(random.randint(0, 736))
    senemyY.append(random.randint(50, 150))
    senemyX_change.append(6)
    senemyY_change.append(40)

# load in and create bullet objects
bulletImg = pygame.image.load("laser.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# create and load in fonts for later use
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
welcome_font = pygame.font.Font("freesansbold.ttf", 46)
instruction_font = pygame.font.Font('freesansbold.ttf', 18)

testX = 10 
testY = 10 

# this text will be displayed when the game is over :(
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# create and display welcome message
def welcome_text():
    welcome_text = welcome_font.render("Welcome to Space Invaders!", True, (255, 255, 255))
    start_text = font.render("Press space to start!", True, (255, 255, 255))
    instruction_text = font.render("Move using 'A' and 'D', shoot with Space", True, (255, 255, 255))
    screen.blit(welcome_text, (50, 250))
    screen.blit(instruction_text, (75, 300))
    screen.blit(start_text, (200, 350))

# show the player score in the top left corner 
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

counter = 0

def show_level(x, y):

    global counter
    global level_value
    global start_ticks

    level = font.render("Level: " + str(level_value), True, (255, 255, 255))
    screen.blit(level, (x, y))

    if pygame.time.get_ticks() > start_ticks:

        # after enough time has passed increase player level by 1
        start_ticks += 30000
        level_value += 1
    
        level = font.render("Level: " + str(level_value), True, (255, 255, 255))
        screen.blit(level, (x, y))

# load the player, enemies and bullets onto the screen with screen.blit
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def speed_enemy(x, y, i):
    screen.blit(senemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# check if collision happens 
def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True 
    else:
        return False

title = True 

# title screen loop 
while title:

    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            title = False
            pygame.quit()

        # close the title screen once the player hit the 'space' key
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                title = False
                break

    welcome_text()

    pygame.display.update()

running = True

# start main game loop
while running:

    # add background colour and image
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))

    # get and record each event 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # check if a key is pressed
        if event.type == pygame.KEYDOWN:

            # if 'a' key is hit move player right
            if event.key == pygame.K_a:

                playerX_change = -2
            # if 'd' key is hit move player left
            if event.key == pygame.K_d:

                playerX_change = 2
                
            # is 'space' key is hit, fire a bullet
            if event.key == pygame.K_SPACE:

                if bullet_state == "ready":

                    bulletSound = mixer.Sound("shooting.wav")
                    bulletSound.play()
                    bulletX = playerX 
                    fire_bullet(bulletX, bulletY)

    playerX += playerX_change

    # keep the player in bounds on the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # if an enemy makes it to the bottom of the screen, the game is over
    for i in range(num_of_enemies):

        if enemyY[i] > 440:

            for j in range(num_of_enemies):

                enemyY[j] = 2000
            game_over_text()
            break
            
        # keep moving the enemies down the screen
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        
        # check if a bullet collides with an enemy; if so, delete them
        if collision:

            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # repeat the above code for speed enemies
    if pygame.time.get_ticks() > 15000:

        for i in range(num_of_senemies):

            if senemyY[i] > 440:

                for j in range(num_of_senemies):

                    senemyY[j] = 2000
                game_over_text()
                break

            senemyX[i] += senemyX_change[i]
            if senemyX[i] <= 0:
                senemyX_change[i] = 4
                senemyY[i] += senemyY_change[i]
            elif senemyX[i] >= 736:
                senemyX_change[i] = -4
                senemyY[i] += senemyY_change[i]

            collision = isCollision(senemyX[i], senemyY[i], bulletX, bulletY)

            if collision:

                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 2
                senemyX[i] = random.randint(0, 736)
                senemyY[i] = random.randint(50, 150)

            speed_enemy(senemyX[i], senemyY[i], i)
    # check if bullets are ready to be fired
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":

        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(testX, testY)
    show_level(10, 45)
    pygame.display.update()

pygame.quit()

