import queue
import pygame
import buildings

class troop:
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple):
        self.alive = True
        self.health = health
        self.speed = speed
        self.attack_damage = attack_damage
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_size = troop_size
        self.troop_coordinates = troop_coordinates

    def draw_troop(self, screen, rgb_color: tuple, troop_coordinates: tuple, radius: int, alive: bool): #rgb color moet een 3delige tuple zijn.
        if self.alive:
            pygame.draw.circle(screen, rgb_color, troop_coordinates, self.troop_size)

    def find_nearest_building(self, buildings: list, troop_coordinates: tuple): #idris, sava: troop_coordinates is een tuple!
        x_coordinate_of_nearest_building = 2 + self.x_grid_size * 2 
        y_coordinate_of_nearest_building = 2 + self.y_grid_size * 2
        x_troop_coordinate, y_troop_coordinate = troop_coordinates
        for building in buildings:
            building_x_coordinate, building_y_coordinate = building.coordinates #idris, voeg aan je gebouwclass een property toe voor de coordinaten van het gebouw als tuple 
            if abs(building_x_coordinate - x_troop_coordinate) < x_coordinate_of_nearest_building:
                if abs(building_y_coordinate - y_troop_coordinate) < y_coordinate_of_nearest_building:
                    x_coordinate_of_nearest_building = building_x_coordinate
                    y_coordinate_of_nearest_building = building_y_coordinate
        coordinates_of_nearest_building = (x_coordinate_of_nearest_building, y_coordinate_of_nearest_building)
        return coordinates_of_nearest_building
    
    #deze functie zoekt een pad van de huidige positie naar de positie bepaald in de find_nearest_building() functie.
    def find_path(self, troop_coordinates: tuple, coordinates_of_nearest_building: tuple, grid, visited_locations): #sava, grid system moet een geneste lijst zijn met waarden voor wat er op iedere pixel staat, een 0 voor leeg, een 1 voor een troep, een 2 voor een gebouw
        instructions = []
        fifo = queue.Queue()
        path = [troop_coordinates]
        fifo.put(troop_coordinates)
        print(troop_coordinates)
        while fifo.empty() != True:
            troop_coordinates = fifo.get()
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for direction in directions:
                if visited_locations.count((troop_coordinates[0] + direction[0], troop_coordinates[1] + direction[1])) == 0:
                    if troop_coordinates[1] + direction[1] < self.x_grid_size and troop_coordinates[1] + direction[1] > 0:  #binnen breedte (x) dimenties van de grid
                        if troop_coordinates[0] + direction[0] < self.y_grid_size and troop_coordinates[0] + direction[0] > 0:   #binnen hoogte (y) dimenties van de grid
                            if grid[troop_coordinates[0] + direction[0], troop_coordinates[1] + direction[1]] == 0: #als de plaats waar je naar wilt verplaatsen leeg is
                                x_coordinate, y_coordinate = troop_coordinates
                                x_direction, y_direction = direction
                                instructions.append((x_direction, y_direction))
                                new_coordinates = (x_coordinate + x_direction, y_coordinate + y_direction)
                                print(new_coordinates)
                                if new_coordinates == coordinates_of_nearest_building:
                                    return visited_locations, path
                                else:
                                    visited_locations.append(new_coordinates)
                                    fifo.put(new_coordinates)
                
        visited_locations.append(coordinates_of_nearest_building)
        return visited_locations, instructions
            
    """def move_2(self, troop_coordinates, building, grid_system):
        try:
            coordinates_of_nearest_building = (building.x, building.y)
            path, instructions = self.find_path(troop_coordinates, coordinates_of_nearest_building, grid_system)
            instruction = instructions.pop(0)
            troop_coordinates = (troop_coordinates[0] + instruction[0],troop_coordinates[1] + instruction[1])
            return troop_coordinates
        except IndexError:
            troop_coordinates = (troop_coordinates[0], troop_coordinates[1])
            self.die()
            return troop_coordinates"""
        
    def move(self, troop_coordinates, path):
        if len(path) >= 1:
            instruction = path.pop(0)
            print(instruction)
            troop_coordinates = (troop_coordinates[0] + instruction[0], troop_coordinates[1] + instruction[1]) 
        else:
            self.attack(self.attack_damage)
        return troop_coordinates
    
    def check_for_collision():
        print("PLACEHOLDER")
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    
    def attack(self, building: buildings.Building):
        building.damage(building.hp)

    def die(self):
        self.alive = False    
        print("dood")

class terrorist(troop):
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple):
        self.alive = True
        self.health = 1
        self.speed = 5
        self.attack_damage = 30
        self.troop_size = 3
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_coordinates = troop_coordinates

    def move(self, troop_coordinates, path, building):
        if len(path) >= 1:
            instruction = path.pop(0)
            print(instruction)
            troop_coordinates = (troop_coordinates[0] + instruction[0], troop_coordinates[1] + instruction[1]) 
        else:
            self.die()
            self.attack(building)
            del self
        return troop_coordinates
    
class big_troop(troop):
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple):
        self.alive = True
        self.health = 50
        self.speed = 1
        self.attack_damage = 20
        self.troop_size = 10
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_coordinates = troop_coordinates

class small_troop(troop):
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple):
        self.alive = True
        self.health = 15
        self.speed = 4
        self.attack_damage = 5
        self.troop_size = 4
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_coordinates = troop_coordinates
