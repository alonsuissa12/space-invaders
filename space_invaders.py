import random
import math
import sys
import pygame
from pygame import mixer

speed = 10
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
num_of_enemies = 12
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('001-enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(50)
    enemy_x_change.append((0.5 + i * 0.01) * speed)
    enemy_y_change.append(40)
num_of_enemies = 1

# bullet

# 'ready' - the bullet is unseen.
# 'fire' - the bullet is being shot
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_y_change = 1 * speed
bullet_state = "ready"

# speed boost
speed_boost_img = pygame.image.load('boost.png')
speed_boost_x = 2000
speed_boost_y = 2000
speed_boost_change_y = 0.3 * speed
is_speed_boost_on = False
speed_boost_timer = 5000 / speed
boost_speed = 0
catch_speed_boost = False


def show_speed_boost(x, y):
    screen.blit(speed_boost_img, (x, y))


def stop_speed_boost():
    global speed_boost_timer
    global is_speed_boost_on
    global boost_speed
    screen.blit(speed_boost_img, (2000, 2000))
    is_speed_boost_on = False
    boost_speed = 0
    speed_boost_timer = 5000 / speed


# bullets boost
bullets_boost_img = pygame.image.load('bullets boost.png')
bullets_boost_x = 2000
bullets_boost_y = 2000
bullets_boost_change_y = 0.3 * speed
is_bullets_boost_on = False
bullets_boost_timer = 5000 / speed
catch_bullets_boost = False

# bullets of bullets boost
bulletsImg = []
bulletsX = [0, 0, 0]
bulletsY = [480, 480, 480]
bullets_y_change = [1 * speed, 1 * speed, 1 * speed]
bullets_state = []

for i in range(3):
    bulletsImg.append(pygame.image.load('bullet.png'))
    bullets_state.append("ready")


def stop_bullets_boost():
    global bullets_boost_timer
    global is_bullets_boost_on
    global catch_speed_boost
    screen.blit(speed_boost_img, (2000, 2000))
    is_bullets_boost_on = False
    catch_bullets_boost = False
    bullets_boost_timer = 5000 / speed


def show_bullets_boost(x, y):
    screen.blit(bullets_boost_img, (x, y))


def is_collect_boost(player_x, player_y, boost_x, boost_y):
    distance = math.sqrt((math.pow((player_x - boost_x), 2) + math.pow((player_y - boost_y), 2)))
    if distance < 30 and (player_y - boost_y) > 5:
        return True
    if (0 > player_x - boost_x > - 50) and (player_y - boost_y) > 5:
        if distance < 70:
            return True
    return False


def its_boost_time():
    if random.randint(1, 12) == 1:
        return True
    return False


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10

# game over
game_over_font = pygame.font.Font('freesansbold.ttf', 80)
big_font = pygame.font.Font('freesansbold.ttf', 80)
med_font = pygame.font.Font('freesansbold.ttf', 50)
small_font = pygame.font.Font('freesansbold.ttf', 20)


def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (250, 0, 80))
    screen.blit(game_over_text, (160, 250))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# collision
def is_collision(xBullet, yBullet, xEnemy, yEnemy):
    distance = math.sqrt((math.pow((xEnemy - xBullet), 2) + math.pow((yEnemy - yBullet), 2)))
    if distance < 28:
        return True
    if 0 > xEnemy - xBullet > - 30:
        if distance < 50:
            return True
    return False


def fire_bullet(x, y, bullet):
    global bullet_state, bullets_state
    if bullet == 4:
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))
    else:
        bullets_state[bullet] = "fire"
        screen.blit(bulletsImg[bullet], (bulletsX[bullet], bulletsY[bullet]))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def intro():
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False

        welcome_text1 = big_font.render("welcome", True, (250, 0, 80))
        welcome_text2 = med_font.render("to space invaders!", True, (250, 0, 80))
        rules = small_font.render("-the goal is to kill the enemies before they get to you", True, (250, 0, 80))
        keys1 = small_font.render("-use left/right arrows for moving", True, (250, 0, 80))
        keys2 = small_font.render("-use space for shooting", True, (250, 0, 80))
        keys3 = small_font.render("-use P to stop ", True, (250, 0, 80))
        keys4 = small_font.render("PRESS SPACE TO START ", True, (255, 255, 153))

        screen.blit(background, (0, 0))

        screen.blit(welcome_text1, (220, 50))
        screen.blit(welcome_text2, (180, 150))
        screen.blit(rules, (160, 250))
        screen.blit(keys1, (160, 280))
        screen.blit(keys2, (160, 310))
        screen.blit(keys3, (160, 340))
        screen.blit(keys4, (270, 400))

        player(playerX, plyerY)

        pygame.display.update()
        clock.tick(5)


def game_over(p_x, p_y):
    small_font = pygame.font.Font('freesansbold.ttf', 20)
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    break
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        text1 = small_font.render("press SPACE to play again and Q to quit", True, (250, 0, 80))

        screen.blit(background, (0, 0))
        screen.blit(text1, (200, 400))

        game_over_text()

        player(playerX, plyerY)
        pygame.display.update()
        clock.tick(5)

    game_loop()

def pose(px, py, ex, ey, NOE):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.blit(background, (0, 0))

        text1 = small_font.render("press SPACE to continue and Q to quit", True, (250, 0, 80))
        for t in range(NOE):
            enemy(ex[t], ey[t], t)
            show_score(score_x, score_y)

        screen.blit(text1, (200, 400))

        player(px, py)
        pygame.display.update()



# game loop
def game_loop():
    global speed, catch_bullets_boost, boost_speed, playerX, bullet_state, bulletY, player_x_change, num_of_enemies, bulletX, is_speed_boost_on, is_bullets_boost_on, score_value, speed_boost_x, bullets_boost_y, bullets_boost_x, speed_boost_y, catch_speed_boost, speed_boost_timer, bullets_boost_timer
    playerX = 370
    plyerY = 480
    player_x_change = 0

    # enemy
    enemyImg = []
    enemyX = []
    enemyY = []

    num_of_enemies = 12
    for i in range(num_of_enemies):
        enemyX.append(random.randint(0, 735))
        enemyY.append(50)
    num_of_enemies = 1

    # bullet

    # 'ready' - the bullet is unseen.
    # 'fire' - the bullet is being shot
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"

    # speed boost
    speed_boost_x = 2000
    speed_boost_y = 2000
    speed_boost_change_y = 0.3 * speed
    is_speed_boost_on = False
    speed_boost_timer = 5000 / speed
    boost_speed = 0
    catch_speed_boost = False

    # bullets boost
    bullets_boost_x = 2000
    bullets_boost_y = 2000

    bullets_boost_change_y = 0.3 * speed
    is_bullets_boost_on = False
    bullets_boost_timer = 5000 / speed
    catch_bullets_boost = False

    # bullets of bullets boost
    bulletsImg = []
    bulletsX = [0, 0, 0]
    bulletsY = [480, 480, 480]
    bullets_y_change = [1 * speed, 1 * speed, 1 * speed]
    bullets_state = []

    clock = pygame.time.Clock()
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
                if event.key == pygame.K_p:
                    pose(playerX, plyerY, enemyX, enemyY, num_of_enemies)

                if event.key == pygame.K_LEFT:
                    player_x_change = (-0.6) * speed - boost_speed

                if event.key == pygame.K_RIGHT:
                    player_x_change = 0.6 * speed + boost_speed

                if event.key == pygame.K_SPACE:
                    if catch_bullets_boost:
                        bullet_to_shoot = -1
                        for index in range(3):
                            if bullets_state[index] == "ready":
                                bullet_to_shoot = index
                        if bullet_to_shoot != -1:
                            bulletsX[bullet_to_shoot] = playerX
                            fire_bullet(bulletsX[bullet_to_shoot], bulletsY[bullet_to_shoot], bullet_to_shoot)
                            bullet_sound = mixer.Sound('laser.wav')
                            bullet_sound.play()
                    else:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY, 4)
                            bullet_sound = mixer.Sound('laser.wav')
                            bullet_sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player_x_change = 0

        playerX = (playerX + player_x_change) % 800

        # enemy movement(in boundaries) and game-over
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over(playerX, plyerY)
            if enemyX[i] <= 0 or enemyX[i] > 735:
                enemy_x_change[i] *= -1
                enemyY[i] += enemy_y_change[i]
            enemyX[i] += enemy_x_change[i]

        # bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY, 4)
            bulletY -= bullet_y_change

        if catch_bullets_boost:
            for j, by in enumerate(bulletsY):
                if by <= 0:
                    bulletsY[j] = 480
                    bullets_state[j] = "ready"
            for j in range(3):
                if bullets_state[j] == "fire":
                    fire_bullet(bulletsX[j], bulletsY[j], j)
                    bulletsY[j] -= bullet_y_change

        # collision
        for k in range(num_of_enemies):
            collision_happened = False
            if not catch_bullets_boost:
                collision = is_collision(bulletX, bulletY, enemyX[k], enemyY[k])
                if collision:
                    collision_happened = True
                    bulletY = 480
                    bullet_state = "ready"
            else:
                for j in range(3):
                    collision = is_collision(bulletsX[j], bulletsY[j], enemyX[k], enemyY[k])
                    if collision:
                        collision_happened = True
                        bulletsY[j] = 480
                        bullets_state[j] = "ready"
            if collision_happened:
                if its_boost_time() and (not is_speed_boost_on):
                    is_speed_boost_on = True
                    speed_boost_x = enemyX[k]
                    speed_boost_y = enemyY[k]
                if its_boost_time() and (not is_bullets_boost_on):
                    is_bullets_boost_on = True
                    bullets_boost_x = enemyX[k]
                    bullets_boost_y = enemyY[k]
                score_value += 1
                enemyX[k] = random.randint(0, 735)
                enemyY[k] = 50
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()

        if score_value >= num_of_enemies * 4 and num_of_enemies < 12:
            num_of_enemies += 1

        # taking boost
        if is_collect_boost(playerX, plyerY, speed_boost_x, speed_boost_y):
            boost_speed = 0.3 * speed
            catch_speed_boost = True
        if is_collect_boost(playerX, plyerY, bullets_boost_x, bullets_boost_y):
            catch_bullets_boost = True

        # boost
        if is_speed_boost_on:
            speed_boost_y += speed_boost_change_y  # * speed
            if not catch_speed_boost:
                show_speed_boost(speed_boost_x + 3, speed_boost_y - 5)
            if not catch_speed_boost and speed_boost_y > 600:
                stop_speed_boost()
                catch_speed_boost = False
            if speed_boost_timer > 0:
                speed_boost_timer -= 1
            else:
                stop_speed_boost()
                catch_speed_boost = False

        if is_bullets_boost_on:
            bullets_boost_y += bullets_boost_change_y  # *  speed
            if not catch_bullets_boost and bullets_boost_y > 600:
                stop_bullets_boost()
            else:
                if not catch_bullets_boost:
                    show_bullets_boost(bullets_boost_x, bullets_boost_y)
                    catch_bullets_boost = False
                if bullets_boost_timer > 0:
                    bullets_boost_timer -= 1
                else:
                    stop_bullets_boost()
                    catch_bullets_boost = False

        player(playerX, plyerY)
        for t in range(num_of_enemies):
            enemy(enemyX[t], enemyY[t], t)
            show_score(score_x, score_y)
        pygame.display.update()
        clock.tick(60)


# main
intro()
game_loop()
