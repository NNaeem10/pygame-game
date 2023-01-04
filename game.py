import pygame
import os

s = 'sounds'
p = 'pictures'

class Block:
    x_position = 0
    y_position = 0
    x_speed = 0
    y_speed = 0
    image = pygame.image.load(os.path.join(p, "blue.png"))

    def __init__(self, thisXPos, thisYPos, thisXSpeed, thisYSPeed) -> None:
        self.x_position = thisXPos
        self.y_position = thisYPos
        self.x_speed = thisXSpeed
        self.y_speed = thisYSPeed

    def update_block(self):
        self.x_position += self.x_speed
        self.y_position += self.y_speed

# main
block_1 = Block(0, 0, 2, 2)
block_2 = Block(1200, 0, -2, 2)

# pygame
pygame.init()
screen = pygame.display.set_mode((1200, 680))
background = pygame.image.load(os.path.join(p, "back.png"))
clock = pygame.time.Clock()

while True:
    # every time you update the screen, you need the background to get rid of the previous frames on the screen
    clock.tick(60)
    block_1.update_block()
    block_2.update_block()
    screen.blit(background, (0, 0))
    screen.blit(block_1.image, (block_1.x_position, block_1.y_position))
    screen.blit(block_2.image, (block_2.x_position, block_2.y_position))
    pygame.display.update()