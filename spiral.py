import pygame

screenX = 700
screenY = 700

class Block:
    x_position = 0
    y_position = 0
    x_speed = 0
    y_speed = 0
    image = pygame.image.load("blue.png")

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

    def spiral(self, magnitude, direction):
        if self.x_position >= (screenX-50) or self.x_position <= 0:
            self.x_speed *= -1
            magnitude = 1
        if self.y_position >= (screenY-50) or self.y_position <= 0:
            self.y_speed *= -1
            magnitude = 1
        magnitude %= 100
        if direction == 0:
            self.x_position += 0
            self.y_position += (-1 * abs(self.y_speed))*magnitude
        elif direction == 1:
            self.x_position += abs(self.x_speed) * magnitude
            self.y_position += (-1 * abs(self.y_speed))*magnitude
        elif direction == 2:
            self.x_position += abs(self.x_speed) * magnitude
            self.y_position += 0
        elif direction == 3:
            self.x_position += abs(self.x_speed) * magnitude
            self.y_position += abs(self.y_speed) * magnitude
        elif direction == 4:
            self.x_position += 0
            self.y_position += abs(self.y_speed) * magnitude
        elif direction == 5:
            self.x_position += (-1 * abs(self.x_speed)) * magnitude
            self.y_position += abs(self.y_speed)*magnitude
        elif direction == 6:
            self.x_position += (-1 * self.x_speed) * magnitude
            self.y_position += 0
        elif direction == 7:
            self.x_position += (-1 * abs(self.x_speed)) * magnitude
            self.y_position += (-1 * abs(self.y_speed))*magnitude


block_1 = Block(350, 350, 2, 2, 'blue.png')
block_2 = Block(240, 300, 2, -2, 'red.png')
block_3 = Block(470, 360, -2, 2, 'yellow.png')
block_4 = Block(80, 0, -2, -2, 'green.png')

pygame.init()
screen = pygame.display.set_mode((screenX, screenY))
background = pygame.image.load("new_back.png")
clock = pygame.time.Clock()
counter = 0
gameFlag = True

while gameFlag:
    counter += 0.5
    clock.tick(20)
    block_1.spiral(counter, counter%8)
    block_2.spiral(counter, counter%8)
    block_3.spiral(counter, counter%8)
    block_4.spiral(counter, counter%8)
    # screen.blit(background, (0, 0))
    screen.blit(block_1.image, (block_1.x_position, block_1.y_position))
    screen.blit(block_2.image, (block_2.x_position, block_2.y_position))
    screen.blit(block_3.image, (block_3.x_position, block_3.y_position))
    screen.blit(block_4.image, (block_4.x_position, block_4.y_position))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False