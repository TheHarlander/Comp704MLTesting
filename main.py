import pygame
import random
import math
import pickle
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
leftSpeed = -0.6
rightSpeed = 0.6

# Obstacle
obstacleImage = pygame.image.load('cone.png')
obstacleX = random.randint(200, 600)
obstacleY = 0
obstacleYSpeed = 0.8

# Coins
coinImage = pygame.image.load('coin.png')
coinX = random.randint(200, 600)
coinY = 0
coinSpeed = 1

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 26)
textX = 10
textY = 10

# Flavour
roadMarking1X = 400
roadMarking1Y = 0
roadMarking2X = 400
roadMarking2Y = 425
roadMarkingSpeed = 0.8

# Game restart
gameOver = False

#################################################################################################

# Testing data #
# Linear Regression = LRtestTrainData.pkl
# MulitLinear Regression = MLRtestTrainData.pkl
# Gradient boosting Regression = GBRtestTrainData.pkl
# Voter Regression = VRtestTrainData.pkl

infile = open("VRtestTrainData.pkl", 'rb')
pickleModel = pickle.load(infile)
infile.close()


##################################################################################################
# Renders text(score) to screen at x , y
def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, (0, 0, 0))
    screen.blit(score, (x, y))

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

def mLPredictiction(X):
    X = [[coinX]]
    ynew = pickleModel.predict(X)

    if playerX > ynew:
        playerXSpeed = leftSpeed

    elif playerX < ynew:
        playerXSpeed = rightSpeed


# Game Loop
running = True
while running:

    # Draw background, grass , barriers and road markings
    screen.fill((75, 75, 75))
    pygame.draw.rect(screen, (100, 140, 100), [0, 0, 150, 850])
    pygame.draw.rect(screen, (30, 30, 30), [140, 0, 10, 850])
    pygame.draw.rect(screen, (100, 140, 100), [650, 0, 200, 850])
    pygame.draw.rect(screen, (30, 30, 30), [650, 0, 10, 850])
    pygame.draw.rect(screen, (200, 200, 200), [round(roadMarking1X), round(roadMarking1Y), 20, 100])
    pygame.draw.rect(screen, (200, 200, 200), [round(roadMarking2X), round(roadMarking2Y), 20, 100])

    ##############################################################################
   # Data prediction and movement

    nearBool = 0
    if obstacleY >= 600:
        nearBool = 1
    elif obstacleY < 600:
        nearBool = 0

    # LR =  X = [[coinX]]
    # MLR = X = [[obstacleX,obstacleY, coinX, coinY]]
    # GBR + VR =  X = [[obstacleX,obstacleY, coinX, coinY, nearBool]]

    X = [[obstacleX,obstacleY, coinX, coinY, nearBool]]

    ynew = pickleModel.predict(X)

    if playerX > ynew:
        playerXSpeed = leftSpeed

    elif playerX < ynew:
        playerXSpeed = rightSpeed

    ###################################################################################################################
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


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXSpeed = 0

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
        gameOver = True

    if gameOver == True:
        obstacleY = -50
        obstacleX = random.randint(175, 625)
        obstacleYSpeed = 0.8
        roadMarkingSpeed = 0.8
        coinSpeed = 1
        coinY = -50
        coinX = random.randint(175, 625)
        scoreValue = 0
        errorSize = 50
        sleep(3)
        gameOver = False

    # Update image locations
    player(round(playerX), round(playerY))
    obstacle(round(obstacleX), round(obstacleY))
    coin(round(coinX), round(coinY))
    showScore(round(textX), round(textY))
    pygame.display.update()
