import pygame 
def make_grid(surface:pygame.Surface,color:tuple,height_block:int,width_block:int,height_screen:int,width_screen:int):
    
    
    number_of_rows = height_screen // height_block # // range heeft int nodig
    number_of_colomns = width_screen // width_block
    for row in range(number_of_rows):
        for colomn in range(number_of_colomns):
            x = colomn*width_block
            y = row * height_block
          
            block = pygame.Rect(x, y,width_block,height_block )
 
            pygame.draw.rect(surface, color, block)
            
