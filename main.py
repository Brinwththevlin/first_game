"""
    This is a very basic game buit using pygame
    The objective is to make a platformer/shooter (open to suggestions).
    Main Issues:
        1) I wish to have a the ability to spirnt,
           but it sometimes crashes unexpcetedly;
        2) need to change the enemy
            i) no death animations
        3) need to change the  back dorp
        4) only one screen at the moment (sidescroller? or maybe hard screen
           changes like in calstevainia or metroid?)
    potential improvements:
        1) life systems, how many lives do you get before a game over
        2) score system??
        3) upgrade system /power ups or other form of pickup (inventory?)
        4) extra mobility options (rolling/double jump/crouch)
        5) more variety in enemy types, attributes health
        6) pause menu (level select, restart, quit to main)
        7) title screen (dificulty setting, character select,
           save states(level passcodes), enimey encylopedea)
        8) if the game is simple enough and time permits machine learning to
           teach the game to play itself (unlikely or is another project idea)
"""
import pygame  # allows for 'easy' gamedev
from player import Player
from projectile import Projectile
from hitboxclass import HitBox


# doesn't have any means of attacking, and he is now
# too slow to just follow the player
class enemy(object):

    def __init__(self, x, y, width, height, end):
        self.x, self.y = x, y
        self.w, self.h = width, height
        self.end = end
        self.path = [self.x, self.end]  # need a more interesting walk pattern
        self.walkCount = 0
        self.vel = 3
        self.hitbox = HitBox(self.x + 20, self.y, 28, 60)
        self.idle = False
        self.maxHP = 5
        self.HP = self.maxHP
        self.Hbar = [pygame.image.load('pics/hb2.png'),
                     pygame.image.load('pics/hb21.png'),
                     pygame.image.load('pics/hb22.png'),
                     pygame.image.load('pics/hb23.png'),
                     pygame.image.load('pics/hb24.png'),
                     pygame.image.load('pics/hb2empty.png')]
        self.walkRight = [pygame.image.load('pics/R1E.png'),
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
        self.walkLeft = [pygame.image.load('pics/L1E.png'),
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

    def draw(self, win):
        self.move()
        # if not self.idle:
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            if not self.idle:
                self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            if not self.idle:
                self.walkCount += 1
        self.hitbox = HitBox(self.x + 20, self.y, 28, 60)

    def changeDirection(self):
        self.vel *= -1
        self.walkCount = 0

    # definitaly going to change, need a more interesting walk pattern
    def move(self):
        if (self.x > man.x and self.vel > 0) or (self.x < man.x and self.vel < 0):
            self.changeDirection()
            self.idle = False
        elif abs(self.x - man.x) <= 1:
            self.x = self.x
            self.idle = True
        else:
            self.x += self.vel
            self.idle = False

    def colliding(self, other):
        return other.hitbox.x >= self.hitbox.x and other.hitbox.x <= self.hitbox.x + self.hitbox.width and other.hitbox.y <= self.hitbox.y + self.hitbox.height and other.hitbox.y >= self.hitbox.y


# initiates the pygame
pygame.init()
# pygame.mixer.music.load("music.mp3")
# pygame.mixer.music.play()
mute = False

# initial window sizes
# Original: W, H = 500, 480 (Use this)
# for Repl: W, H = 800, 575
W = 500
H = 480

# opens a new window that is resizable named first game
win = pygame.display.set_mode((W, H))  # , pygame.RESIZABLE)
pygame.display.set_caption("bullet escape")

# background image, subject to change
bg = pygame.image.load('pics/bg.jpg')

# sets a clock and the FPS
clock = pygame.time.Clock()
FPS = 27

# gun information
magSize = 10
bullets = []
bulletBuffer = 6
bufferCount = 0
prevPress = False


man = Player(W/2, 400, 64, 64)
zombie = enemy(W/4, 400, 64, 64, 3*W/4)
run = True
invincibles = man.invincibleFrames


# redraws the window after every frame
def redrawGameWindow():
    print("Check")
    # uses the picture stored in bg as the background
    win.blit(bg, (0, 0))
    man.draw(win)
    if zombie:
        zombie.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if man:
        win.blit(man.Hbar[man.maxHP-man.HP], (0, 0))
        pygame.draw.rect(win, [225, 0, 0], man.hitbox.rect, 2)
    if zombie:
        win.blit(zombie.Hbar[zombie.maxHP - zombie.HP], (W-64, 0))
        pygame.draw.rect(win, [0, 225, 225], zombie.hitbox.rect, 2)
    pygame.display.update()


while run:
    print("Check")
    clock.tick(FPS)

    for event in pygame.event.get():
        # closes the window if you hit the big red X
        if event.type == pygame.QUIT:
            run = False

    # processes all the bullets on the screen
    for bullet in bullets:
        if bullet.x > W or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.x += bullet.vel
        if zombie:
            if zombie.colliding(bullet):
                bullets.pop(bullets.index(bullet))
                zombie.HP -= 1
                if zombie.HP == 0:
                    zombie = False
    if zombie:
        if zombie.colliding(man) and man.vulnerable:
            man.HP -= 1
            man.vulnerable = False
            if man.HP == 0:
                man = False
    # man = player character
    if man:
        if not man.vulnerable and invincibles < man.invincibleFrames:
            invincibles += 1
            print("can't hit me")
        else:
            invincibles = 0
            man.vulnerable = True
            print("ok yes you can")

    # stored a dict of ALL keyboard keys and whether they are being pressed
    keys = pygame.key.get_pressed()

    # quits if ESC is pressed
    if keys[pygame.K_ESCAPE]:
        run = False
    if man:
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

    # abruptly quits the game
    if not zombie or not man:
        run = False
    else:
        redrawGameWindow()

pygame.quit()
