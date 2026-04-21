import pygame
import buildings
import troops
from math import sqrt

class Arrow:
    color = 0xD81111

    # snelheid in tiles/tick
    def __init__(self, x, y, target, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.target_reached = False

    def tick(self, grid):
        if self.target == None or not self.target.alive:
            self.target_reached = True
            return

        if isinstance(self.target, troops.troop):
            t_x, t_y = self.target.troop_coordinates
        elif isinstance(self.target, buildings.Building):
            t_x = self.target.x
            t_y = self.target.y

        direction_x = t_x - self.x
        direction_y = t_y - self.y

        distance = sqrt(direction_x ** 2 + direction_y ** 2) 

        if distance <= self.speed:
            if isinstance(self.target, troops.troop):
                self.target.take_damage(self.damage, grid)
            elif isinstance(self.target, buildings.Building):
                self.target.damage(self.damage, grid)

            self.target_reached = True
            return

        direction_x /= distance
        direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def draw(self, screen, tile_size):
        centre_x = self.x * tile_size + tile_size // 2
        centre_y = self.y * tile_size + tile_size // 2
        radius = 5
        pygame.draw.circle(screen, self.color, (centre_x, centre_y), radius)
