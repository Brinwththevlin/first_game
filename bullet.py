import pygame
pygame.init()

W = 500
H = 480
win = pygame.display.set_mode((W, H))  # , pygame.RESIZABLE)
pygame.display.set_caption("ball hit box")
win.fill([255, 255, 255])


class projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.hitbox = (self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


black = [0, 0, 0]
bullet = projectile(200, 200, 30, black)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    bullet.draw(win)
    pygame.display.update()

pygame.quit()
