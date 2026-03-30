import troop_classes
import buildings
import pygame
import numpy as np
import random


grid_tile_size = 10
tick = 0
ticks_per_second = 100
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

troop_speed = 50
troop_pos_x, troop_pos_y = 5, 5
troop_coordinates = (troop_pos_x, troop_pos_y)
troops = []
terrorist = troop_classes.terrorist(50, 2, (50, 50), 50, 5, troop_coordinates)
terrorist1 = troop_classes.terrorist(50, 2, (10, 10), 50, 5, troop_coordinates)
terrorist2 = troop_classes.terrorist(50, 2, (20, 20), 50, 5, troop_coordinates)

troops.append(terrorist)
troops.append(terrorist1)
troops.append(terrorist2)



building_1 = buildings.Wall(8 * grid_tile_size, 8 * grid_tile_size, 0)

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
    """
    0 is open plaats
    1 is muur
    """
    maze = np.zeros((dim, dim))

    for x in range(maze.shape[0]):
        for y in range(maze.shape[1]):
            waarde = random.randint(0, 1000)
            if waarde > saturation*10:
                maze[x, y] = 0
            else:
                maze[x, y] = 1
    #make an edge around
    maze[:,0] = 1
    maze[0,:] = 1
    maze[:,-1] = 1
    maze[-1,:] = 1

    maze[1, 1] = 0
    return maze


running = True
while running:
    clock.tick(ticks_per_second)
    tick += 1
    screen.fill(color=(0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    grid = create_maze(16, 65)
    buildings = [building_1]
    for troop in troops:
        if terrorist.alive:
            terrorist.draw_troop(screen, (255,255,255), (troop.troop_coordinates[0] * grid_tile_size, troop.troop_coordinates[1] * grid_tile_size), radius = 5, alive = True)
        if tick >= ticks_per_second/troop.speed:
            tick = 0
            coordinates_of_nearest_building = terrorist.find_nearest_building([building_1], troop.troop_coordinates) 
            visited_locations, path_to_nearest_building = terrorist.find_path(troop.troop_coordinates, coordinates_of_nearest_building, grid, visited_locations)
            troop.troop_coordinates = terrorist.move(troop_coordinates, path_to_nearest_building, building_1)
    pygame.display.flip()

pygame.quit()




