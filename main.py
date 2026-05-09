import pygame
import queue
import math
from buildings import *
from troops import *
import generation 
import arrow 
import particle_effect 
import potions 

pygame.init()
# =========================================================
"SETTINGS"
# =========================================================
grid_rows = 25
grid_cols = 25
grid_tile_size = 30
ui_width = 350

screen_width = grid_cols * grid_tile_size + ui_width
screen_height = grid_rows * grid_tile_size

fps = 60
move_delay = 20

starting_cash = 20

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 22)

volume = 0.4
muted = False

# =========================================================
"MUSIC"
# =========================================================
pygame.mixer.init()

pygame.mixer.music.load("kissan4-pixel-paradise-358340.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

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
active_potions = []
cash = starting_cash
selected_troop = "small"

troop_costs = {
    "small": 2,
    "big": 5,
    "terrorist": 4,
    "archer": 3,
    "health_potion" : 2,
    "damage_potion" : 2,
}

translation = {
    "small": "kleine troep",
    "big": "grote troep",
    "terrorist": "terrorist",
    "archer": "boogschutter",
    "health_potion" : "geneesdrankje",
    "damage_potion" : "vuurbal",
}

grid = generation.generate_level(grid_rows, grid_cols, 100)

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
    elif selected_troop == "terrorist":
        new_troop = terrorist((grid_rows, grid_cols), (col, row), grid_tile_size)
    elif selected_troop == "archer":
        new_troop = archer((grid_rows, grid_cols), (col, row), grid_tile_size)

    troops.append(new_troop)
    grid[row][col] = new_troop
    cash -= cost

def place_potions(row,col):
    global cash
    
    if not (0 <= row < grid_rows and 0 <= col < grid_cols):
        return
    
    cost = troop_costs[selected_troop]
    if cash < cost:
        return
    
    if selected_troop == "health_potion":
        new_troop = potions.health_potion(cost, (col, row))
    else:
        new_troop = potions.damage_potion(cost, (col, row))

    active_potions.append(new_troop)
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
            if move_timer % (current_troop.attack_speed) == 0:
                destroyed = current_troop.attack(current_building, grid)
                if destroyed:
                    cash += current_building.destruction_reward
                    current_troop.instructions = []
                continue
        if current_troop.instructions:  
            if move_timer % (current_troop.speed) == 0:
                current_troop.move(current_troop.instructions, grid)
        else:
            visited_locations = []
            _, path = current_troop.find_path(grid, visited_locations)
            current_troop.instructions = path

def update_potions():
    object_list = []
    object_list.extend(get_alive_troops())
    object_list.extend(get_alive_buildings())
    for current_potion in active_potions:
        current_potion.effect(object_list, grid)

        if current_potion.duration <= 0:
            active_potions.remove(current_potion)

def draw_ui():
    ui_rect = pygame.Rect(grid_rows * grid_tile_size, 0, ui_width, screen_height)
    pygame.draw.rect(screen, (25, 25, 25), ui_rect)

    texts = []
    texts.append(font.render("toetsen voor troep of drankje:", True, (255, 255, 255)))
    
    i = 1
    for troop in troop_costs:
        texts.append(font.render(f" [{i}]: {translation[troop]} {troop_costs[troop]}¢", True, (255, 255, 255)))
        i += 1

    texts.append(font.render(f"geselecteerd: {translation[selected_troop]}", True, (255, 255, 0)))
    texts.append(font.render(f"cash: {cash}¢", True, (0, 255, 0)))
    texts.append(small_font.render("plaats troepen op de groene vakjes,", True, (200, 200, 200)))
    texts.append(small_font.render("drankjes kunnen overal geplaatst worden", True, (200, 200, 200)))
    texts.append(small_font.render("bruine torens schieten, groene landmijnen", True, (200, 200, 200)))
    texts.append(small_font.render("ontploffen", True, (200, 200, 200)))

    left = grid_cols * grid_tile_size + 10
    padding = 5
    height = 10
    for text in texts:
        screen.blit(text, (left, height))  # een surface tekenen op een andere
        height += text.get_height() + padding

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
    particle_effect.draw(screen, grid_tile_size)
    for potion in active_potions:
        potion.draw_potion(screen, grid_tile_size)
    draw_ui()

    if not (isinstance(grid[12][12], Very_Important_Building)):
            
            win_text = font.render("you destroyed the very important building!", True, (255, 255, 255))
            screen.blit(win_text, ((screen_width - win_text.get_width()) // 2, (screen_height - win_text.get_height()) // 2))

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
            elif event.key == pygame.K_4:
                selected_troop = "archer"
            elif event.key == pygame.K_5:
                selected_troop = "health_potion"
            elif event.key == pygame.K_6:
                selected_troop = "damage_potion"
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_m:
                if muted:
                    pygame.mixer.music.set_volume(volume)
                    muted = False
                else:
                    pygame.mixer.music.set_volume(0)
                    muted = True


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if my < grid_rows * grid_tile_size:
                    if selected_troop == "health_potion" or selected_troop == "damage_potion":
                        row = my / grid_tile_size
                        col = mx / grid_tile_size
                        place_potions(row, col)
                    else:
                        row = my // grid_tile_size
                        col = mx // grid_tile_size
                        if row == 0 or row == grid_rows - 1 or col == 0 or col == grid_cols - 1:
                            place_troop(row, col)

    update_buildings()
    arrow.tick_arrows(grid)

    move_timer += 1
    if len(get_alive_buildings()) > 0:
        update_troops()
        update_potions()

    draw_everything()

pygame.quit()
