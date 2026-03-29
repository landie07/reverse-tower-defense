from math import sin, cos, pi, sqrt
import pygame

class Building:
    def tick(self):
        pass

    def draw(self, screen):
        pass

    @property
    def coordinates(self) -> tuple[float]:
        return (self.x, self.y)

    def damage(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            pass # toren deleten

class Wall(Building):
    thickness = 5
    width = 50
    color = 0xaaaaaa
    hp = 200

    # let op met rotation want positieve y-as gaat naar beneden
    def __init__(self, x: float, y: float, rotation_angle: float):
        self.x = x
        self.y = y
        self.rotation = rotation_angle
        self.hp = Wall.hp

    def tick(self):
        pass

    def draw(self, screen):
        start = (self.x - Wall.width * cos(self.rotation) / 2, self.y - Wall.width * sin(self.rotation) / 2)
        end   = (self.x + Wall.width * cos(self.rotation) / 2, self.y + Wall.width * sin(self.rotation) / 2)

        pygame.draw.line(screen, Wall.color, start, end, width=Wall.thickness)

class Tower(Building):
    hp = 100
    range = 4
    damage_hp = 5
    shot_cooldown = 60
    radius = 50
    color = 0x99550C

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hp = Tower.hp
        self.target = None
        self.shot_cooldown = Tower.shot_cooldown

    def tick(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            return

        self.shot_cooldown = Tower.shot_cooldown
        troops = [] # TODO
        self.find_target(troops)
        self.target.take_damage(Tower.damage_hp)

        

    def find_target(self, troops: list):
        if self.target != None:
            dst = sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
            if dst <= Tower.range:
                return

            self.target = None

        nearest_dst = float("+inf")
        nearest_idx = -1

        for i, troop in enumerate(troops):
            dst = sqrt((self.x - troop.x) ** 2 + (self.y - troop.y) ** 2)
            if dst < nearest_dst:
                nearest_dst = dst
                nearest_idx = i

        if nearest_idx < 0 or nearest_dst > Tower.range:
            return

        self.target = troops[nearest_idx]


    def draw(self, screen):
        pygame.draw.circle(screen, Tower.color, self.coordinates, Tower.radius)

class Landmine(Building):
    hp = 1
    draw_radius = 25
    activation_radius = 1
    damage_radius = 2
    color = 0x6E7A07
    damage_hp = 20

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hp = Landmine.hp

    def tick(self):
        troops = [] # TODO

        explode = False

        for i, troop in enumerate(troops):
            dst = sqrt((self.x - troop.x) ** 2 + (self.y - troop.y) ** 2)
            if dst < Landmine.activation_radius:
                explode = True
                break

        if not explode:
            return

        for troop in troops:
            dst = sqrt((self.x - troop.x) ** 2 + (self.y - troop.y) ** 2)
            if dst < Landmine.damage_radius:
                troop.take_damage(Landmine.damage_hp)

        self.hp = 0

    def draw(self, screen):
        pygame.draw.circle(screen, Landmine.color, self.coordinates, Landmine.draw_radius)

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
