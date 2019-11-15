""" This is a very basic game buit using pygame
    The objective is to turn it into a platformer/shooter (open to suggestions).
    Main Issues:
        1) I wish to have a the ability to spirnt, but it sometimes crashes unexpcetedly;
        2) No projectile class nor shooting function (shooting animation??)
        3) No collision detection, no platforms for platforming
        4) no enemies
            i) no death animations
            ii) no health bar /health pick ups
        5) Backdropp is currently too small dont know how to resize
        6) only one screen at the moment (sidescroller? or maybe hard screen changes like in calstevainia or metroid?)
        7) I DID NOT make the sprites in use preferably we would make them or at least change the ones available
    potential improvements:
        1) life systems, how many lives do you get before a game over
        2) winning condition
        3) score system??
        4) upgrade system (if time permits)/power ups or other form of pickup (inventory?)
        5) extra mobility options (rolling/double jump/crouch)
        6) more veriety in enemy types, attributes health
        7) pause menu (level select, restart, quit to main)
        8) title screen (dificulty setting, character select, save states(level passcodes), enimey encclopedea)
        9) if the game is simple enough and time permits machine learning to teach the game to play itself (unlikely or is another project idea)
"""
import pygame  # allows for 'easy' gamedev

# initiates the pygame
pygame.init()

# initial window sizes
W = 500
H = 480

# opens a new window that is resizable named first game
win = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("First Game")

# loads all of the sprites into the file using 'pygame.image.load('img.png')'
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'),
             pygame.image.load('R3.png'), pygame.image.load('R4.png'),
             pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'),
             pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'),
            pygame.image.load('L3.png'), pygame.image.load('L4.png'),
            pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'),
            pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')          # background image
char = pygame.image.load('standing.png')  # idle image

# sets a clock and the FPS
clock = pygame.time.Clock()
FPS = 27
jumpFrames = 9


class player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = 5
        self.isJump = False
        self.jumpCount = jumpFrames
        self.left = False
        self.right = False
        self.walkCount = 0
        # self.sprint = False

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

        if self.walkCount + 1 >= FPS:
            self.walkCount = 0
        frameCount = self.walkCount // 3

        # displays each image for 3 frames for a total of 27 FPS
        if left:
            if man.isJump:
                win.blit(walkLeft[frameCount], (self.x, self.y))
            else:
                win.blit(walkLeft[frameCount], (self.x, self.y))
                self.walkCount += 1
        elif right:
            if man.isJump:
                win.blit(walkRight[frameCount], (self.x, self.y))
            else:
                win.blit(walkRight[frameCount], (self.x, self.y))
                self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))


# redraws the window after every frame
def redrawGameWindow():

    win.blit(bg, (0, 0))  # uses the picture stored in bg as the background
    man.draw(win)
    pygame.display.update()


# main loop
man = player(300, 400, 64, 64)
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
        #     win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        #     W = event.w
        #     Ht = event.h
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

    # uses arrow keys or WASD to move left and right
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        left = True
        right = False

    elif keys[pygame.K_RIGHT] and man.x < W-man.w-man.vel:
        man.x += man.vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    # jumping algorithim, needs improvemnt
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            walkCount = 0
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
