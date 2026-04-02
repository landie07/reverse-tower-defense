class settings:
    def __init__(self):
        self.grid_tile_size = 1
        self.tick = 0
        self.ticks_per_second = 1
        self.screen_width = 500
        self.screen_height = 500
        self.grid_width = 64
        self.grid_height = 64
        self.troop_speed = 50
        self.troop_pos_x, self.troop_pos_y = 5, 5
        self.troop_coordinates = (self.troop_pos_x, self.troop_pos_y)
        self.troops = []
        