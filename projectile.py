import pygame
from hitboxclass import HitBox


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x, self.y = x, y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing  # vel = velocity/ the number of pixels to moves.
        self.hitbox = HitBox(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        self.hitbox = HitBox(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)
