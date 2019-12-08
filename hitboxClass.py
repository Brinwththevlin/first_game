import pygame


class HitBox(object):
    def __init__(self, x, y, w, h):
        # Hitbox Position
        self.x, self.y = x, y
        # Hitbox size
        self.width, self.height = w, h
        # Hitbox rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
# A HitBox is a Rectangle that determines if an object has made contact with another object on screen such as the player, enemy, and projectiles. (Allows Collision detection)
