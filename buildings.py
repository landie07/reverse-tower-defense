from math import sin, cos, pi, sqrt
import pygame

class Building:
    destruction_reward = 0
    def tick(self, grid, alive_troops):
        pass

    def draw(self, screen, tile_size):
        pass

    @property
    def coordinates(self) -> tuple[int]:
        return (self.x, self.y)

    def damage(self, hp, grid) -> bool:
        self.hp -= hp
        if self.hp > 0:
            return False

        if not (self is grid[self.y][self.x]):
            print("probleem")
        grid[self.y][self.x] = None
        return True

class Wall(Building):
    color = 0xffffff
    hp_max = 200
    destruction_reward = 2

    # let op met rotation want positieve y-as gaat naar beneden
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = self.hp_max

    def draw(self, screen, tile_size):
        screen_x = self.x * tile_size
        screen_y = self.y * tile_size
        # misschien in de toekomst kijken naar naburige gebouwen zodat muren kunnen verbinden
        padding = 10

        rect = pygame.Rect(
                screen_x + padding,
                screen_y + padding,
                tile_size - 2*padding,
                tile_size - 2*padding,
                )

        pygame.draw.rect(screen, self.color, rect)

class Tower(Building):
    hp_max = 100
    range = 4
    damage_hp = 5
    shot_cooldown_max = 60
    color = 0x99550C
    destruction_reward = 5

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = self.hp_max
        self.target = None
        self.shot_cooldown = self.shot_cooldown_max

    def tick(self, grid, alive_troops):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            return

        self.shot_cooldown = self.shot_cooldown_max

        self.find_target(alive_troops)

        if self.target != None:
            self.target.take_damage(self.damage_hp)

    def find_target(self, alive_troops: list):
        if self.target != None and self.target.alive:
            target_x, target_y = self.target.troop_coordinates
            dst = sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2)
            if dst <= self.range:
                return

        self.target = None
        nearest_dst = float("+inf")

        for i, troop in enumerate(alive_troops):
            troop_x, troop_y = troop.troop_coordinates
            dst = sqrt((self.x - troop_x) ** 2 + (self.y - troop_y) ** 2)
            if dst < nearest_dst:
                nearest_dst = dst
                self.target = troop

        if nearest_dst > self.range:
            self.target = None

    def draw(self, screen, tile_size):
        centre_x = self.x * tile_size + tile_size // 2
        centre_y = self.y * tile_size + tile_size // 2
        radius = tile_size - 5
        pygame.draw.circle(screen, self.color, (centre_x, centre_y), tile_size // 2)

class Landmine(Building):
    hp_max = 1
    activation_radius = 2
    damage_radius = 2
    color = 0x6E7A07
    damage_hp = 20
    destruction_reward = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = self.hp_max

    def tick(self, grid, alive_troops):
        explode = False

        for troop in alive_troops:
            troop_x, troop_y = troop.troop_coordinates
            dst = sqrt((self.x - troop_x) ** 2 + (self.y - troop_y) ** 2)
            if dst < self.activation_radius:
                explode = True
                break

        if not explode:
            return

        for troop in alive_troops:
            troop_x, troop_y = troop.troop_coordinates
            dst = sqrt((self.x - troop_x) ** 2 + (self.y - troop_y) ** 2)
            if dst < self.damage_radius:
                troop.take_damage(self.damage_hp)

        self.damage(self.hp, grid)

    def draw(self, screen, tile_size):
        centre_x = self.x * tile_size + tile_size // 2
        centre_y = self.y * tile_size + tile_size // 2
        radius = tile_size - 5
        pygame.draw.circle(screen, self.color, (centre_x, centre_y), tile_size // 2)
