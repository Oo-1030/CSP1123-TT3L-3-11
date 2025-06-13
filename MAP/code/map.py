import pygame
from math import ceil
import os

map_folder_location = "maps"
base_path = os.path.dirname(__file__)
assets_path = os.path.join(base_path, "assets")
tile_size = 32

tile_char_map = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '!': 10,
    '@': 11, 
    '#': 12,
    '$': 13,
    '%': 14,
    '^': 15,
    '&': 16,
    'r': 17,
    'f': 18,
    'w': 19,
    'b': 20,
}

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(assets_path + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, data, tile_kinds):
        from engine import engine
        engine.background_drawables.append(self)

        self.tile_kinds = tile_kinds

        # Set up the tiles from loaded data
        self.tiles = []
        for line in data.split('\n'):
            row = []
            for tile_char in line:
                if tile_char in tile_char_map:
                    row.append(tile_char_map[tile_char])
                else:
                    raise ValueError(f"Unknown tile character: '{tile_char}'")
            self.tiles.append(row)

        # How big in pixels are the tiles?
        self.tile_size = tile_size

    def is_point_solid(self, x, y):
        x_tile = int(x/self.tile_size)
        y_tile = int(y/self.tile_size)
        if x_tile < 0 or \
            y_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return True
        tile = self.tiles[y_tile][x_tile]
        return self.tile_kinds[tile].is_solid


    def is_rect_solid(self, x, y, width, height):
        # Check the top left and middle (if bigger than tile size)
        x_checks = int(ceil(width/self.tile_size))
        y_checks = int(ceil(height/self.tile_size))
        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi*self.tile_size + x
                y = yi*self.tile_size + y
                if self.is_point_solid(x, y):
                    return True
        if self.is_point_solid(x + width, y):
            return True
        if self.is_point_solid(x, y + height):
            return True
        if self.is_point_solid(x + width, y + height):
            return True
        return False

    def draw(self, screen):
        # Go row by row
        from camera import camera
        for y, row in enumerate(self.tiles):
            # Within the current row, go through each tile
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)