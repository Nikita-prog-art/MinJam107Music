if __name__ == '__main__':
	import main
	main.random.randint(0, 1)
	exit()

import pygame
import random
from common import *

entities = []

class Base_entity:
	def __init__(self, texture: str) -> None:
		self.texture = to_surf(texture)

	def to_crt(self):
		return (self.x, self.y)

	def draw(self, surf: pygame.surface.Surface):
		surf.blit(self.texture, self.to_crt())

class Box_entity(Base_entity):
	def __init__(self, texture: str, diff = 0) -> None:
		super().__init__(texture)
		self.diff = diff
		self.randomize()
		entities.append(self)

	def convert_cords(self):
		self.x = self.bx * cell_size + space_between + self.diff
		self.y = self.by * cell_size + space_between + self.diff

	def randomize(self):
		self.bx = random.randint(1, cell_width - 2)
		self.by = random.randint(1, cell_width - 2)
		self.convert_cords()
		for ent in entities:
			if self.to_crt() == ent.to_crt():
				self.randomize()

	def move(self, x = 0, y = 0):
		if 0 < self.bx + x < cell_width and 0 < self.by + y < cell_height:
			self.bx += x
			self.by += y
			self.convert_cords()
		