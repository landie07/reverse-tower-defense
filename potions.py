import queue
import buildings
import pygame
import arrow
import troops
import math

class potion:
    def __init__(self, cost, duration, range, coordinates):
        self.cost = cost
        self.duration = duration
        self.range = range
        self.coordinates = coordinates
    

    def draw_potion(self, screen):
        circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (255, 0, 0, 128), (100, 100), 100)
        screen.blit(circle_surface, (100, 100))

    def locate_objects(self, object_list):
        objects_in_potionrange = []
        for object in object_list:
            if isinstance(object, buildings.Building):
                distance = math.sqrt((object.x - self.coordinates[0])**2 + (object.y - self.coordinates[1])**2)
                if distance < self.range:
                    print(object)
                    objects_in_potionrange.append(object)
            if isinstance(object, troops.troop):
                distance = math.sqrt((object.troop_coordinates[0] - self.coordinates[0])**2 + (object.troop_coordinates[1] - self.coordinates[1])**2)
                if distance < self.range:
                    print(object)
                    objects_in_potionrange.append(object)
        return objects_in_potionrange
    
    def effect(self, object_list, grid, screen):
        objects = potion.locate_objects(self, screen, object_list)
        if isinstance(self, health_potion):
            for object in objects:
                object.damage(-self.healing_amount, grid) #negatieve damage doen is hetzelfde als healen
        if isinstance(self, damage_potion):
            for object in objects:
                object.damage(self.damage_amount, grid)

class health_potion(potion):
    def __init__(self, cost, duration, range, coordinates, screen):
        super().__init__(cost, duration, range, coordinates)
        self.healing_amount = 5
        self.screen = screen

    def heal(self, object_list, grid, screen):
        objects = potion.locate_objects(self, screen, object_list)
        for object in objects:
            object.damage(-self.healing_amount, grid) #negatieve damage doen is hetzelfde als healen

class damage_potion(potion):
    def __init__(self, cost, duration, range, coordinates, screen):
        super().__init__(cost, duration, range, coordinates)
        self.damage_amount = 5
        self.screen = screen

    def damage(self, object_list, grid, screen):
        objects = potion.locate_objects(self, screen, object_list)
        for object in objects:
            object.damage(self.damage_amount, grid)



"""
TODO POTIONS
healing potion


damage potion
kleinere range dan healing
doet veel damage

optioneel:speed potion

"""
