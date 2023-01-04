import pygame
import random
import os

screenX = 700
screenY = 700

s = 'sounds'
p = 'pictures'

class Glob:
    x_pos = 0
    y_pos = 0
    image = ''
    size = 30 # default value

    def __init__(self, x_pos, y_pos, image) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Player:
    x_pos = 0
    y_pos = 0
    x_speed = 0
    y_speed = 0
    hearts = 3
    size = 60
    image = pygame.transform.scale(
        pygame.image.load(os.path.join(p, 'noob.png')),
        (size, size)
    )

    def __init__(self, xpos, ypos, xspeed, yspeed) -> None:
        self.x_pos = xpos
        self.y_pos = ypos
        self.x_speed = xspeed
        self.y_speed = yspeed

    def moveCharacter(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # event handler
        keys = pygame.key.get_pressed()

        if 0 < self.x_pos < screenX and 0 < self.y_pos < screenY:
            self.x_pos += (keys[pygame.K_RIGHT] -
                           keys[pygame.K_LEFT]) * self.x_speed
            self.y_pos += (keys[pygame.K_DOWN] -
                           keys[pygame.K_UP]) * self.y_speed

        # restricting boundary movement
        if self.x_pos <= self.size:
            self.x_pos += (keys[pygame.K_RIGHT]) * self.x_speed
            self.y_pos += (keys[pygame.K_DOWN] -
                           keys[pygame.K_UP]) * self.y_speed
        elif self.x_pos + self.size >= screenX:
            self.x_pos -= (keys[pygame.K_LEFT]) * self.x_speed
            self.y_pos += (keys[pygame.K_DOWN] -
                           keys[pygame.K_UP]) * self.y_speed
        elif self.y_pos <= self.size:
            self.x_pos += (keys[pygame.K_RIGHT] -
                           keys[pygame.K_LEFT]) * self.x_speed
            self.y_pos += (keys[pygame.K_DOWN]) * self.y_speed
        elif self.y_pos + self.size >= screenY:
            self.x_pos += (keys[pygame.K_RIGHT] -
                           keys[pygame.K_LEFT]) * self.x_speed
            self.y_pos -= (keys[pygame.K_UP]) * self.y_speed


class Spike:
    x_pos = 0
    y_pos = 0
    size = 50 # default value

    image = pygame.transform.scale(pygame.image.load(
        os.path.join(p, 'spike.png')), (size, size))

    def __init__(self, x, y) -> None:
        self.x_pos = x
        self.y_pos = y


def spawnGlob():
    color_randomiser = random.randint(1, 4)
    colors = {
        1: 'blue.png',
        2: 'yellow.png',
        3: 'green.png',
        4: 'red.png'
    }
    position_randomiser = [random.randint(
        0, screenX-30), random.randint(0, screenY-30)]
    rGlob = Glob(
        position_randomiser[0], position_randomiser[1], os.path.join(p, colors[color_randomiser]))
    return rGlob


def spawnSpike():
    position_randomiser = [random.randint(
        0, screenX-50), random.randint(0, screenY-50)]
    rSpike = Spike(
        position_randomiser[0], position_randomiser[1])
    return rSpike


def checkCollision(player: Player, Object):
    if player.x_pos < Object.x_pos < player.x_pos+player.size and player.y_pos < Object.y_pos < player.y_pos+player.size:
        return True
    return False

# initialising pygame and others
pygame.init()
pygame.font.init()
pygame.mixer.init()

# variables and instantiation
noob = Player(350, 350, 5, 5)

nom = pygame.mixer.Sound(os.path.join(s, 'nom-nom-nom.ogg'))
hit = pygame.mixer.Sound(os.path.join(s, 'hit.ogg'))
wasted = pygame.mixer.Sound(os.path.join(s, 'wasted.ogg'))
music = pygame.mixer.music.load(os.path.join(s, 'bg-music.ogg'))

screen = pygame.display.set_mode((screenX, screenY))
bg = pygame.transform.scale(pygame.image.load(
    os.path.join(p, 'bg_og.png')), (screenX, screenY))
clock = pygame.time.Clock()

death_screen = pygame.transform.scale(pygame.image.load(os.path.join(p, 'wasted.png')), (700, 300))
clear = pygame.transform.scale(pygame.image.load(
    os.path.join(p, 'back.png')), (screenX, screenY))

glob_counter = 0
spike_counter = 5
score = 0

spikes = []

game = True

# background music hehe
pygame.mixer.music.play(-1)

sound_not_played = True

# while game:
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_q]:
#         game = False

    # glitchy exit idk why tho
    
# game runs here
while noob.hearts > 0:
    clock.tick(30)
    noob.moveCharacter()

    if glob_counter <= 1:
        rGlob = spawnGlob()
        noGlobs = False
        glob_counter += 1
    if checkCollision(noob, rGlob):
        score += 1
        noGlobs = True
        glob_counter -= 1
        pygame.mixer.Sound.play(nom)

    # if spike_counter <= 1:
    #     noSpikes = False
    #     spikes.append(spawnSpike())
    #     spike_counter += 1

    while len(spikes) < spike_counter:
        spikes.append(spawnSpike())

    noSpikes = True if len(spikes) == 0 else False

    screen.blit(bg, (0, 0))
    screen.blit(noob.image, (noob.x_pos, noob.y_pos))

    if not noGlobs:
        screen.blit(rGlob.image, (rGlob.x_pos, rGlob.y_pos))

    if not noSpikes:
        for i in range(len(spikes)):
            spike = spikes[i]
            if checkCollision(noob, spike):
                score -= 1
                # spike_counter -= 1
                spikes[i] = None
                pygame.mixer.Sound.play(hit)
                noob.hearts -= 1
            while None in spikes:
                spikes.remove(None)
            # if spike_counter == 0:
            #     noSpikes = True
            screen.blit(spike.image, (spike.x_pos, spike.y_pos))
    pygame.display.update()

    # pygame.mixer.music.stop()
    # if sound_not_played:
    #     pygame.mixer.Sound.play(wasted)
    #     sound_not_played = False
    # screen.blit(clear, (0, 0))
    # screen.blit(death_screen, (0,100))
    # pygame.display.update()
    
        # pygame.quit()

# TODO: THINK ABOUT MORE THAN ONE SPIKE