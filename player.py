import pygame
from hitboxclass import HitBox


# class for the player character
class Player(object):
    def __init__(self, x, y, w, h):
        # x and y are for positon, w and h are for size
        self.x, self.y, self.w, self.h = x, y, w, h
        # vel: Velocity, the Player's movement speed, the number of pixels he move when walking/running.
        self.vel = 5
        self.isJump = False
        self.jumpFrames = 9
        self.jumpCount = self.jumpFrames
        self.left = True
        self.right = False
        self.walkCount = 0
        self.maxHP = 5
        self.HP = self.maxHP
        self.vulnerable = True
        self.invincibleFrames = 5
        self.standing = True
        self.hitbox = HitBox(self.x + 20, self.y, 28, 60)  # (x,y,w,h)
        self.walkRight = [pygame.image.load('pics/R1.png'),
                          pygame.image.load('pics/R2.png'),
                          pygame.image.load('pics/R3.png'),
                          pygame.image.load('pics/R4.png'),
                          pygame.image.load('pics/R5.png'),
                          pygame.image.load('pics/R6.png'),
                          pygame.image.load('pics/R7.png'),
                          pygame.image.load('pics/R8.png'),
                          pygame.image.load('pics/R9.png')]
        self.walkLeft = [pygame.image.load('pics/L1.png'),
                         pygame.image.load('pics/L2.png'),
                         pygame.image.load('pics/L3.png'),
                         pygame.image.load('pics/L4.png'),
                         pygame.image.load('pics/L5.png'),
                         pygame.image.load('pics/L6.png'),
                         pygame.image.load('pics/L7.png'),
                         pygame.image.load('pics/L8.png'),
                         pygame.image.load('pics/L9.png')]
        self.Hbar = [pygame.image.load('pics/hb1.png'),
                     pygame.image.load('pics/hb12.png'),
                     pygame.image.load('pics/hb13.png'),
                     pygame.image.load('pics/hb14.png'),
                     pygame.image.load('pics/hb1empty.png')]

    # Does the drawing for the character here to clean up redrawGameWindow
    def draw(self, win):

        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            # displays each image for 3 frames for a total of 27 FPS
            frameCount = self.walkCount // 3
            if self.left:
                if self.isJump:
                    win.blit(self.walkLeft[frameCount], (self.x, self.y))
                else:
                    win.blit(self.walkLeft[frameCount], (self.x, self.y))
                    self.walkCount += 1
            elif self.right:
                if self.isJump:
                    win.blit(self.walkRight[frameCount], (self.x, self.y))
                else:
                    win.blit(self.walkRight[frameCount], (self.x, self.y))
                    self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))
        self.hitbox = HitBox(self.x + 20, self.y, 28, 60)  # redraws the hitbox
