from math import sin, cos, pi, sqrt
import pygame

class Building:
    def tick(self):
        pass

    def draw(self, screen):
        pass

wall_thickness = 5
wall_width = 50
wall_color = 0xaaaaaa
wall_hp = 200
class Wall(Building):
    # let op met rotation want positieve y-as gaat naar beneden
    def __init__(self, x: float, y: float, rotation_angle: float):
        self.x = x
        self.y = y
        self.rotation = rotation_angle
        self.hp = wall_hp

    def tick(self):
        pass

    def draw(self, screen):
        start = (self.x - wall_width * cos(self.rotation) / 2, self.y - wall_width * sin(self.rotation) / 2)
        end   = (self.x + wall_width * cos(self.rotation) / 2, self.y + wall_width * sin(self.rotation) / 2)

        pygame.draw.line(screen, wall_color, start, end, width=wall_thickness)

tower_hp = 100
tower_range = 4
tower_shot_cooldown = 60
tower_radius = 50
tower_color = 0x99550C
class Tower(Building):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hp = tower_hp
        self.target = None
        self.shot_cooldown = tower_shot_cooldown

    def tick(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            return

        self.shot_cooldown = tower_shot_cooldown
        troops = [] # TODO
        self.find_target(troops)
        # shoot at target

        

    def find_target(self, troops: list):
        if self.target != None:
            dst = sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
            if dst <= tower_range:
                return

            self.target = None

        nearest_dst = float("+inf")
        nearest_idx = -1

        for i, troop in enumerate(troops):
            dst = sqrt((self.x - troop.x) ** 2 + (self.y - troop.y) ** 2)
            if dst < nearest_dst:
                nearest_dst = dst
                nearest_idx = i

        if nearest_idx < 0 or nearest_dst > tower_range:
            return

        self.target = troops[nearest_idx]


    def draw(self, screen):
        pygame.draw.circle(screen, tower_color, (self.x, self.y), tower_radius)

landmine_hp = 1
landmine_draw_radius = 25
landmine_activation_radius = 1
landmine_damage_radius = 2
landmine_color = 0x6E7A07
class Landmine(Building):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hp = landmine_hp

    def tick(self):
        troops = [] # TODO

        explode = False

        for i, troop in enumerate(troops):
            dst = sqrt((self.x - troop.x) ** 2 + (self.y - troop.y) ** 2)
            if dst < landmine_activation_radius:
                explode = True
                break

        if not explode:
            return

        for troop in troops:
            dst = sqrt((self.x - troop.x) ** 2 + (self.y - troop.y) ** 2)
            if dst < landmine_damage_radius:
                # troop.damage()

        self.hp = 0

    def draw(self, screen):
        pygame.draw.circle(screen, landmine_color, (self.x, self.y), landmine_draw_radius)

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
