import queue
import pygame
import buildings
import math
import settings as settings_file

settings = settings_file.settings()

class troop:
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: int, troop_coordinates: tuple, grid_tile_size:int):
        self.alive = True
        self.health = health
        self.speed = speed
        self.attack_damage = attack_damage
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_size = troop_size
        self.troop_coordinates = troop_coordinates
        self.grid_tile_size = grid_tile_size
        self.instructions = None
        self.collision = False
        self.at_target = False

    def find_nearest_building(self, buildings: list): #idris, sava: troop_coordinates is een tuple!
        x_coordinate_of_nearest_building = 2 + self.x_grid_size * 2 
        y_coordinate_of_nearest_building = 2 + self.y_grid_size * 2
        x_distance_of_nearest_building = 2 + self.x_grid_size * 2 
        y_distance_of_nearest_building = 2 + self.y_grid_size * 2
        distance_of_nearest_building = math.sqrt(x_distance_of_nearest_building**2 + y_distance_of_nearest_building**2)
        x_troop_coordinate, y_troop_coordinate = self.troop_coordinates
        for building in buildings:
            building_x_coordinate, building_y_coordinate = building.coordinates #idris, voeg aan je gebouwclass een property toe voor de coordinaten van het gebouw als tuple 
            if (building_x_coordinate - x_troop_coordinate)**2 + (building_y_coordinate - y_troop_coordinate) **2 < distance_of_nearest_building ** 2:
                x_coordinate_of_nearest_building = building_x_coordinate
                y_coordinate_of_nearest_building = building_y_coordinate
                x_distance_of_nearest_building = abs(building_x_coordinate - x_troop_coordinate)
                y_distance_of_nearest_building = abs(building_y_coordinate - y_troop_coordinate)
                distance_of_nearest_building = math.sqrt(x_distance_of_nearest_building**2 + y_distance_of_nearest_building**2)
        coordinates_of_nearest_building = (x_coordinate_of_nearest_building, y_coordinate_of_nearest_building)
        return coordinates_of_nearest_building
    
    def find_path(self, grid, visited_locations):

        fifo = queue.Queue()
        fifo.put(self.troop_coordinates)

        came_from = {}
        came_from[self.troop_coordinates] = None

        visited = set()
        visited.add(self.troop_coordinates)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while not fifo.empty():
            current = fifo.get()

            if isinstance(grid[current[0]][current[1]], buildings.Building):

                # pad reconstrueren (coördinaten)
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]

                path.reverse()

                # omzetten naar instructions (dx, dy)
                instructions = []
                for i in range(len(path) - 1):
                    dx = path[i+1][0] - path[i][0]
                    dy = path[i+1][1] - path[i][1]
                    instructions.append((dx, dy))
                print(instructions)
                self.instructions = instructions
                del instructions[-1]
                return visited_locations, instructions

            for direction in directions:
                new_x = current[0] + direction[0]
                new_y = current[1] + direction[1]
                new_coordinates = (new_x, new_y)

                if new_coordinates not in visited:
                    if 0 <= new_x < self.y_grid_size and 0 <= new_y < self.x_grid_size:
                        cell = grid[new_x][new_y]
                        if cell == None or isinstance(cell, buildings.Building):
                            fifo.put(new_coordinates)
                            visited.add(new_coordinates)
                            came_from[new_coordinates] = current

                            visited_locations.append(new_coordinates)

        return visited_locations, []
    
    def go_to_building(self, grid, visited_locations):
        fifo = queue.Queue()
        fifo.put(self.troop_coordinates)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        visited = set()
        visited.add(self.troop_coordinates)

        came_from = {}
        came_from[self.troop_coordinates] = None

        while not fifo.empty():
            current = fifo.get()
            if isinstance(grid[current[0]][current[1]], buildings.Building):

                # pad reconstrueren (coördinaten)
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]

                path.reverse()

                # omzetten naar instructions (dx, dy)
                instructions = []
                for i in range(len(path) - 1):
                    dx = path[i+1][0] - path[i][0]
                    dy = path[i+1][1] - path[i][1]
                    instructions.append((dx, dy))
                print("instructies")
                print(instructions)
                return visited_locations, instructions

            for direction in directions:
                new_coordinates = (self.troop_coordinates[0] + direction[0], self.troop_coordinates[1] + direction[1])
                fifo.put(new_coordinates)

                if new_coordinates not in visited:
                    if 0 <= self.troop_coordinates[0] + direction[0] < self.y_grid_size and 0 <= self.troop_coordinates[1] + direction[1] < self.x_grid_size:
                        if grid[self.troop_coordinates[0] + direction[0]][self.troop_coordinates[1] + direction[1]] == None:
                            fifo.put(new_coordinates)
                            visited.add(new_coordinates)
                            came_from[new_coordinates] = current

                            visited_locations.append(new_coordinates)
        return visited_locations, []
      
    def move(self, path, building, grid):
        if len(path) >= 1:
            instruction = path.pop(0)
            print(instruction)
            self.troop_coordinates = (self.troop_coordinates[0] + instruction[0], self.troop_coordinates[1] + instruction[1]) 
        else:
            self.at_target = True
        return self.troop_coordinates
    
    def check_for_collision(self, grid):
        x, y = self.troop_coordinates

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            # bounds check
            if 0 <= nx < self.x_grid_size and 0 <= ny < self.y_grid_size:
                cell = grid[nx][ny]

                if cell is not None:
                    return True, cell

        return False, None

 

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    
    def attack(self, building, grid):
        building.damage(self.attack_damage, grid)

    def die(self, grid):
        self.alive = False 
        print(self.alive)  
        print("troep gestorven") 
        self.remove_object(grid)

    def remove_object(self, grid):
        grid[self.troop_coordinates[0]][self.troop_coordinates[1]] = None



    """ def check_for_collision2(self, grid):  #LANDER BIJ COLLISION MOGEN ER GEEN 2 OBJECTEN IN DEZELFDE TILE ZITTEN !!!!!!!!!!!!!!!!!!!!!!!!!!
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            if grid[self.troop_coordinates[0] + direction[0]][self.troop_coordinates[1] + direction[1]] != None:
                if isinstance(grid[self.troop_coordinates[0] + direction[0]][self.troop_coordinates[1] + direction[1]], buildings.Building):
                    print(grid[self.troop_coordinates[0] + direction[0]][self.troop_coordinates[1] + direction[1]])
                    return True, grid[self.troop_coordinates[0] + direction[0]][self.troop_coordinates[1] + direction[1]]
            else:
                return False, None """    

    """
     def find_path(self, coordinates_of_nearest_building: tuple, grid, visited_locations):
    #     print(grid)
    #     instructions = []
    #     fifo = queue.Queue()
    #     fifo.put(self.troop_coordinates)

    #     visited = set()
    #     visited.add(self.troop_coordinates)

    #     came_from = {}
    #     came_from[self.troop_coordinates] = None

    #     while fifo.empty() != True:
    #         huidige_toestand = fifo.get()
    #         directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    #         for richting in directions:
    #             x = huidige_toestand[0] + richting[0]
    #             y = huidige_toestand[1] + richting[1]
    #             if 0 <= x < self.x_grid_size and 0 <= y < self.y_grid_size:
    #                 if grid[y][x] == 0:
    #                     nieuwe_toestand = (x, y)
    #                     if nieuwe_toestand not in visited:
    #                         visited.add(nieuwe_toestand)
    #                         fifo.put(nieuwe_toestand)
    #                         came_from[nieuwe_toestand] = huidige_toestand
    #                         if nieuwe_toestand == coordinates_of_nearest_building:
    #                             path = []
    #                             current = nieuwe_toestand
    #                             while current != self.troop_coordinates:
    #                                 prev = came_from[current]
    #                                 dx = current[0] - prev[0]
    #                                 dy = current[1] - prev[1]
    #                                 path.append((dx, dy))
    #                                 current = prev
    #                             path.reverse()
    #                             instructions = path.copy()
    #                             print("tag 1")
    #                             print(instructions)
    #                             return path, instructions
    #     return [], []
    """

    """
    #deze functie zoekt een pad van de huidige positie naar de positie bepaald in de find_nearest_building() functie.  
    def find_path2(self, coordinates_of_nearest_building: tuple, grid, visited_locations): #sava, grid system moet een geneste lijst zijn met waarden voor wat er op iedere pixel staat, een 0 voor leeg, een 1 voor een troep, een 2 voor een gebouw
        instructions = []
        fifo = queue.Queue()
        #path = [self.troop_coordinates]
        fifo.put(self.troop_coordinates)
        print(self.troop_coordinates)
        while fifo.empty() != True:
            self.troop_coordinates = fifo.get()
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for direction in directions:
                if visited_locations.count((self.troop_coordinates[0] + direction[0], self.troop_coordinates[1] + direction[1])) == 0:
                    if self.troop_coordinates[1] + direction[1] < self.x_grid_size and self.troop_coordinates[1] + direction[1] >= 0:  #binnen breedte (x) dimenties van de grid
                        if self.troop_coordinates[0] + direction[0] < self.y_grid_size and self.troop_coordinates[0] + direction[0] >= 0:   #binnen hoogte (y) dimenties van de grid
                            if grid[self.troop_coordinates[0] + direction[0]][ self.troop_coordinates[1] + direction[1]] == 0: #als de plaats waar je naar wilt verplaatsen leeg is
                                x_coordinate, y_coordinate = self.troop_coordinates
                                x_direction, y_direction = direction
                                instructions.append((x_direction, y_direction))
                                new_coordinates = (x_coordinate + x_direction, y_coordinate + y_direction)
                                if new_coordinates == coordinates_of_nearest_building:
                                    print("oplossing gevonden")
                                    return visited_locations, instructions
                                else:
                                    visited_locations.append(new_coordinates)
                                    fifo.put(new_coordinates)
                
        visited_locations.append(coordinates_of_nearest_building)
        return visited_locations, instructions
            
    def move_2(self, troop_coordinates, building, grid_system):
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

class terrorist(troop):
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple, grid_tile_size:int):
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.alive = True
        self.health = 1
        self.speed = 5
        self.attack_damage = 30*1000
        self.troop_size = 3.5
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_coordinates = troop_coordinates
        self.grid_tile_size = grid_tile_size
        self.rgb_color = (255, 0, 0)

    def draw_troop(self, screen, rgb_color: tuple): #rgb color moet een 3delige tuple zijn.
        if self.alive:
            pygame.draw.circle(screen, self.rgb_color, (self.troop_coordinates[0] * self.grid_tile_size, self.troop_coordinates[1] * self.grid_tile_size), self.troop_size)

    """ def move(self, path, building, grid):
        if len(path) >= 1:
            instruction = path.pop(0)
            print(instruction)
            self.troop_coordinates = (self.troop_coordinates[0] + instruction[0], self.troop_coordinates[1] + instruction[1]) 
        else:
            building.damage(self.attack_damage, grid)
            self.die()
        return self.troop_coordinates"""
    
class big_troop(troop):
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple, grid_tile_size):
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.alive = True
        self.health = 50
        self.speed = 1
        self.attack_damage = 20*100
        self.troop_size = 7
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_coordinates = troop_coordinates
        self.rgb_color = (0, 255, 0)

    def draw_troop(self, screen, rgb_color: tuple): #rgb color moet een 3delige tuple zijn.
        if self.alive:
            pygame.draw.circle(screen, self.rgb_color, (self.troop_coordinates[0] * settings.grid_tile_size, self.troop_coordinates[1] * settings.grid_tile_size), self.troop_size)

class small_troop(troop):
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int, troop_size: float, troop_coordinates: tuple, grid_tile_size):
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.alive = True
        self.health = 15
        self.speed = 4
        self.attack_damage = 5*100
        self.troop_size = 2
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_coordinates = troop_coordinates
        self.rgb_color = (0, 0, 255)

    def draw_troop(self, screen, rgb_color: tuple): #rgb color moet een 3delige tuple zijn.
        if self.alive:
            pygame.draw.circle(screen, self.rgb_color, (self.troop_coordinates[0] * self.grid_tile_size, self.troop_coordinates[1] * self.grid_tile_size), self.troop_size)

