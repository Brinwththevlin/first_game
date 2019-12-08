"""
    This is a very basic game buit using pygame
    The objective is to make a platformer/shooter (open to suggestions).
    Main Issues:
        1) I wish to have a the ability to spirnt,
           but it sometimes crashes unexpcetedly;
        2) No collision detection, no platforms for platforming
        3) need to change the enemy
            i) no death animations
            ii) no health bar / health pick ups
        4) need to change the  back dorp
        5) only one screen at the moment (sidescroller? or maybe hard screen
           changes like in calstevainia or metroid?)
        6) I DID NOT make the sprites in use preferably we would make them or
           at least change the ones available
    potential improvements:
        1) life systems, how many lives do you get before a game over
        2) winning condition
        3) score system??
        4) upgrade system /power ups or other form of pickup (inventory?)
        5) extra mobility options (rolling/double jump/crouch)
        6) more variety in enemy types, attributes health
        7) pause menu (level select, restart, quit to main)
        8) title screen (dificulty setting, character select,
           save states(level passcodes), enimey encylopedea)
        9) if the game is simple enough and time permits machine learning to
           teach the game to play itself (unlikely or is another project idea)
"""
import pygame  # allows for 'easy' gamedev
from player import Player
from projectile import Projectile
from hitboxClass import HitBox


class enemy(object):
    walkRight = [pygame.image.load('pics/R1E.png'),
                 pygame.image.load('pics/R2E.png'),
                 pygame.image.load('pics/R3E.png'),
                 pygame.image.load('pics/R4E.png'),
                 pygame.image.load('pics/R5E.png'),
                 pygame.image.load('pics/R6E.png'),
                 pygame.image.load('pics/R7E.png'),
                 pygame.image.load('pics/R8E.png'),
                 pygame.image.load('pics/R9E.png'),
                 pygame.image.load('pics/R10E.png'),
                 pygame.image.load('pics/R11E.png')]
    walkLeft = [pygame.image.load('pics/L1E.png'),
                pygame.image.load('pics/L2E.png'),
                pygame.image.load('pics/L3E.png'),
                pygame.image.load('pics/L4E.png'),
                pygame.image.load('pics/L5E.png'),
                pygame.image.load('pics/L6E.png'),
                pygame.image.load('pics/L7E.png'),
                pygame.image.load('pics/L8E.png'),
                pygame.image.load('pics/L9E.png'),
                pygame.image.load('pics/L10E.png'),
                pygame.image.load('pics/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.end = end
        self.path = [self.x, self.end]  # need a more interesting walk pattern
        self.walkCount = 0
        self.vel = 3
        self.hitbox = HitBox(self.x + 20, self.y, 28, 60)
        self.idle = False

    def draw(self, win):
        self.move()
        # if not self.idle:
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = HitBox(self.x + 20, self.y, 28, 60)

    def changeDirection(self):
        self.vel *= -1
        self.walkCount = 0

    # definitaly going to change, need a more interesting walk pattern
    def move(self):
        if (self.x > man.x and self.vel > 0) or (self.x < man.x and self.vel < 0):
            self.changeDirection()
        elif abs(self.x - man.x) <= 1:
            self.x = self.x
            self.idle = True
        else:
            self.x += self.vel


# class not necisarry but makes it cleaner for when we add more things

# initiates the pygame
pygame.init()
pygame.mixer.music.load("desert.mp3")
pygame.mixer.music.play()

mute = False
# initial window sizes
W = 500
H = 480

# health bars
zombieHealth = 10
playerHealth = 10

playerHbar = [pygame.image.load('pics/hb1.png')]
# opens a new window that is resizable named first game
win = pygame.display.set_mode((W, H))  # , pygame.RESIZABLE)
pygame.display.set_caption("bullet escape")

# loads all of the right walking art into an array to be cycled through


bg = pygame.image.load('pics/bg.jpg')  # background image, subject to change
char = pygame.image.load('pics/standing.png')  # idle image

# sets a clock and the FPS
clock = pygame.time.Clock()
FPS = 27


# redraws the window after every frame
def redrawGameWindow():

    win.blit(bg, (0, 0))  # uses the picture stored in bg as the background
    man.draw(win)
    if zombie:
        zombie.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    win.blit(playerHbar[0], (0, 0))
    pygame.display.update()


# gun information
magSize = 10
bullets = []
bulletBuffer = 6
bufferCount = 0
prevPress = False

# main loop
man = Player(W/2, 400, 64, 64)
zombie = enemy(W/4, 410, 64, 64, 3*W/4)
run = True


def inBox(b):
    if zombie:
        return b.x > zombie.hitbox.x and b.x < zombie.hitbox.x+zombie.hitbox.width and b.y < zombie.hitbox.y+zombie.hitbox.height and b.y > zombie.hitbox.y


while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        # closes the window if you hit the big red X
        if event.type == pygame.QUIT:
            run = False

        # **********FIXME************#
        # # properly resizes the game
        # if event.type == pygame.VIDEORESIZE:
        #     W = event.w
        #     H = event.h
        #     win = pygame.display.set_mode((W, H), pygame.RESIZABLE)

    for bullet in bullets:
        if bullet.x > W or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.x += bullet.vel
        if(inBox(bullet)):
            bullets.pop(bullets.index(bullet))
            zombieHealth -= 1
            if zombieHealth == 0:
                zombie = False

    # stored a dict of ALL keyboard keys and whether they are being pressed
    keys = pygame.key.get_pressed()

    # quits if ESC is pressed
    if keys[pygame.K_ESCAPE]:
        run = False

    # allows you to fire bullets
    if keys[pygame.K_SPACE]:
        if bufferCount >= bulletBuffer:
            bufferCount = 0
        if not prevPress or bufferCount == 0:
            if len(bullets) < magSize:
                if man.left:
                    f = -1
                else:
                    f = 1
                Bx = round(man.x+man.w//2)
                By = round(man.y+man.h//2)
                black = [0, 0, 0]
                bullet = Projectile(Bx, By, 4, black, f)
                bullets.append(bullet)
                prevPress = True
        bufferCount += 1
    else:
        prevPress = False

    # ability to mute the music
    if keys[pygame.K_m]:
        if not mute:
            pygame.mixer.music.set_volume(0)
            mute = True

        else:
            pygame.mixer.music.set_volume(.3)
            mute = False

    # uses arrow keys or WASD to move left and right
    if keys[pygame.K_a] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_d] and man.x + man.w < W:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    # jumping algorithim, needs improvemnt to parabolic in my oppinion
    if not (man.isJump):
        if keys[pygame.K_w]:
            man.isJump = True
            man.walkCount = 0

    else:
        if man.jumpCount >= -man.jumpFrames:
            if man.jumpCount >= 0:
                man.y -= ((man.jumpCount)**2) * 0.5
                man.jumpCount -= 1
            else:
                man.y += ((man.jumpCount)**2) * 0.5
                man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = man.jumpFrames

    redrawGameWindow()


pygame.quit()
