import queue
import pygame

class small_troop:
    def __init__(self, health: int, speed : int, grid_dimentions: tuple, attack_damage: int):
        self.alive = True
        self.health = health
        self.speed = speed
        self.attack_damage = attack_damage
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions

    def draw_troop(self, screen, rgb_color: tuple, troop_coordinates: tuple, radius: int, alive: bool): #rgb color moet een 3delige tuple zijn.
        if self.alive:
            pygame.draw.circle(screen, rgb_color, troop_coordinates, 50)

    def find_nearest_building(self, buildings: list, troop_coordinates: tuple): #idris, sava: troop_coordinates is een tuple!
        nearest_building = None
        x_coordinate_of_nearest_building = None
        y_coordinate_of_nearest_building = None
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
    def find_path(self, troop_coordinates, coordinates_of_nearest_building, grid_system): #sava, grid system moet een geneste lijst zijn met waarden voor wat er op iedere pixel staat, een 0 voor leeg, een 1 voor een troep, een 2 voor een gebouw
        visited_locations = []
        instructions = []
        fifo = queue.Queue()
        path = [troop_coordinates]
        fifo.put(troop_coordinates)
        print(type(troop_coordinates))
        print(troop_coordinates)
        while fifo.empty() != True:
            troop_coordinates = fifo.get()
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for direction in directions:
                if visited_locations.count((troop_coordinates[0] + direction[0], troop_coordinates[1] + direction[1])) == 0:
                    if troop_coordinates[1] + direction[1] < 10 and troop_coordinates[1] + direction[1] > 0:
                        if troop_coordinates[0] + direction[0] < 10 and troop_coordinates[0] + direction[0] > 0:
                            if grid_system[troop_coordinates[0] + direction[0], troop_coordinates[1] + direction[1]] == 0: 
                                x_coordinate, y_coordinate = new_coordinates
                                x_direction, y_direction = direction
                                instructions.append((x_direction, y_direction))
                                new_coordinates = (x_coordinate + x_direction, y_coordinate + y_direction)
                                if new_coordinates[0] == self.x_grid_size - 1 and new_coordinates[1] == self.y_grid_size - 2:
                                    print("oplossing gevonden!")
                                    return True
                                else:
                                    visited_locations.append(new_coordinates)
                                    fifo.put(new_coordinates)
        visited_locations.append(coordinates_of_nearest_building)
        return visited_locations, instructions
            
    def move(self, troop_coordinates, speed, buildings, grid_system):
        nearest_building = (buildings, troop_coordinates)
        path, instructions = self.find_path(self, troop_coordinates, nearest_building.coordinates, grid_system)
        instruction = instructions.pop(0)
        troop_coordinates = (troop_coordinates[0] + instruction[0],troop_coordinates[1] + instruction[1])
        return troop_coordinates

    def check_for_collision():
        print("PLACEHOLDER")
        
    def take_damage(self, damage):
        self.health -= damage
    
    def attack(self, tower_health):
        tower_health -= self.attack_damage
        if tower_health <= 0:
            print("PLACEHOLDER")
            #idris, de "verwijder de toren" functie moet hier gecald worden, jij moet die nog maken
        return tower_health
    
    def die(self, alive):
        self.alive = False    


