import troop_classes
import pygame
import numpy as np
import random

screen_width = 500
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
small_troop1 = troop_classes.small_troop(50, 50, (50, 50), 50)



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
            print(maze[x, y])
    #make an edge around
    maze[:,0] = 1
    maze[0,:] = 1
    maze[:,-1] = 1
    maze[-1,:] = 1

    maze[1, 1] = 0
    print(maze)
    return maze


running = True
while running:
    clock.tick(20)
    screen.fill(color=(0,0,0))
   # small_troop1.draw_troop(screen, (255,255,255), (0, 0), radius = 50, alive = True)
    maze = create_maze(24, 20)
    small_troop1.move((5, 5), 5, )
   # small_troop1.find_nearest_building()
    pygame.display.flip()

pygame.quit()




