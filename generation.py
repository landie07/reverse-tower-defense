import buildings
import random
import numpy
from math import sqrt, exp

costs = {
        "wall": 1,
        "tower": 5,
        "landmine": 7,
        }

wall_structures_weight = {
        "square": 6,
        "circle": 3,
        "random": 1,
        }

wall_destruction_chance = {
        "square": 0.08,
        "circle": 0.08,
        "random": 0,
        }

# budget moet klein genoeg zijn dat niet alles opgevuld wordt
def generate_level(rows, cols, budget):
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    centre_x = cols // 2
    centre_y = rows // 2
    grid[centre_y][centre_x] = buildings.Very_Important_Building(centre_x, centre_y)

    affected_cells = { b: [[None for _ in range(cols)] for _ in range(rows)] for b in costs }

    min_cost = min(costs.values())

    budgets = { "wall": 0, "tower": 0, "landmine": 0 }
    divide_budget(budget, budgets)

    left_over = place_walls(grid, budgets["wall"])
    del budgets["wall"]
    divide_budget(left_over, budgets)

    left_over = place_towers(grid, budgets["tower"])
    del budgets["tower"]
    divide_budget(left_over, budgets)

    left_over = place_landmines(grid, budgets["landmine"])
    del budgets["landmine"]
    divide_budget(left_over, budgets)

    return grid

# todo hier willekeur aan toevoegen
def divide_budget(budget, budgets):
    l = len(budgets)
    i = l - 1
    for key in budgets:
        budgets[key] += (budget + i) // l
        i -= 1

def place_walls(grid, budget):
    structs = list(wall_structures_weight.keys())
    struct_weights = []
    for struct in structs:
        struct_weights.append(wall_structures_weight[struct])

    last_round = False
    cost = costs["wall"]
    MAX_LOOP = 100
    while budget > cost:
        MAX_LOOP -= 1
        if MAX_LOOP == 0:
            break

        struct = random.choices(structs, weights=struct_weights, k=1)[0]

        if struct == "square":
            if last_round:
                max_side = 7
            else:
                max_side = budget // 4 + 1 # +1 omdat hoekpunten

            max_radius = (max_side) // 2
            min_radius = 2
            if not last_round and max_radius < min_radius:
                last_round = True
                continue

            radius = random.randint(min_radius, max_radius)
            cy = len(grid) // 2
            cx = len(grid[cy]) // 2

            r = random.random()
            if r < 0.05:
                cx -= 1
            elif r < 0.1:
                cx += 1

            r = random.random()
            if r < 0.05:
                cy -= 1
            elif r < 0.1:
                cy += 1

            y1 = cy - radius
            y2 = cy + radius
            x1 = cx - radius
            x2 = cx + radius

            destruct_chance = wall_destruction_chance["square"]
            if last_round:
                destruct_chance = 1 - destruct_chance
            placed = 0
            # zijden
            for i in range(-radius+1, radius):
                x = cx + i
                y = cy + i

                if random.random() >= destruct_chance:
                    placed += put(grid, buildings.Wall(x, y1))
                if random.random() >= destruct_chance:
                    placed += put(grid, buildings.Wall(x, y2))
                if random.random() >= destruct_chance:
                    placed += put(grid, buildings.Wall(x1, y))
                if random.random() >= destruct_chance:
                    placed += put(grid, buildings.Wall(x2, y))


            # hoeken
            if random.random() >= destruct_chance:
                placed += put(grid, buildings.Wall(x1, y1))
            if random.random() >= destruct_chance:
                placed += put(grid, buildings.Wall(x2, y1))
            if random.random() >= destruct_chance:
                placed += put(grid, buildings.Wall(x1, y2))
            if random.random() >= destruct_chance:
                placed += put(grid, buildings.Wall(x2, y2))

            budget -= cost * placed
            if last_round:
                break

        elif struct == "circle":
            if last_round:
                max_radius = 7
            else:
                max_radius = budget // 6 // cost # 6 ≈ 2π
            min_radius = 2

            if not last_round and max_radius < min_radius:
                last_round = True
                continue

            radius = random.randint(min_radius, max_radius)

            cy = len(grid) // 2
            cx = len(grid[cy]) // 2

            r = random.random()
            if r < 0.05:
                cx -= 1
            elif r < 0.1:
                cx += 1

            r = random.random()
            if r < 0.05:
                cy -= 1
            elif r < 0.1:
                cy += 1

            destruct_chance = wall_destruction_chance["circle"]
            if last_round:
                destruct_chance = 1 - destruct_chance

            placed = 0

            neighbours = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]

            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    dst = sqrt(dx**2 + dy**2)

                    # in de cirkel zijn
                    if dst > radius + 0.5:
                        continue

                    # rand detecteren
                    if not any(map(lambda n: sqrt((n[0]+dx)**2 + (n[1]+dy)**2) > radius + 0.5, neighbours)):
                        continue

                    if random.random() >= destruct_chance:
                        placed += put(grid, buildings.Wall(cx + dx, cy + dy))


            budget -= cost*placed
            if last_round:
                break

        elif struct == "random":
            count = random.randint(1, 3)
            placed = 0
            for i in range(count):
                y = random.randrange(1, len(grid) - 1)
                x = random.randrange(1, len(grid[y]) - 1)
                placed += put(grid, buildings.Wall(x, y))

            budget -= cost*placed

    return budget

def place_towers(grid, budget):
    cost = costs["tower"]

    free_spots = []
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] == None:
                free_spots.append((j, i))

    placed = []
    while budget >= cost:
        to_centre = -1
        from_others = 0.4

        ws = []
        cy = len(grid) // 2
        cx = len(grid[cy]) // 2

        for x, y in free_spots:
            w = 1
            w *= exp(to_centre*sqrt( (x-cx)**2 + (y-cy)**2 ))

            for px, py in placed:
                w *= -exp(-from_others*sqrt( (x-px)**2 + (y-py)**2 )) + 1

            ws.append(w)

        i = random.choices(range(len(free_spots)), weights = ws, k=1)[0]
        x, y = free_spots[i]

        if put(grid, buildings.Tower(x, y)) == 1:
            del free_spots[i]
            placed.append((x, y))
            budget -= cost

    return budget

def place_landmines(grid, budget):
    cost = costs["landmine"]
    MAX_LOOP = 100
    while budget >= cost:
        MAX_LOOP -= 1
        if MAX_LOOP <= 0:
            break

        x = random.randrange(1, len(grid)-1)
        y = random.randrange(1, len(grid)-1)
        budget -= cost*put(grid, buildings.Landmine(x, y))

    return budget

def put(grid, building):
    if grid[building.y][building.x] == None:
        grid[building.y][building.x] = building
        return 1

    return 0
