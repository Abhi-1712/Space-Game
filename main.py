import pygame
from pygame import mixer
import math
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Game", )

game_icon = pygame.image.load('001-project.png')
pygame.display.set_icon(game_icon)

background = pygame.image.load('space_background.png')

mixer.music.load('alien-spaceship_daniel_simion.wav')
mixer.music.play(-1)

fighterImg = pygame.image.load('001-spaceship.png')
fighterX = 420
fighterY = 480
fighterX_change = 0

shipImg = []
shipX = []
shipY = []
shipY_change = []
ship_count = 4

for i in range(ship_count):
    shipImg.append(pygame.image.load('ship.png'))
    shipX.append(random.randint(2, 735))
    shipY.append(random.randint(-200, -20))
    shipY_change.append(0.25)

alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alien_count = 4
alien_missile_X = []
alien_missile_Y = []
for i in range(alien_count):
    alienImg.append(pygame.image.load('ufo.png'))
    alienX.append(random.randint(2, 735))
    alien_missile_X.append(alienX)
    alienY.append(random.randint(55, 200))
    alien_missile_Y.append(alienY)
    alienX_change.append(0.50)
    alienY_change.append(25)

missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 1.75
missile_state = "ready"

alien_missile_Img = pygame.image.load('alien_Missile.png')

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

lives_value = 5
livesFont = pygame.font.Font('freesansbold.ttf', 32)
livesX = 650
livesY = 10

game_over = pygame.font.Font('freesansbold.ttf', 64)


def game_over_message():
    game_over_text = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def show_lives(x, y):
    lives = font.render("LIVES: " + str(lives_value), True, (255, 0, 0))
    screen.blit(lives, (x, y))


def fighter(x, y):
    screen.blit(fighterImg, (x, y))


def ship(x, y, i):
    screen.blit(shipImg[i], (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def check_collision(alienX, alienY, missileX, missileY):
    distance = math.sqrt((math.pow(alienX - missileX, 2)) + (math.pow(alienY - missileY, 2)))
    if distance < 30:
        return True
    return False


def check_collision2(shipX, shipY, missileX, missileY):
    distance = math.sqrt((math.pow(shipX - missileX, 2)) + (math.pow(shipY - missileY, 2)))
    if distance < 30:
        return True
    return False


Window_run_status = True
while Window_run_status:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Window_run_status = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                fighterX_change = 0.75
            if event.key == pygame.K_LEFT:
                fighterX_change = -0.75
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missile_sound = mixer.Sound('Gun_Shot-Marvin-1140816320.wav')
                    missile_sound.play()
                    missileX = fighterX
                    fire_missile(missileX, missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                fighterX_change = 0

    fighterX += fighterX_change
    if fighterX <= 2:
        fighterX = 2
    elif fighterX >= 730:
        fighterX = 730

    for i in range(alien_count):
        if alienY[i] > 440:
            for j in range(alien_count):
                alienY[j] = 2000
                shipY[j] = 2000
                game_over_message()
            break
        alienX[i] += alienX_change[i]
        if alienX[i] <= 2:
            alienX_change[i] = 0.5
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.5
            alienY[i] += alienY_change[i]
        collision = check_collision(alienX[i], alienY[i], missileX, missileY)
        if collision:
            missileY = 480
            collision_sound = mixer.Sound('Blast-SoundBible.com-2068539061.wav')
            collision_sound.play()
            missile_state = "ready"
            score_value += 1
            alienX[i] = random.randint(2, 735)
            alienY[i] = random.randint(55, 200)
        alien(alienX[i], alienY[i], i)
        if shipY[i] >= 600:
            shipY[i] = random.randint(-200, -20)
            lives_value -= 1
        collision2 = check_collision2(shipX[i], shipY[i], missileX, missileY)
        if collision2:
            missileY = 480
            collision_sound = mixer.Sound('Blast-SoundBible.com-2068539061.wav')
            collision_sound.play()
            missile_state = "ready"
            score_value += 1
            shipX[i] = random.randint(2, 735)
            shipY[i] = random.randint(-200, -20)
        shipY[i] += shipY_change[i]
        ship(shipX[i], shipY[i], i)

    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change
    if lives_value == 0:
        for j in range(alien_count):
            alienY[j] = 2000
            shipY[j] = 2000
            game_over_message()

    fighter(fighterX, fighterY)
    show_score(textX, textY)
    show_lives(livesX, livesY)
    pygame.display.update()
