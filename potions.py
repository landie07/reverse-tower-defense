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
        self.circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA)

    
    def locate_objects(self, object_list):
        objects_in_potionrange = []
        for object in object_list:
            if isinstance(object, buildings.Building):
                distance = math.sqrt((object.x - self.coordinates[0])**2 + (object.y - self.coordinates[1])**2)
                if distance < self.range:
                    print(object)
                    print("azeuojeraar")
                    objects_in_potionrange.append(object)
            if isinstance(object, troops.troop):
                distance = math.sqrt((object.troop_coordinates[0] - self.coordinates[0])**2 + (object.troop_coordinates[1] - self.coordinates[1])**2)
                if distance < self.range:
                    print(object)
                    objects_in_potionrange.append(object)
        return objects_in_potionrange

class health_potion(potion):
    def __init__(self, cost, duration, range, coordinates, screen):
        super().__init__(cost, duration, range, coordinates)
        self.healing_amount = 5
        self.screen = screen

    def draw_potion(self, screen, grid_size):
        pygame.draw.circle(self.circle_surface, (0, 255, 0, 50), (100, 100), 100)
        screen.blit(self.circle_surface, (self.coordinates[0]*grid_size - 100, self.coordinates[1]*grid_size - 100))

    def effect(self, object_list, grid, screen):
        objects = potion.locate_objects(self, object_list)
        for object in objects:
            print("er loopt iets mis met het damage nemen")
            object.take_damage(-self.healing_amount, grid) #negatieve damage doen is hetzelfde als healen

class damage_potion(potion):
    def __init__(self, cost, duration, range, coordinates, screen):
        super().__init__(cost, duration, range, coordinates)
        self.damage_amount = 5
        self.screen = screen

    def draw_potion(self, screen, grid_size):
        pygame.draw.circle(self.circle_surface, (255, 0, 0, 50), (100, 100), 100)
        screen.blit(self.circle_surface, (self.coordinates[0]*grid_size - 100, self.coordinates[1]*grid_size - 100))
    
    def effect(self, object_list, grid, screen):
        objects = potion.locate_objects(self, object_list)
        for object in objects:
            object.damage(self.damage_amount, grid)




