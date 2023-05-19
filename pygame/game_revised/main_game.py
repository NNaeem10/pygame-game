import pygame
import random
import moviepy.editor

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('Noob game')

# Variables
s_width = 1000
s_height = 800

bg = pygame.transform.scale(pygame.image.load('pictures/bg_og.png'), (s_width, s_height))
screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

d_s = pygame.transform.scale(pygame.image.load('pictures/wasted.png'), (s_width, s_height))

font = pygame.font.SysFont('comicsans', 20)

bg_music = pygame.mixer.music.load('sounds/bg-music.ogg')
wasted = pygame.mixer.Sound('sounds/wasted.ogg')
hit = pygame.mixer.Sound('sounds/hit.ogg')
nom = pygame.mixer.Sound('sounds/nom.ogg')

win_vid = moviepy.editor.VideoFileClip('videos/win_vid.mp4')

pygame.mixer.music.play(-1)




#  * character class
class character:
    x_pos = 0
    y_pos = 0
    x_speed = 10
    y_speed = 10
    hearts = 3
    img = pygame.image.load('pictures/noob.png')
    size = (0, 0)
    avatar = None
    is_alive = None

    def __init__(self, x, y, size) -> None:
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.avatar = pygame.transform.scale(self.img, self.size)
        self.is_alive = True

    def move(self):
        keys = pygame.key.get_pressed()
        # * edge overcross prevention
        if 0 < self.x_pos:
            self.x_pos -= self.x_speed * keys[pygame.K_LEFT]
        if self.x_pos < s_width - self.size[0]:
            self.x_pos += self.x_speed * keys[pygame.K_RIGHT]
        if 0 < self.y_pos:
            self.y_pos -= self.y_speed * keys[pygame.K_UP]
        if self.y_pos < s_height - self.size[1]:
            self.y_pos += self.y_speed * keys[pygame.K_DOWN]

# * heart class
class heart:
    x_pos = 0
    y_pos = 0
    size = 50
    img = ''
    
    def __init__(self,x, y) -> None:
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.transform.scale(pygame.image.load('pictures/heart.png'), (self.size, self.size))

# * glob class
class glob:
    x_pos = 0
    y_pos = 0
    size = 30
    img = ''
    colors = {
        1: 'red',
        2: 'blue',
        3: 'yellow',
        4: 'green'
    }

    def __init__(self, x, y) -> None:
        self.x_pos = x
        self.y_pos = y
        color_tag = random.randint(1, 4)
        self.img = pygame.transform.scale(pygame.image.load(f'pictures/{self.colors[color_tag]}.png'), (self.size, self.size))

# * spike class
class spike:
    x_pos = 0
    y_pos = 0
    size = 70
    img = ''

    def __init__(self, x, y) -> None:
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.transform.scale(
            pygame.image.load('pictures/spike.png'), (self.size, self.size))

# * check for collision
def checkCollision(character, npc):
    c_size = character.size
    n_size = npc.size
    if (character.x_pos < npc.x_pos + n_size and
        character.x_pos + c_size[0] > npc.x_pos and
        character.y_pos < npc.y_pos + n_size and
            character.y_pos + c_size[1] > npc.y_pos):
        return True
    return False

def spawnNPC(npc):
    return npc(random.randint(1, s_width-npc.size),
                random.randint(1, s_height-npc.size))

# * instantiation
noob = character(s_width//2, s_height//2, (100, 100))

hearts = []
h_x = 0
for _ in range(noob.hearts):
    hearts.append(heart(h_x, 0))
    h_x += heart.size

globs = []
glob_counter = 0
# creating globs
for _ in range(5):
    globs.append(spawnNPC(glob))

spikes = []
# creating spikes
for _ in range(5):
    spikes.append(spawnNPC(spike))

win_count = 100
sound_not_played = True
globs_for_heart =  10
vid_not_played = True

# ! main loop here
game = True
while game:
    clock.tick(30)

    if noob.is_alive:
        if glob_counter < win_count:
            screen.blit(bg, (0, 0))

            # * the character himself
            noob.move()
            screen.blit(noob.avatar, (noob.x_pos, noob.y_pos))

            # * the hearts
            for h in hearts:
                screen.blit(h.img, (h.x_pos, h.y_pos))

            # * the globs
            for g in globs:
                screen.blit(g.img, (g.x_pos, g.y_pos))
                # * collision detection
                if checkCollision(noob, g):
                    globs.remove(g)
                    glob_counter += 1
                    globs.append(glob(random.randint(1, s_width-glob.size),
                                      random.randint(1, s_height-glob.size)))
                    pygame.mixer.Sound.play(nom)
                    heart_replenished = False

            # * the spikes
            for s in spikes:
                screen.blit(s.img, (s.x_pos, s.y_pos))
                if checkCollision(noob, s):
                    spikes.remove(s)
                    noob.hearts -= 1
                    hearts.pop(-1)
                    pygame.mixer.Sound.play(hit)
                    spikes.append(spike(random.randint(1, s_width-spike.size),
                                      random.randint(1, s_height-spike.size)))

            # * heart replenished
            if glob_counter > 0 and glob_counter % globs_for_heart == 0 and not heart_replenished and noob.hearts < 3:
                hearts.append(heart(hearts[-1].x_pos + heart.size, 0))
                heart_replenished = True
                noob.hearts += 1

        else:
            pygame.mixer.music.stop()
            # ? win screen
            if vid_not_played:
                win_vid.preview()
                vid_not_played = False
            screen.fill((0, 255, 0))
            win = font.render('YOU WIN!', 1, (255, 0, 0))
            screen.blit(win, (s_width//2, s_height//2))


        if noob.hearts == 0:
            noob.is_alive = False
    
    else:
        if sound_not_played:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(wasted)
            sound_not_played = False
        # death screen
        screen.fill((0, 0, 0))
        screen.blit(d_s, (0, 0))

    # * exiting the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    
    pygame.display.update()
