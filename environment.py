import pygame
import os
import random

class Environment:
    def __init__(self, screen):
        self.screen = screen
        self.tiles = []
        self.tile_size = 32  # Tile size (32x32 pixels)

        # Load all available tiles
        self.load_tiles()

        # Calculate rows and columns for the screen
        screen_width, screen_height = self.screen.get_size()
        self.rows = screen_height // self.tile_size + 1
        self.cols = screen_width // self.tile_size + 1

        # Map to store randomized tile indices
        self.tile_map = self.generate_map()

    def load_tiles(self):
        """ Load all tiles dynamically from the Asset folder """
        tile_folder = os.path.join("Asset", "environment")
        for i in range(1, 31):  # Adjust this range based on the tile count
            tile_path = os.path.join(tile_folder, f"FieldsTile_{i:02d}.png")
            try:
                tile_image = pygame.image.load(tile_path).convert_alpha()
                self.tiles.append(tile_image)
            except pygame.error:
                print(f"Error loading {tile_path}")

    def generate_map(self):
        """ Generate a tile map with better randomness """
        tile_map = []
        for row in range(self.rows):
            tile_row = []
            for col in range(self.cols):
                # Avoid repeating the same tile as the previous one
                prev_tile = tile_row[-1] if tile_row else None
                new_tile = random.randint(0, len(self.tiles) - 1)
                while new_tile == prev_tile:  # Ensure no consecutive repetition
                    new_tile = random.randint(0, len(self.tiles) - 1)
                tile_row.append(new_tile)
            tile_map.append(tile_row)
        return tile_map

    def draw(self):
        """ Draw the environment using the generated tile map """
        for row_idx, row in enumerate(self.tile_map):
            for col_idx, tile_index in enumerate(row):
                tile = self.tiles[tile_index]
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size
                self.screen.blit(tile, (x, y))
