import queue
import buildings
import pygame
import arrow

class troop:
    def __init__(self, health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size):
        self.alive = True
        self.health = health
        self.speed = speed
        self.attack_damage = attack_damage
        self.grid_dimentions = grid_dimentions
        self.x_grid_size, self.y_grid_size = self.grid_dimentions
        self.troop_size = troop_size
        self.troop_coordinates = troop_coordinates
        self.grid_tile_size = grid_tile_size
        self.instructions = []
        self.at_target = False

    def find_path(self, grid, visited_locations):
        self.at_target = False
        fifo = queue.Queue()
        fifo.put(self.troop_coordinates)

        came_from = {}
        came_from[self.troop_coordinates] = None

        visited = set()
        visited.add(self.troop_coordinates)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while not fifo.empty():
            current = fifo.get()
 
            if isinstance(grid[current[1]][current[0]], buildings.Visible_Building):
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]

                path.reverse()

                instructions = []
                for i in range(len(path) - 1):
                    dx = path[i + 1][0] - path[i][0]
                    dy = path[i + 1][1] - path[i][1]
                    instructions.append((dx, dy))

                if len(instructions) > 0:
                    instructions.pop()

                self.instructions = instructions[:]
                return visited_locations, instructions

            for direction in directions:
                new_x = current[0] + direction[0]
                new_y = current[1] + direction[1]
                new_coordinates = (new_x, new_y)

                if new_coordinates not in visited:
                    if 0 <= new_x < self.x_grid_size and 0 <= new_y < self.y_grid_size:
                        fifo.put(new_coordinates)
                        visited.add(new_coordinates)
                        came_from[new_coordinates] = current
                        visited_locations.append(new_coordinates)

        return visited_locations, []

    def move(self, path, grid):
        if len(path) >= 1:
            old_x, old_y = self.troop_coordinates
            instruction = path.pop(0)
            new_x = old_x + instruction[0]
            new_y = old_y + instruction[1]

            if grid[old_y][old_x] is self:
                grid[old_y][old_x] = None

            self.troop_coordinates = (new_x, new_y)
            grid[new_y][new_x] = self
        else:
            self.at_target = True

        return self.troop_coordinates

    def check_for_collision(self, grid):
        x, y = self.troop_coordinates
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.x_grid_size and 0 <= ny < self.y_grid_size:
                cell = grid[ny][nx]
                if isinstance(cell, buildings.Building):
                    return True, cell

        return False, None

    def take_damage(self, damage, grid=None):
        self.health -= damage
        if self.health <= 0:
            self.die(grid)

    def attack(self, target_building, grid):
        destroyed = target_building.damage(self.attack_damage, grid)
        return destroyed

    def die(self, grid=None):
        self.alive = False
        if grid is not None:
            self.remove_object(grid)

    def remove_object(self, grid):
        x, y = self.troop_coordinates
        if grid[y][x] is self:
            grid[y][x] = None


class big_troop(troop):
    def __init__(self, grid_dimentions, troop_coordinates, grid_tile_size):
        health = 50
        speed = 1
        attack_damage = 67
        troop_size = 12

        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.rgb_color = (0, 255, 0)

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)


class small_troop(troop):
    def __init__(self, grid_dimentions, troop_coordinates, grid_tile_size):
        health = 15
        speed = 4
        attack_damage = 50
        troop_size = 8

        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.rgb_color = (0, 0, 255)

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)


class terrorist(troop):
    def __init__(self, grid_dimentions, troop_coordinates, grid_tile_size):
        health = 1
        speed = 5
        attack_damage = 999999
        troop_size = 10

        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.rgb_color = (255, 0, 0)

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)

    def attack(self, target_building, grid):
        destroyed = target_building.damage(self.attack_damage, grid)
        self.die(grid)
        return destroyed

class archer(troop):
    def __init__(self, grid_dimentions, troop_coordinates, grid_tile_size):
        health = 50
        speed = 1
        attack_damage = 25
        troop_size = 12
        
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.rgb_color = (0, 0, 0)
        self.shooting_speed = 0.1
        self.target_building = None

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)

    def attack(self, target_building, grid):
        arrow.create_arrow(
                self.troop_coordinates[0],
                self.troop_coordinates[1],
                target_building,
                self.shooting_speed,
                self.attack_damage)

        dead = target_building.hp <= self.attack_damage

        return dead

    def check_for_collision(self, grid):
        x, y = self.troop_coordinates
        for dx, dy in self.instructions[:2]:
            x += dx
            y += dy

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.x_grid_size and 0 <= ny < self.y_grid_size:
                cell = grid[ny][nx]
                if isinstance(cell, buildings.Visible_Building):
                    return True, cell

        if len(self.instructions) < 3:
            self.instructions = []

        return False, None

    
    def move(self, path, grid):
        if len(path) >= 3:
            old_x, old_y = self.troop_coordinates
            instruction = path.pop(0)
            new_x = old_x + instruction[0]
            new_y = old_y + instruction[1]

            if grid[old_y][old_x] is self:
                grid[old_y][old_x] = None

            self.troop_coordinates = (new_x, new_y)
            grid[new_y][new_x] = self
        else:
            self.at_target = True

        return self.troop_coordinates
