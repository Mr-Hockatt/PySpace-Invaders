import pygame, random, math
from pygame import mixer


#INITIALIZE PYGAME
pygame.init()

#CREATE A SCREEN
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#ADD A BACKGROUND
background = pygame.image.load('background.png')

#ADD MUSIC
mixer.music.load('background.wav')
mixer.music.play(-1)

#CREATE A CLOCK (TO CONTROL FPS)
clock = pygame.time.Clock()

#TITLE AND ICON
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#PLAYER
player_image = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_velocity = 0

def Draw_Player(x, y):
    screen.blit(player_image, (player_x, player_y))


#ENEMY
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_velocity = []
enemy_y_velocity = []
enemy_number = 10

for i in range(enemy_number):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_velocity.append(2)
    enemy_y_velocity.append(64)

def Draw_Enemy(x, y, i):
    screen.blit(enemy_image[i], (enemy_x[i], enemy_y[i]))

#BULLET
bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_velocity = 0
bullet_y_velocity = -10
bullet_state = "ready"

def Fire_Bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x+16, y+10))

def Is_Collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x-bullet_x)**2 + (enemy_y-bullet_y)**2)
    if distance < 27:
        return True
    else:
        return False

score_value = 0
Font = pygame.font.Font('Bajawa.ttf', 32)
#Font = pygame.font.SysFont('Bahnschrift Light', 32)
text_x = 10
text_y = 10

def Show_Score(x, y):
    score = Font.render("Score: "+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

Font2 = pygame.font.Font('Bajawa.ttf', 64)

def Game_Over():
    end_game = Font2.render("GAME OVER", True, (255, 255, 255))
    screen.blit(end_game, (200, 250))

running = True
while running:

    #screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_velocity = -10
            if event.key == pygame.K_RIGHT:
                player_x_velocity = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    Fire_Bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_velocity = 0



    if player_x > screen_width - 64:
        player_x = screen_width - 64
    if player_x < 0:
        player_x = 0

    for i in range(enemy_number):

        if enemy_y[i] > 440:
            for j in range(enemy_number):
                enemy_y[j] = 2000
            Game_Over()
            break

        if enemy_x[i] > screen_width - 64:
            enemy_x_velocity[i] = -enemy_x_velocity[i]
            enemy_y[i] = enemy_y[i] + enemy_y_velocity[i]
        if enemy_x[i] < 0:
            enemy_x_velocity[i] = -enemy_x_velocity[i]
            enemy_y[i] = enemy_y[i] + enemy_y_velocity[i]

        collision = Is_Collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value = score_value + 1
            print(score_value)
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy_x[i] = enemy_x[i] + enemy_x_velocity[i]
        Draw_Enemy(enemy_x[i], enemy_y[i], i)

    if bullet_state is "fire":
        Fire_Bullet(bullet_x, bullet_y)
        bullet_y = bullet_y + bullet_y_velocity
    if bullet_y<=0:
        bullet_y = 480
        bullet_state = "ready"



    player_x = player_x + player_x_velocity


    Draw_Player(player_x, player_y)
    Show_Score(text_x, text_y)

    pygame.display.update()
    clock.tick(60)
