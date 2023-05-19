import pygame
import os

p = 'pictures'

screenX = 500
screenY = 500

class Block:
    x_position = 0
    y_position = 0
    x_speed = 0
    y_speed = 0
    image = pygame.image.load(os.path.join(p, "blue.png"))

    def __init__(self, thisXPos, thisYPos, thisXSpeed, thisYSPeed, image) -> None:
        self.x_position = thisXPos
        self.y_position = thisYPos
        self.x_speed = thisXSpeed
        self.y_speed = thisYSPeed
        self.image = pygame.image.load(image)

    def update_block(self):
        self.x_position += self.x_speed
        if self.x_position >= (screenX-50) or self.x_position <= 0:
            self.x_speed *= -1
        self.y_position += self.y_speed
        if self.y_position >= (screenY-50) or self.y_position <= 0:
            self.y_speed *= -1

block_1 = Block(200, 200, 2, 2, os.path.join(p, 'blue.png'))
block_2 = Block(250, 200, -2, 2, os.path.join(p, 'red.png'))
block_3 = Block(200, 250, 2, -2, os.path.join(p, 'yellow.png'))
block_4 = Block(250, 250, -2, -2, os.path.join(p, 'green.png'))

pygame.init()
screen = pygame.display.set_mode((screenX, screenY))
background = pygame.image.load(os.path.join(p, "back.png"))
clock = pygame.time.Clock()
gameFlag = True

while gameFlag:
    # every time you update the screen, you need the background to get rid of the previous frames on the screen
    clock.tick(120)
    block_1.update_block()
    block_2.update_block()
    block_3.update_block()
    block_4.update_block()
    screen.blit(background, (0, 0))
    screen.blit(block_1.image, (block_1.x_position, block_1.y_position))
    screen.blit(block_2.image, (block_2.x_position, block_2.y_position))
    screen.blit(block_3.image, (block_3.x_position, block_3.y_position))
    screen.blit(block_4.image, (block_4.x_position, block_4.y_position))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False

# TODO: TRY AND ENHANCE IT BROTHER!