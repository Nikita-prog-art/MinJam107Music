import random
from dataclasses import dataclass

import pygame

import entity
from common import *


def draw_ramka(self: entity.Box_entity):
	draw_rect(self.x - 1.5 * space_between, self.y - 1.5 * space_between, cell_size,
	(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

def draw_rect(x, y, size, color):
	rect = pygame.Rect(x , y, size, size)
	pygame.draw.rect(screen, color, rect)

def draw_map():
	for y in range(1, cell_width - 1):
		for x in range(1, cell_height - 1):
			draw_rect(x * cell_size + space_between,
				y * cell_size + space_between,
				tile_size, tile_color
			)
	draw_ramka(music_block)
	music_block.draw(screen)
	player.draw(screen)

def play_logic_sound() -> bool:
	if random.randint(0, 9) == 9:
		sound.play()
		return True
	return False

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

screen = pygame.display.set_mode((cell_width * cell_size, cell_height * cell_size))
gameRunning = True
back_color = (113, 188, 225)
tile_color = (204, 204, 196)
s = "f f fff    ff   fff   ff      fff  ffffff   ff   fff   fff"

music_block = entity.Box_entity("music_block.png", space_between / 2)
player = entity.Box_entity("player.png") # дорисовать причёску
sound = pygame.mixer.Sound("res/sound.wav")
clock = pygame.time.Clock()
canMove = False

PLAY_LOGIC_SOUND = pygame.USEREVENT
pygame.time.set_timer(PLAY_LOGIC_SOUND, 120)

while gameRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameRunning = False
		if event.type == PLAY_LOGIC_SOUND:
			canMove = play_logic_sound()
		if event.type == pygame.KEYDOWN and canMove:
			if event.key in (pygame.K_UP, pygame.K_w):
				player.move(y = -1)
			if event.key in (pygame.K_DOWN, pygame.K_s):
				player.move(y = 1)
			if event.key in (pygame.K_LEFT, pygame.K_a):
				player.move(x = -1)
			if event.key in (pygame.K_RIGHT, pygame.K_d):
				player.move(x = 1)	

	screen.fill(back_color)
	draw_map()
	pygame.display.update()
	clock.tick(30)

pygame.quit()