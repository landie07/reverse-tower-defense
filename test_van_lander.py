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
troop_coordinates_terrorist = (5, 5)
troop_coordinates_big_troop = (5, 10)
troop_coordinates_small_troop = (10, 5)
troops = []
Buildings =  []

terrorist = troop_classes.terrorist(50, 2, (settings.grid_width, settings.grid_height), 50, 5, troop_coordinates_terrorist, settings.grid_tile_size)
big_troop = troop_classes.big_troop(50, 2, (settings.grid_width, settings.grid_height), 50, 5, troop_coordinates_big_troop, settings.grid_tile_size)
small_troop = troop_classes.small_troop(50, 2, (settings.grid_width, settings.grid_height), 50, 5, troop_coordinates_small_troop, settings.grid_tile_size)


Buildings =  []

#building_1 = buildings.Wall(6 * settings.grid_tile_size, 6 * settings.grid_tile_size, 0)
#Buildings.append(building_1)
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
                maze[x].insert(y, buildings.Wall(x * settings.grid_tile_size, y * settings.grid_tile_size, 0))

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

grid = create_maze(settings.grid_width, 15)

"""
troop_coordinates_terrorist = (5, 5)
troop_coordinates_big_troop = (5, 10)
troop_coordinates_small_troop = (10, 5)
"""

grid[troop_coordinates_terrorist[0]].insert(troop_coordinates_terrorist[1], terrorist)
grid[troop_coordinates_big_troop[0]].insert(troop_coordinates_big_troop[1], big_troop)
grid[troop_coordinates_small_troop[0]].insert(troop_coordinates_small_troop[1], small_troop)

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
                        print("alive is true")
                        cel.draw_troop(screen, (255,255,255))
                    if isinstance(cel, troop_classes.terrorist):
                        if (cel.instructions == None or len(cel.instructions) == 0) and cel.alive == True:
                            visited_locations, path_to_nearest_building = cel.find_path(grid, visited_locations) 
                            print(path_to_nearest_building)
                            collision_bool, collision_object = cel.check_for_collision(grid)
                            print("collision_Bool:")
                            print(collision_bool)
                            if collision_bool == True and isinstance(collision_object, buildings.Building):
                                print("damage doen")
                                collision_object.damage(cel.attack_damage, grid)  
                                cel.die(grid)  
                        if cel.alive == True: 
                            cel.troop_coordinates = cel.move(path_to_nearest_building, grid)
                    if isinstance(cel, troop_classes.big_troop):
                        if cel.instructions == None or len(cel.instructions) == 0 and cel.alive == True:
                            visited_locations, path_to_nearest_building = cel.find_path(grid, visited_locations) 
                            print(path_to_nearest_building)
                            collision_bool, collision_object = cel.check_for_collision(grid)
                            print("collision_Bool:")
                            print(collision_bool)
                            print(collision_object)
                            if collision_bool == True and isinstance(collision_object, buildings.Building):
                                print("damage doen")
                                collision_object.damage(cel.attack_damage, grid)  
                        if cel.alive == True:    
                            cel.troop_coordinates = cel.move(path_to_nearest_building,  grid)
                    if isinstance(cel, troop_classes.small_troop):
                        if cel.instructions == None or len(cel.instructions) == 0  and cel.alive == True:
                            visited_locations, path_to_nearest_building = cel.find_path(grid, visited_locations) 
                            print(path_to_nearest_building)
                            collision_bool, collision_object = cel.check_for_collision(grid)
                            print("collision_Bool:")
                            print(collision_bool)
                            print(collision_object)
                            if collision_bool == True and isinstance(collision_object, buildings.Building):
                                print("damage doen")
                                collision_object.damage(cel.attack_damage, grid)
                        if cel.alive == True:      
                            cel.troop_coordinates = cel.move(path_to_nearest_building, grid)
    pygame.display.flip()

pygame.quit()

