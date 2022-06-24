import pygame
import random

tile_width = 500
ground_y = 700

random.seed()


class Tile:
    def __init__(self,x):
        self.map_x = x
    
    def tick(self, x_shift):
        self.x = self.map_x - x_shift

    def render(self, screen):
        screen.fill((0,255,0), pygame.Rect(self.x, ground_y, tile_width, 200))
        pygame.draw.line(screen, (0,0,0), (self.x, 0), (self.x, ground_y))

class Map:
    def __init__(self):
        self.tiles = []
        self.generate()

    def generate(self):
        for i in range(128):
            self.tiles.append(Tile(i*tile_width))
   
    def tick(self, x_shift):
        for tile in self.tiles:
            tile.tick(x_shift)
     
    def render(self, screen):
        for tile in self.tiles:
            tile.render(screen)
