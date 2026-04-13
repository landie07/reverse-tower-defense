import pygame
import queue
import math

pygame.init()

# =========================================================
"SETTINGS"
# =========================================================
grid_rows = 10
grid_cols = 10
grid_tile_size = 80
ui_height = 160

screen_width = grid_cols * grid_tile_size
screen_height = grid_rows * grid_tile_size + ui_height

fps = 60
move_delay = 15

starting_cash = 20
building_reward = 4

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 22)

# =========================================================
"VISUAL GRID FUNCTION"
# =========================================================
def make_grid(surface, normal_color, spawn_color, height_block, width_block, height_screen, width_screen):
    number_of_rows = height_screen // height_block
    number_of_colomns = width_screen // width_block

    for row in range(number_of_rows):
        for colomn in range(number_of_colomns):
            x = colomn * width_block
            y = row * height_block
            block = pygame.Rect(x, y, width_block, height_block)

            if row == 0 or row == number_of_rows - 1 or colomn == 0 or colomn == number_of_colomns - 1:
                pygame.draw.rect(surface, spawn_color, block)
            else:
                pygame.draw.rect(surface, normal_color, block)

            pygame.draw.rect(surface, (80, 80, 80), block, 1)  # 1 is de dikte van border

# =========================================================
"BUILDING CLASSES"
# =========================================================
class building:
    color = (150, 100, 50)

    def tick(self, grid):
        pass

    def draw(self, screen, tile_size):
        px = self.y * tile_size
        py = self.x * tile_size

        rect = pygame.Rect(px + 5, py + 5, tile_size - 10, tile_size - 10)
        pygame.draw.rect(screen, self.color, rect)

    @property
    def coordinates(self):
        return (self.x, self.y)

    def damage(self, hp, grid):
        self.hp -= hp
        if self.hp > 0:
            return False

        for row in grid:
            for i, e in enumerate(row):
                if e is self:
                    row[i] = None
                    print("gebouw gestorven")
                    return True
        return True


class wall(building):
    hp = 200
    color = (220, 220, 220)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = wall.hp

    def draw(self, screen, tile_size):
        px = self.y * tile_size
        py = self.x * tile_size

        rect = pygame.Rect(px + 12, py + 28, tile_size - 24, tile_size - 56)
        pygame.draw.rect(screen, self.color, rect)


class tower(building):
    hp = 100
    range = 4
    damage_hp = 5
    shot_cooldown_max = 45
    color = (153, 85, 12)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = tower.hp
        self.shot_cooldown = tower.shot_cooldown_max
        self.target = None

    def find_target(self, troops):
        nearest_troop = None
        nearest_dst = 999999

        for current_troop in troops:
            if not current_troop.alive:
                continue

            tx, ty = current_troop.troop_coordinates
            dst = math.sqrt((self.x - tx) ** 2 + (self.y - ty) ** 2)

            if dst <= self.range and dst < nearest_dst:
                nearest_dst = dst
                nearest_troop = current_troop

        self.target = nearest_troop

    def tick(self, grid, troops):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            return

        self.shot_cooldown = tower.shot_cooldown_max
        self.find_target(troops)

        if self.target is not None and self.target.alive:
            self.target.take_damage(self.damage_hp, grid)

    def draw(self, screen, tile_size):
        super().draw(screen, tile_size)
        px = self.y * tile_size + tile_size // 2
        py = self.x * tile_size + tile_size // 2
        pygame.draw.circle(screen, (90, 50, 10), (px, py), 8)


class landmine(building):
    hp = 1
    trigger_range = 1
    damage_hp = 20
    color = (110, 122, 7)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = landmine.hp

    def tick(self, grid, troops):
        should_explode = False

        for current_troop in troops:
            if not current_troop.alive:
                continue

            tx, ty = current_troop.troop_coordinates
            distance = abs(self.x - tx) + abs(self.y - ty)

            if distance <= self.trigger_range:
                should_explode = True
                break

        if not should_explode:
            return

        for current_troop in troops:
            if not current_troop.alive:
                continue

            tx, ty = current_troop.troop_coordinates
            distance = abs(self.x - tx) + abs(self.y - ty)

            if distance <= self.trigger_range:
                current_troop.take_damage(self.damage_hp, grid)

        self.damage(999999, grid)

    def draw(self, screen, tile_size):
        super().draw(screen, tile_size)
        px = self.y * tile_size + tile_size // 2
        py = self.x * tile_size + tile_size // 2
        pygame.draw.circle(screen, (50, 70, 0), (px, py), 6)

# =========================================================
"TROOP CLASSES"
# =========================================================
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
        self.collision = False
        self.at_target = False

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

            if isinstance(grid[current[0]][current[1]], building):
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
                        cell = grid[new_x][new_y]
                        if cell is None or isinstance(cell, building):
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

            if grid[old_x][old_y] is self:
                grid[old_x][old_y] = None

            self.troop_coordinates = (new_x, new_y)
            grid[new_x][new_y] = self
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
                cell = grid[nx][ny]
                if isinstance(cell, building):
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
        if grid[x][y] is self:
            grid[x][y] = None


class terrorist(troop):
    def __init__(self, health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size):
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.health = 1
        self.speed = 5
        self.attack_damage = 999999
        self.troop_size = 10
        self.rgb_color = (255, 0, 0)

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)

    def attack(self, target_building, grid):
        destroyed = target_building.damage(self.attack_damage, grid)
        self.die(grid)
        return destroyed


class big_troop(troop):
    def __init__(self, health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size):
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.health = 50
        self.speed = 1
        self.attack_damage = 2000
        self.troop_size = 12
        self.rgb_color = (0, 255, 0)

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)


class small_troop(troop):
    def __init__(self, health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size):
        super().__init__(health, speed, grid_dimentions, attack_damage, troop_size, troop_coordinates, grid_tile_size)
        self.health = 15
        self.speed = 4
        self.attack_damage = 500
        self.troop_size = 8
        self.rgb_color = (0, 0, 255)

    def draw_troop(self, screen, rgb_color):
        if self.alive:
            x = self.troop_coordinates[1] * self.grid_tile_size + self.grid_tile_size // 2
            y = self.troop_coordinates[0] * self.grid_tile_size + self.grid_tile_size // 2
            pygame.draw.circle(screen, self.rgb_color, (x, y), self.troop_size)

# =========================================================
"GAME VARIABLES"
# =========================================================
grid = [[None for col in range(grid_cols)] for row in range(grid_rows)]
troops = []
cash = starting_cash
selected_troop = "small"

troop_costs = {
    "small": 2,
    "big": 5,
    "terrorist": 4
}

preplaced_buildings = [
    tower(2, 2),
    tower(2, 5),
    tower(2, 7),
    landmine(3, 4),
    wall(3, 5),
    landmine(4, 6),
    wall(4, 5),
    tower(5, 5),
    wall(5, 4),
    landmine(5, 7),
    tower(7, 2),
    wall(7, 3),
    tower(7, 6),
    landmine(6, 4)
]

for current_building in preplaced_buildings:
    grid[current_building.x][current_building.y] = current_building

# =========================================================
"Check state of game + Place and Update + draw ui and rest of game"
# =========================================================
def get_alive_buildings():
    result = []
    for row in grid:
        for cell in row:
            if isinstance(cell, building):  # is cell een instance van building
                result.append(cell)
    return result

def get_alive_troops():
    result = []
    for current_troop in troops:
        if current_troop.alive:
            result.append(current_troop)
    return result

def place_troop(row, col):
    global cash  # variable bestaat niet enkel in functie maar globaal

    if not (0 <= row < grid_rows and 0 <= col < grid_cols):
        return

    if row != 0 and row != grid_rows - 1 and col != 0 and col != grid_cols - 1:
        return

    if grid[row][col] is not None:
        return

    cost = troop_costs[selected_troop]
    if cash < cost:
        return

    if selected_troop == "small":
        new_troop = small_troop(15, 4, (grid_rows, grid_cols), 500, 8, (row, col), grid_tile_size)
    elif selected_troop == "big":
        new_troop = big_troop(50, 1, (grid_rows, grid_cols), 2000, 12, (row, col), grid_tile_size)
    else:
        new_troop = terrorist(1, 5, (grid_rows, grid_cols), 999999, 10, (row, col), grid_tile_size)

    troops.append(new_troop)
    grid[row][col] = new_troop
    cash -= cost

def update_buildings():
    alive_troops = get_alive_troops()

    for row in grid:
        for cell in row:
            if isinstance(cell, tower):
                cell.tick(grid, alive_troops)
            elif isinstance(cell, landmine):
                cell.tick(grid, alive_troops)

def update_troops():
    global cash

    for current_troop in troops[:]:
        if not current_troop.alive:
            continue

        collision, current_building = current_troop.check_for_collision(grid)

        if collision:
            destroyed = current_troop.attack(current_building, grid)
            if destroyed:
                cash += building_reward
            current_troop.instructions = []
            continue

        if not current_troop.instructions:
            visited_locations = []
            _, path = current_troop.find_path(grid, visited_locations)
            current_troop.instructions = path

        if current_troop.instructions:
            current_troop.move(current_troop.instructions, grid)

def draw_ui():
    ui_rect = pygame.Rect(0, grid_rows * grid_tile_size, screen_width, ui_height)
    pygame.draw.rect(screen, (25, 25, 25), ui_rect)

    text1 = font.render("1 = small   2 = big   3 = terrorist", True, (255, 255, 255))  # text --> iets om te tekenen
    text2 = font.render(f"selected: {selected_troop}", True, (255, 255, 0))
    text3 = font.render(f"cash: {cash}", True, (0, 255, 0))
    text4 = small_font.render("green edge tiles = where you can place troops", True, (200, 200, 200))
    text5 = small_font.render("towers shoot, landmines explode", True, (200, 200, 200))

    screen.blit(text1, (10, grid_rows * grid_tile_size + 10))  # een surface tekenen op een andere
    screen.blit(text2, (10, grid_rows * grid_tile_size + 40))
    screen.blit(text3, (220, grid_rows * grid_tile_size + 40))
    screen.blit(text4, (350, grid_rows * grid_tile_size + 20))
    screen.blit(text5, (350, grid_rows * grid_tile_size + 45))

def draw_everything():
    screen.fill((30, 30, 30))

    make_grid(
        screen,
        (45, 45, 45),
        (60, 100, 60),
        grid_tile_size,
        grid_tile_size,
        grid_rows * grid_tile_size,
        grid_cols * grid_tile_size
    )

    for row in grid:
        for cell in row:
            if isinstance(cell, building):
                cell.draw(screen, grid_tile_size)

    for current_troop in troops:
        if current_troop.alive:
            current_troop.draw_troop(screen, (255, 255, 255))

    draw_ui()

    if len(get_alive_buildings()) == 0:
        win_text = font.render("you destroyed all buildings!", True, (255, 255, 255))
        screen.blit(win_text, (screen_width // 2 - 140, screen_height // 2 - 20))

    pygame.display.flip()

# =========================================================
"BIG WHILE LOOP"
# =========================================================
running = True
move_timer = 0

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_troop = "small"
            elif event.key == pygame.K_2:
                selected_troop = "big"
            elif event.key == pygame.K_3:
                selected_troop = "terrorist"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if my < grid_rows * grid_tile_size:
                    row = my // grid_tile_size
                    col = mx // grid_tile_size
                    place_troop(row, col)

    update_buildings()

    move_timer += 1
    if move_timer >= move_delay:
        move_timer = 0
        if len(get_alive_buildings()) > 0:
            update_troops()

    draw_everything()

pygame.quit()