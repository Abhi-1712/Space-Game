import time
import os
import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Game", )
game_icon = pygame.image.load(os.path.join("images", "001-project.png"))
pygame.display.set_icon(game_icon)
background = pygame.image.load(os.path.join("images", "space_background.png"))
mixer.music.load(os.path.join("audio", "background_music.wav"))
mixer.music.play(-1)

fighterImg = pygame.image.load(os.path.join("images", "001-spaceship.png"))
fighterX = 420
fighterY = 480
fighterX_change = 0

alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alien_count = 4
for i in range(alien_count):
    alienImg.append(pygame.image.load(os.path.join("images", "ufo.png")))
    alienX.append(random.randint(2, 735))
    alienY.append(random.randint(55, 200))
    alienX_change.append(0.25)
    alienY_change.append(25)

missileImg = pygame.image.load(os.path.join("images", "missile.png"))
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 1.75
missile_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

game_over = pygame.font.Font('freesansbold.ttf', 64)


def game_over_message():
    game_over_text = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fighter(x, y):
    screen.blit(fighterImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def alien_missile(x, y, i):
    screen.blit(missileImg, (x + 16, y + 10))


def check_collision(alienX, alienY, missileX, missileY):
    distance = math.sqrt((math.pow(alienX - missileX, 2)) + (math.pow(alienY - missileY, 2)))
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
                    missile_sound = mixer.Sound(os.path.join("audio", "Missile_fire.wav"))
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
        if random.randrange(0, 120) == 1:
            alien_missileY = alienY[i]
            alien_missileX = alienX[i]
            alien_missile(alien_missileX,alien_missileY,i)
            alien_missileY += 0.05
        if alienY[i] > 440:
            for j in range(alien_count):
                alienY[j] = 2000
                game_over_message()
            break
        alienX[i] += alienX_change[i]
        if alienX[i] <= 2:
            alienX_change[i] = 0.25
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.25
            alienY[i] += alienY_change[i]
        collision = check_collision(alienX[i], alienY[i], missileX, missileY)
        if collision:
            missileY = 480
            collision_sound = mixer.Sound(os.path.join("audio", "explosion.wav"))
            collision_sound.play()
            missile_state = "ready"
            score_value += 1
            alienX[i] = random.randint(2, 735)
            alienY[i] = random.randint(55, 200)
        alien(alienX[i], alienY[i], i)

    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change
    fighter(fighterX, fighterY)
    show_score(textX, textY)
    pygame.display.update()
