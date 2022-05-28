import pygame

cell_size = 54
cell_width = 12 #15
cell_height = 12 #15
tile_size = cell_size - 10
space_between = (cell_size - tile_size) / 2

def to_surf(path: str) -> pygame.surface.Surface:
	return pygame.image.load('res/' + path).convert_alpha()
