import troop_classes
import buildings
import pygame
import random
import settings
import numpy

settings = settings.settings()
screen = pygame.display.set_mode([settings.grid_width * settings.grid_tile_size, settings.grid_height * settings.grid_tile_size])
clock = pygame.time.Clock()

troop_speed = 50
troop_pos_x, troop_pos_y = 5, 5
troop_coordinates = (troop_pos_x, troop_pos_y)
troops = []
Buildings =  []

terrorist = troop_classes.terrorist(50, 2, (settings.grid_width, settings.grid_height), 50, 5, troop_coordinates, settings.grid_tile_size)
terrorist1 = troop_classes.terrorist(50, 2, (settings.grid_width, settings.grid_height), 50, 5, troop_coordinates, settings.grid_tile_size)
terrorist2 = troop_classes.terrorist(50, 2, (settings.grid_width, settings.grid_height), 50, 5, troop_coordinates, settings.grid_tile_size)

troops.append(terrorist)
troops.append(terrorist1)
troops.append(terrorist2)

Buildings =  []

building_1 = buildings.Wall(6 * settings.grid_tile_size, 6 * settings.grid_tile_size, 0)
Buildings.append(building_1)
visited_locations = []


def make_grid(surface:pygame.Surface,color:tuple,height_block:int,width_block:int,height_screen:int,width_screen:int):
    
    number_of_rows = height_screen // height_block # // range heeft int nodig
    number_of_colomns = width_screen // width_block
    for row in range(number_of_rows):
        for colomn in range(number_of_colomns):
            x = colomn*width_block
            y = row * height_block
          
            block = pygame.Rect(x, y,width_block,height_block )
 
            pygame.draw.rect(surface, color, block)
            
def create_maze(dim, saturation):
    maze = [[]]

    for x in range(settings.grid_width):
        maze.append([])
        for y in range(settings.grid_height):
            waarde = random.randint(0, 1000)
            if waarde > saturation*10:
                maze[x].append(None)
            else:
                maze[x].append(buildings.Wall(x * settings.grid_tile_size, y * settings.grid_tile_size, 0))
    #make an edge around
   # maze[building_1.x//settings.grid_tile_size, building_1.y//settings.grid_tile_size] = 1
    #[1, 1] = 0
    for rij in maze:
        for cel in rij:
            if cel == None:
                print("0 ", end="")
            else:
                print("1 ", end="")
        print("")
        print("")
    return maze

grid = create_maze(settings.grid_width, 4)
grid[5].append(terrorist1)
running = True
while running:
    clock.tick(settings.ticks_per_second)
    screen.fill(color=(0,0,0))
    print(grid)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for row in grid:
        for cel in row:
            if cel != None:
                if isinstance(cel, buildings.Building):
                    if cel.hp > 0:
                        cel.draw(screen)
                if isinstance(cel, troop_classes.troop):
                    if cel.alive:
                        cel.draw_troop(screen, (255,255,255))
                    if isinstance(cel, troop_classes.terrorist):
                        if cel.instructions == None or str(cel.instructions) == 0:
                            visited_locations, path_to_nearest_building = cel.find_path(grid, visited_locations) 
                            print(path_to_nearest_building)
                            collision_bool, collision_object = cel.check_for_collision(grid)
                            print("collision_Bool:")
                            print(collision_bool)
                            if collision_bool == True and isinstance(collision_object, buildings.Building):
                                print("damage doen")
                                collision_object.damage(cel.attack_damage, grid)     
                        cel.troop_coordinates = terrorist.move(path_to_nearest_building, building_1, grid)
    pygame.display.flip()

pygame.quit()



# for troop in troops:
#         if terrorist.alive:
#             terrorist.draw_troop(screen, (255,255,255))
#             print("alive")
#         if settings.tick >= settings.ticks_per_second/troop.speed:
#             settings.tick = 0
#             if troop.instructions == None:
#                 visited_locations, path_to_nearest_building = troop.find_path(grid, visited_locations)
#             elif len(troop.instructions) == 0:
#                 visited_locations, path_to_nearest_building = troop.find_path(grid, visited_locations)
#             else:
#                 print("troop.instructions:")
#                 print("'"+str(troop.instructions)+"'")
#         #    visited_locations, path_to_nearest_building = terrorist.go_to_building(grid, visited_locations) 
#         #    visited_locations, path_to_nearest_building = terrorist.find_path(coordinates_of_nearest_building, grid, visited_locations)
#             troop.troop_coordinates = terrorist.move(path_to_nearest_building, building_1, grid)
#     for building in Buildings:
#         building.draw(screen)




