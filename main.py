import pygame
from pygame import Color as palette

def draw_rect(x, y, size, color):
	rect = pygame.Rect(x , y, size, size)
	pygame.draw.rect(screen, color, rect)

def draw_map():
	for y in range(1, cell_width - 1):
		for x in range(1, cell_height - 1):
			draw_rect(x * cell_size + space_between, y * cell_size + space_between, tile_size, tile_color)

pygame.init()

cell_size = 54
cell_width = 15
cell_height = 15

screen = pygame.display.set_mode((cell_width * cell_size, cell_height * cell_size))
gameRunning = True
back_color = (113, 188, 225)
tile_color = (204, 204, 196)
tile_size = cell_size - 10
space_between = (cell_size - tile_size) / 2

while gameRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameRunning = False
	screen.fill(back_color)
	draw_map()
	pygame.display.update()

pygame.quit()