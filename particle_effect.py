import pygame
from math import sqrt

effects = []

def create(x, y, duration, radius, color):
    effect = _Particle_Effect(x, y, duration, radius, color)
    effects.append(effect)

def draw(screen, tile_size):
    to_remove = []
    for i, effect in enumerate(effects):
        effect.draw(screen, tile_size)
        effect.duration -= 1
        if effect.duration <= 0:
            to_remove.append(i)

    for i in to_remove[::-1]:
        del effects[i]

class _Particle_Effect:
    # duration in frames
    def __init__(self, x, y, duration, radius, color):
        self.x = x
        self.y = y
        self.duration = duration
        self.radius = radius
        self.color = color

    def draw(self, screen, tile_size):
        x = self.x * tile_size + tile_size // 2 - self.radius
        y = self.y * tile_size + tile_size // 2 - self.radius
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, self.color, (self.radius, self.radius), self.radius)
        screen.blit(s, (x, y))
