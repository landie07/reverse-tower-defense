from math import sin, cos, pi, sqrt, ceil
import arrow
import troops
import particle_effect
import pygame

class Building:
    destruction_reward = 0
    def tick(self, grid, alive_troops):
        pass

    def draw(self, screen, tile_size):
        pass

    # tekent bar met levenspunten
    def _draw_hp(self, screen, tile_size):
        if not self.alive or self.hp >= self.hp_max:
            return

        green = 0x00FF00
        red = 0xFF0000
        padding = 4
        height = padding
        width = tile_size - 2*padding
        s = pygame.Surface((width, height))
        s.set_alpha(0x40)
        s.fill(red)
        rect = pygame.Rect(0, 0, int(self.hp / self.hp_max * width), height)
        pygame.draw.rect(s, green, rect)

        x = self.x * tile_size + padding
        y = self.y * tile_size + padding
        screen.blit(s, (x, y))

    @property
    def alive(self) -> bool:
        return self.hp > 0

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

class Visible_Building(Building):
    pass

class Wall(Visible_Building):
    color = 0x88889A
    hp_max = 200
    destruction_reward = 2
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = self.hp_max
        self.surrounding = [False, False, False, False] # right, left, top, bottom

    def tick(self, grid, alive_troops):
        for i, (dx, dy) in enumerate(self.directions):
            x = self.x + dx
            y = self.y + dy
            if 0 <= y < len(grid) and 0 <= x < len(grid[y]):
                self.surrounding[i] = isinstance(grid[y][x], Wall)

    def draw(self, screen, tile_size):
        screen_x = self.x * tile_size
        screen_y = self.y * tile_size
        padding = 8

        size = tile_size - 2*padding
        rect = pygame.Rect(
                screen_x + padding,
                screen_y + padding,
                size, size)

        pygame.draw.rect(screen, self.color, rect)

        # offsets (p = padding, s = size) getoond voor x, y equivalent
        # niet op schaal getekend
        #
        #   left
        #   |
        #   +----s----+
        #   +p/2+     |
        # +p+   |     |
        # | |   ##    |
        # | ##########
        # | ##########
        # #####WALL#####
        #   ##########
        #   ##########
        #       ##

        pixel_offset = (-padding, padding//2, size)
        for i, (dx, dy) in enumerate(self.directions):
            if not self.surrounding[i]:
                continue

            if dx == 0:
                width = size - padding
            else:
                width = padding

            if dy == 0:
                height = size - padding
            else:
                height = padding

            side_rect = pygame.Rect(
                    rect.left + pixel_offset[dx + 1],
                    rect.top + pixel_offset[dy + 1],
                    width, height)

            pygame.draw.rect(screen, self.color, side_rect)

        self._draw_hp(screen, tile_size)


class Tower(Visible_Building):
    hp_max = 100
    range = 4
    damage_hp = 5
    shot_cooldown_max = 45
    color = 0x99550C
    destruction_reward = 5
    arrow_speed = 0.5

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

        self.find_target(alive_troops)

        if self.target == None:
            return

        self.shot_cooldown = self.shot_cooldown_max

        arrow.create_arrow(self.x, self.y, self.target, self.arrow_speed, self.damage_hp)

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
        radius = tile_size // 2 - 2
        pygame.draw.circle(screen, self.color, (centre_x, centre_y), radius)

        self._draw_hp(screen, tile_size)

class Landmine(Building):
    hp_max = 1
    activation_radius = 1
    damage_radius = 2
    color = 0x6E7A07
    explode_color = pygame.Color(0xDD4511C8)
    damage_hp = 100
    destruction_reward = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = self.hp_max
        self.explode = False

    def damage(self, hp, grid) -> bool:
        if self.explode:
            dead = super().damage(hp, grid)

        self.explode = True
        return not self.alive


    def tick(self, grid, alive_troops):
        if self.explode:
            self.damage(self.hp, grid)

            for troop in alive_troops:
                troop_x, troop_y = troop.troop_coordinates
                dst = sqrt((self.x - troop_x) ** 2 + (self.y - troop_y) ** 2)
                if dst <= self.damage_radius:
                    troop.take_damage(self.damage_hp)

            return

        for troop in alive_troops:
            troop_x, troop_y = troop.troop_coordinates
            dst = sqrt((self.x - troop_x) ** 2 + (self.y - troop_y) ** 2)
            if dst <= self.activation_radius:
                self.explode = True
                break

    def draw(self, screen, tile_size):
        centre_x = self.x * tile_size + tile_size // 2
        centre_y = self.y * tile_size + tile_size // 2
        padding = 5
        radius = tile_size // 2 - padding
        if self.explode:
            particle_effect.create(self.x, self.y, 30, self.damage_radius * tile_size - 5, self.explode_color)
        pygame.draw.circle(screen, self.color, (centre_x, centre_y), radius)

        self._draw_hp(screen, tile_size)

class Very_Important_Building(Visible_Building):
    color = 0xD1DD13
    hp_max = 500
    destruction_reward = 100

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = self.hp_max

    def draw(self, screen, tile_size):
        screen_x = self.x * tile_size
        screen_y = self.y * tile_size
        padding = 4

        rect = pygame.Rect(
                screen_x + padding,
                screen_y + padding,
                tile_size - 2*padding,
                tile_size - 2*padding,
                )

        pygame.draw.rect(screen, self.color, rect)

        self._draw_hp(screen, tile_size)
