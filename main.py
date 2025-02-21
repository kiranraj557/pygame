import pygame
import random
import math
#intialize the pygame
pygame.init()

#create a screen
screen = pygame.display.set_mode((700,600))

pygame.display.set_caption("Space")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("player.png")
playerX = 300
playerY = 520
playerX_change = 0


#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,700))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)

#bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 520
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",20)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font("freesansbold.ttf",80)

def show_score(x,y):
    score = font.render("score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = font.render("GAME OVER: " + str(score_value),True,(255,255,255))
    screen.blit(over_text,(250,300))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))    

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False    



running = True
while running:

    screen.fill((0, 0 ,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                            
    playerX += playerX_change 

# check for boundaries    
    if playerX <=0:
        playerX = 0
    elif playerX >= 636:
        playerX = 636
    
    # enemy movement
    for i in range (num_of_enemies):
        
        #game over
        if enemyY[i] > 500:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 636:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        
        #collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,700)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 520
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

  
        
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()