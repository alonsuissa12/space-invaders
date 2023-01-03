import random
import math
from pygame import mixer
import pygame

# initialize pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.jpg')
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load('001-ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship.png.png')
playerX = 370
plyerY = 480
player_x_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6
for _ in range(num_of_enemies):
    enemyImg.append(pygame.image.load('001-enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(50)
    enemy_x_change.append(0.35)
    enemy_y_change.append(40)

# bullet

# 'ready' - the bullet is unseen.
# 'fire' - the bullet is being shot
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_y_change = 1
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10


# game over
game_over_font = pygame.font.Font('freesansbold.ttf', 80)
def game_over_text():
    game_over_text = game_over_font.render("GAME OVER" , True, (250,0, 80))
    screen.blit(game_over_text, (160, 250))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# collision
def is_collision(xBullet, yBullet, xEnemy, yEnemy):
    distance = math.sqrt((math.pow((xEnemy - xBullet), 2) + math.pow((yEnemy - yBullet), 2)))
    if distance < 28:
        return True
    return False


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))




# game loop
running = True
while running:
    # RGB - red, green, blue
    # screen.fill((0, 0, 0))
    # background img
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check idf it is right of left
        if event.type == pygame.KEYDOWN:
            print("a keystroke is pressed")
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                print("Right arrow was pressed")
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                print("space was pressed")
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                print("keystroke has been released")
                player_x_change = 0

    playerX = (playerX + player_x_change) % 800

    # enemy movement(in boundaries) and game-over
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        if enemyX[i] <= 0 or enemyX[i] > 735:
            enemy_x_change[i] *= -1
            enemyY[i] += enemy_y_change[i]
        enemyX[i] += enemy_x_change[i]

    # bullet movment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_y_change

    # collision
    for i in range(num_of_enemies):
        collision = is_collision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print("score is:", score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = 50
            bullet_sound = mixer.Sound('explosion.wav')
            bullet_sound.play()

    player(playerX, plyerY)
    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)
        show_score(score_x, score_y)
    pygame.display.update()
