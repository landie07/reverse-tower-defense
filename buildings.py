from math import sin, cos, pi
import pygame

class Building:
    def tick(self):
        pass

    def draw(self, screen):
        pass

wall_thickness = 5
wall_width = 50
wall_color = 0xaaaaaa
wall_hp = 100
class Wall(Building):
    # let op met rotation want positieve y-as gaat naar beneden
    def __init__(self, x: float, y: float, rotation: float):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.hp = wall_hp

    def draw(self, screen):
        start = (self.x - wall_width * cos(self.rotation) / 2, self.y - wall_width * sin(self.rotation) / 2)
        end = (self.x + wall_width * cos(self.rotation) / 2, self.y + wall_width * sin(self.rotation) / 2)

        pygame.draw.line(screen, wall_color, start, end, width=wall_thickness)

tower_hp = 100
class Tower(Building):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hp = tower_hp

landmine_hp = 100
class Landmine(Building):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hp = landmine_hp

def _test():
    screen_width = 500
    screen_height = 500

    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    clock = pygame.time.Clock()

    wall = Wall(250, 250, 0)

    running = True
    dt = 0
    frames = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('0x181818')

        wall.draw(screen)
        x, y, rot = wall.x, wall.y, wall.rotation
        if frames > 60:
            wall = Wall(x, y, rot - 2 * pi * dt / 1000)
        frames += 1

        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()
