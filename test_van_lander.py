import troop_classes
import pygame

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
small_troop1 = troop_classes.small_troop(50, 50, (50, 50), 50)

running = True
while running:
    clock.tick(20)
    screen.fill(color=(0,0,0))
    small_troop1.draw_troop(screen, (255,255,255), (0, 0), radius = 50, alive = True)
   # small_troop1.find_nearest_building()
 # ball = pygame.draw.circle(screen,color=(255,255,255),center=(bal_pos_x, bal_pos_y),radius=bal_radius)

    """ for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
               player_pos -= 15
            if event.key == pygame.K_DOWN:
               player_pos += 15
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos += player_speed 

    font = pygame.font.Font(None, size=font_size)
    screen.blit(font.render(f"Score :{score}", True, (0,0,255)),dest=(locationX,locationY))

    bal_pos_x, bal_pos_y, bal_velocity_x, bal_velocity_y = moveCircle(bal_pos_x, bal_pos_y)
    bal_pos_x, bal_pos_y, bal_velocity_x, bal_velocity_y, score, running = handle_collision(bal_pos_x, bal_pos_y, bal_velocity_x, bal_velocity_y, player_pos, player_width, player_height, score, running)  """
    pygame.display.flip()

pygame.quit()




