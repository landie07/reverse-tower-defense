import queue


class small_troop:
    alive = True
    def __init__(self, health, speed, grid_dimentions, attack_damage):
        self.health = health
        self.speed = speed
        self.attack_damage = attack_damage
        self.x_grid_size, self.y_grid_size = self.grid_dimentions

    def find_nearest_building(buildings, troop_coordinates): #idris, sava: troop_coordinates is een tuple!
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
        coordinates_of_nearest_building  =(x_coordinate_of_nearest_building, y_coordinate_of_nearest_building)
        return coordinates_of_nearest_building
    
    def find_path(self, troop_coordinates, coordinates_of_nearest_Building, grid_system): #sava, grid system moet een geneste lijst zijn
        visited_locations = []
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
                                path.append((x_direction, y_direction))
                                new_coordinates = (x_coordinate + x_direction, y_coordinate + y_direction)
                                if new_coordinates[0] == self.x_grid_size - 1 and new_coordinates[1] == self.y_grid_size - 2:
                                    print("oplossing gevonden!")
                                    return True
                                else:
                                    visited_locations.append(new_coordinates)
                                    fifo.put(new_coordinates)
    def move(x_coordinate, y_coordinate, speed, target):
        print("PLACEHOLDER")

    def take_damage(damage):
        health -= damage
        return health
    
    def attack(self, tower_health):
        tower_health -= self.attack_damage
        if tower_health <= 0:
            print("PLACEHOLDER")
            #idris, verwijder de toren functie moet hier gecald worden, jij moet die nog maken
        return tower_health
    def die(alive):
        alive = False
        #moet meer aan toegevoegd worden!
        return alive
    

