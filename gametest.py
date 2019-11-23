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

# initiates the pygame
pygame.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()

mute = False
# initial window sizes
W = 500
H = 480

# opens a new window that is resizable named first game
win = pygame.display.set_mode((W, H))  # , pygame.RESIZABLE)
pygame.display.set_caption("First Game")

# loads all of the right walking art into an array to be cycled through
walkRight = [pygame.image.load('pics/R1.png'),
             pygame.image.load('pics/R2.png'),
             pygame.image.load('pics/R3.png'),
             pygame.image.load('pics/R4.png'),
             pygame.image.load('pics/R5.png'),
             pygame.image.load('pics/R6.png'),
             pygame.image.load('pics/R7.png'),
             pygame.image.load('pics/R8.png'),
             pygame.image.load('pics/R9.png')]

# does the same thing for the left walking art
walkLeft = [pygame.image.load('pics/L1.png'),
            pygame.image.load('pics/L2.png'),
            pygame.image.load('pics/L3.png'),
            pygame.image.load('pics/L4.png'),
            pygame.image.load('pics/L5.png'),
            pygame.image.load('pics/L6.png'),
            pygame.image.load('pics/L7.png'),
            pygame.image.load('pics/L8.png'),
            pygame.image.load('pics/L9.png')]

bg = pygame.image.load('pics/bg.jpg')          # background image
char = pygame.image.load('pics/standing.png')  # idle image

# sets a clock and the FPS
clock = pygame.time.Clock()
FPS = 27

# change the 'gravity' by changing the number of frames
jumpFrames = 9


# class not necisarry but makes it cleaner for when we add more things
class player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = 5
        self.isJump = False
        self.jumpCount = jumpFrames
        self.left = True
        self.right = False
        self.walkCount = 0
        self.staning = True
        # self.sprint = False

    # Does the drawing for the character here to clean up redrawGameWindow
    def draw(self, win):
        # ******FIXME***********************#
        # supposed to work for if im walking or sprinting
        # if sprint:
        #     frameCount = walkCount // 2
        # else:
        #     frameCount = walkCount // 4
        # if walkCount + 1 >= 36 and not sprint:
        #     walkCount = 0
        # elif walkCount + 1 >= 18 and sprint:
        #     walkCount = 0

        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            # displays each image for 3 frames for a total of 27 FPS
            frameCount = self.walkCount // 3
            if self.left:
                if man.isJump:
                    win.blit(walkLeft[frameCount], (self.x, self.y))
                else:
                    win.blit(walkLeft[frameCount], (self.x, self.y))
                    self.walkCount += 1
            elif self.right:
                if man.isJump:
                    win.blit(walkRight[frameCount], (self.x, self.y))
                else:
                    win.blit(walkRight[frameCount], (self.x, self.y))
                    self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


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
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0


# redraws the window after every frame
def redrawGameWindow():

    win.blit(bg, (0, 0))  # uses the picture stored in bg as the background
    man.draw(win)
    zombie.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# gun information
magSize = 10
bullets = []
bulletBuffer = 6
bufferCount = 0
prevPress = False

# main loop
man = player(W/2, 400, 64, 64)
zombie = enemy(W/4, 410, 64, 64, 3*W/4)
run = True
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

    # stored a dict of ALL keyboard keys and whether they are being pressed
    keys = pygame.key.get_pressed()

    # quits if ESC is pressed
    if keys[pygame.K_ESCAPE]:
        run = False

    # ***********FIXME********************************#
    # # sets movement speed to spring if LSHIFT is pressed
    # if keys[pygame.K_LSHIFT]:
    #     sprint = True
    #     vel = 10
    # else:
    #     sprint = False
    #     vel = 5

    # allows you to fire bullets (they dont clump any more)
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
                bullet = projectile(Bx, By, 4, black, f)
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

    # # allows to warp to ther other end of the screen
    # if man.x < -(3*man.w/4):
    #     man.x = W - man.w/4
    # elif man.x > W:
    #     man.x = -(3*man.w/4)

    # jumping algorithim, needs improvemnt to parabolic in my oppinion
    if not (man.isJump):
        if keys[pygame.K_w]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -jumpFrames:
            if man.jumpCount >= 0:
                man.y -= ((man.jumpCount)**2) * 0.5
                man.jumpCount -= 1
            else:
                man.y += ((man.jumpCount)**2) * 0.5
                man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = jumpFrames

    redrawGameWindow()

pygame.quit()
