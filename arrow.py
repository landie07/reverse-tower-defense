import pygame
import buildings
import troops
from math import sqrt

arrows = []

def create_arrow(x, y, target, speed, damage):
    arrow = _Arrow(x, y, target, speed, damage)
    arrows.append(arrow)

def tick_arrows(grid):
    to_remove = []
    for i, arrow in enumerate(arrows):
        arrow.tick(grid)
        if arrow.target_reached:
            to_remove.append(i)

    for i in to_remove[::-1]:
        del arrows[i]

def draw_arrows(screen, tile_size):
    for arrow in arrows:
        arrow.draw(screen, tile_size)

class _Arrow:
    color = 0x808080

    # snelheid in tiles/tick
    def __init__(self, x, y, target, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.target_reached = False

    # returns (dx, dy), distance
    def direction(self) -> (tuple[float], float):
        if isinstance(self.target, troops.troop):
            t_x, t_y = self.target.troop_coordinates
        elif isinstance(self.target, buildings.Building):
            t_x = self.target.x
            t_y = self.target.y

        direction_x = t_x - self.x
        direction_y = t_y - self.y

        distance = sqrt(direction_x ** 2 + direction_y ** 2) 

        direction_x /= distance
        direction_y /= distance

        return (direction_x, direction_y), distance

    def tick(self, grid):
        if self.target == None or not self.target.alive:
            self.target_reached = True
            return

        (direction_x, direction_y), distance = self.direction()

        if distance <= self.speed:
            if isinstance(self.target, troops.troop):
                self.target.take_damage(self.damage, grid)
            elif isinstance(self.target, buildings.Building):
                self.target.damage(self.damage, grid)

            self.target_reached = True
            return

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def draw(self, screen, tile_size):
        width = 2
        length = 6

        ax = self.x * tile_size + tile_size // 2
        ay = self.y * tile_size + tile_size // 2

        (dx, dy), _ = self.direction()

        bx = int(ax + dx*length)
        by = int(ay + dy*length)

        pygame.draw.line(screen, self.color, (ax, ay), (bx, by), width=width)
