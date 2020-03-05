import pygame
import random
import math
import pandas as pd
from openpyxl import Workbook

from time import sleep


# intialize the pygame
pygame.init()

# Screen/Window
screen = pygame.display.set_mode((800, 850))

# Title and Icon
pygame.display.set_caption("704 Machine Learning")
icon = pygame.image.load('car.png')
pygame.display.set_icon(icon)

# Player
playerImage = pygame.image.load('playercar.png')
playerX = 375
playerY = 750
playerXSpeed = 0
leftSpeed = -0.3
rightSpeed = 0.3

# Obstacle
obstacleImage = pygame.image.load('cone.png')
obstacleX = random.randint(200, 600)
obstacleY = 0
obstacleYSpeed = 0.4

# Coins
coinImage = pygame.image.load('coin.png')
coinX = random.randint(200, 600)
coinY = 0
coinSpeed = 0.5

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 26)
textX = 10
textY = 10

# Game Over
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)

# Flavour
roadMarking1X = 400
roadMarking1Y = 0
roadMarking2X = 400
roadMarking2Y = 425
roadMarkingSpeed = 0.4

# Error rate 24 and it collides
errorSize = 50
errorRate = 1

# Game restart
gameOver = False

# Testing Data
#df = pd.read_csv('MLDrivingData.csv')


##################################################################################################
# Renders text(score) to screen at x , y
def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Renders game over text(score) to screen at x , y
def gameOverText():
    gameOverText = gameOverFont.render("Score: " + str(scoreValue), True, (0, 0, 0))
    screen.blit(gameOverText, (280, 300))


# Draw player at x , y
def player(x, y):
    screen.blit(playerImage, (x, y))


# Draw obstacle at x , y
def obstacle(x, y):
    screen.blit(obstacleImage, (x, y))


# Draw coin at x , y
def coin(x, y):
    screen.blit(coinImage, (x, y))


# distance between 2 coordinates, (less than 27), collision
def isCollision(obstacleX, obstacleY, playerX, playerY):
    distance = math.sqrt((math.pow(obstacleX - playerX, 2)) + (math.pow(obstacleY - playerY, 2)))
    if distance < 28:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # Draw background, grass , barriers and road markings
    screen.fill((75, 75, 75))
    pygame.draw.rect(screen, (100, 140, 100), [0, 0, 150, 850])
    pygame.draw.rect(screen, (30, 30, 30), [140, 0, 10, 850])
    pygame.draw.rect(screen, (100, 140, 100), [650, 0, 200, 850])
    pygame.draw.rect(screen, (30, 30, 30), [650, 0, 10, 850])
    pygame.draw.rect(screen, (200, 200, 200), [roadMarking1X, roadMarking1Y, 20, 100])
    pygame.draw.rect(screen, (200, 200, 200), [roadMarking2X, roadMarking2Y, 20, 100])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXSpeed = leftSpeed

            if event.key == pygame.K_RIGHT:
                playerXSpeed = rightSpeed

            # Player Speed up slow down logic
            if event.key == pygame.K_UP:
                obstacleYSpeed += 0.1
                roadMarkingSpeed += 0.1
                coinSpeed += 0.1
            if event.key == pygame.K_DOWN:
                obstacleYSpeed -= 0.1
                roadMarkingSpeed -= 0.1
                coinSpeed -= 0.1

        # Maybe add some logic here for retaining speed when released, maybe halves?
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXSpeed = 0

    # some form of ai thing
    '''
    if (obstacleY > 400) and (obstacleX <= playerX <= obstacleX + errorSize):
        playerXSpeed = rightSpeed
    elif coinX <= playerX:
        playerXSpeed = leftSpeed
    if (obstacleY > 400) and obstacleX >= playerX >= obstacleX - errorSize:
        playerXSpeed = leftSpeed
    elif coinX >= playerX:
        playerXSpeed = rightSpeed
    '''


    '''
    if coinX <= playerX:
        playerXSpeed = leftSpeed
    elif coinX == playerX:
        playerXSpeed = 0.0

    if coinX >= playerX:
        playerXSpeed = rightSpeed
    elif coinX == playerX:
        playerXSpeed = 0.0
        
    if (obstacleY > 400) and (obstacleX <= playerX <= obstacleX + 32):
        playerXSpeed = rightSpeed
    elif playerX >= obstacleX + 40:
        playerXSpeed = 0.0
    if (obstacleY > 400) and obstacleX >= playerX >= obstacleX - 32:
        playerXSpeed = leftSpeed
    elif playerX <= obstacleX - 40:
        playerXSpeed = 0.0
        
    '''
    # Update player left/right speed
    playerX += playerXSpeed

    # Checking for boundaries(barriers)
    if playerX <= 100:
        playerX = 100
    elif playerX > 640:
        playerX = 640

    # Obstacle movement + re spawn
    obstacleY += obstacleYSpeed

    if obstacleY >= 850:
        obstacleY = -50
        obstacleX = random.randint(175, 625)
        scoreValue += 1

        # Increase difficulty
        obstacleYSpeed += 0.01
        roadMarkingSpeed += 0.01
        coinSpeed += 0.01

        # Decrease error size
        errorSize = errorSize - errorRate


   # if scoreValue == 10:
       # print("10 score met spawn new obstacle")

    # Road markings + re spawn
    roadMarking1Y += roadMarkingSpeed
    roadMarking2Y += roadMarkingSpeed
    if roadMarking1Y >= 850:
        roadMarking1Y = -50
        roadMarking1X = 400
    if roadMarking2Y >= 850:
        roadMarking2Y = -50
        roadMarking2X = 400

    # Coin logic
    coinY += coinSpeed
    coinCollision = isCollision(coinX, coinY, playerX, playerY)
    if coinCollision:




        coinY = -50
        coinX = random.randint(175, 625)
        scoreValue += 1


    if coinY >= 850:
        coinY = -50
        coinX = random.randint(175, 625)

    # Collision/ Game over
    collision = isCollision(obstacleX, obstacleY, playerX, playerY)
    if collision:
        obstacleYSpeed = 0
        playerXSpeed = 0
        roadMarkingSpeed = 0
        coinSpeed = 0
        gameOverText()
        gameOver = True

    if gameOver == True:
        obstacleY = -50
        obstacleX = random.randint(175, 625)
        obstacleYSpeed = 0.4
        roadMarkingSpeed = 0.4
        coinSpeed = 0.5
        coinY = -50
        coinX = random.randint(175, 625)
        scoreValue = 0
        errorSize = 50
        sleep(3)
        gameOver = False

    # Update image locations
    player(playerX, playerY)
    obstacle(obstacleX, obstacleY)
    coin(coinX, coinY)
    showScore(textX, textY)
    pygame.display.update()
