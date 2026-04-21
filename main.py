import pygame
import queue
import math
from buildings import *
from troops import *
import arrow 

pygame.init()

# =========================================================
"SETTINGS"
# =========================================================
grid_rows = 25
grid_cols = 25
grid_tile_size = 35
ui_height = 160

screen_width = grid_cols * grid_tile_size
screen_height = grid_rows * grid_tile_size + ui_height

fps = 60
move_delay = 20

starting_cash = 20

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
    Very_Important_Building(12, 12),
    Tower(13, 12),
    Tower(12, 11),
    Tower(11, 12),
    Tower(12, 13),
    Wall(3, 3),
    Wall(4, 3),
    Wall(5, 3),
    Wall(6, 3),
    Wall(6, 4),
    Wall(6, 5),
    Wall(6, 6),
    Wall(5, 6),
    Wall(4, 6),
    Wall(3, 6),
    Wall(3, 5),
    Wall(3, 4),
    Landmine(2, 2),
    # Landmine(3, 2),
    # Landmine(4, 2),
    # Landmine(5, 2),
    # Landmine(6, 2),
    Landmine(7, 2),
    # Landmine(7, 3),
    # Landmine(7, 4),
    # Landmine(7, 5),
    # Landmine(7, 6),
    Landmine(7, 7),
    # Landmine(6, 7),
    # Landmine(5, 7),
    # Landmine(4, 7),
    # Landmine(3, 7),
    Landmine(2, 7),
    # Landmine(2, 6),
    # Landmine(2, 5),
    # Landmine(2, 4),
    # Landmine(2, 3),
]

for current_building in preplaced_buildings:
    grid[current_building.y][current_building.x] = current_building

# =========================================================
"Check state of game + Place and Update + draw ui and rest of game"
# =========================================================
def get_alive_buildings():
    result = []
    for row in grid:
        for cell in row:
            if isinstance(cell, Building):  # is cell een instance van building
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

    if grid[row][col] is not None:
        return

    cost = troop_costs[selected_troop]
    if cash < cost:
        return

    if selected_troop == "small":
        new_troop = small_troop((grid_rows, grid_cols), (col, row), grid_tile_size)
    elif selected_troop == "big":
        new_troop = big_troop((grid_rows, grid_cols), (col, row), grid_tile_size)
    else:
        new_troop = terrorist((grid_rows, grid_cols), (col, row), grid_tile_size)

    troops.append(new_troop)
    grid[row][col] = new_troop
    cash -= cost

def update_buildings():
    alive_troops = get_alive_troops()

    for row in grid:
        for cell in row:
            if isinstance(cell, Building):
                cell.tick(grid, alive_troops)
                alive_troops = list(filter(lambda t: t.alive, alive_troops))
            

def update_troops():
    global cash

    for current_troop in troops:
        if not current_troop.alive:
            continue

        collision, current_building = current_troop.check_for_collision(grid)

        if collision:
            destroyed = current_troop.attack(current_building, grid)
            if destroyed:
                cash += current_building.destruction_reward
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
            if isinstance(cell, Building):
                cell.draw(screen, grid_tile_size)

    for current_troop in troops:
        if current_troop.alive:
            current_troop.draw_troop(screen, (255, 255, 255))
    arrow.draw_arrows(screen, grid_tile_size)

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

a = 0
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
            elif event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if my < grid_rows * grid_tile_size:
                    row = my // grid_tile_size
                    col = mx // grid_tile_size
                    if row == 0 or row == grid_rows - 1 or col == 0 or col == grid_cols - 1:
                        place_troop(row, col)

    update_buildings()
    arrow.tick_arrows(grid)

    move_timer += 1
    if move_timer >= move_delay:
        move_timer = 0
        if len(get_alive_buildings()) > 0:
            update_troops()

    draw_everything()
    a += 1

pygame.quit()
