if __name__ == "__main__":
    import GreenSuperGravityCube

    GreenSuperGravityCube.random.randint(0, 1)
    exit()

import random
from typing import NamedTuple

import pygame

from common import *

id = 0
rect_entities = []
notes = []


class Base_entity:
    def __init__(self, texture: str) -> None:
        global id
        self.id = id
        id += 1
        self.texture = to_surf(texture)

    def to_crt(self):
        return (self.x, self.y)

    def draw(self, surf: pygame.surface.Surface):
        surf.blit(self.texture, self.to_crt())


class Box_entity(Base_entity):
    def __init__(self, texture: str, diff=0, s_crt: tuple = (0, 0)) -> None:
        super().__init__(texture)
        self.diff = diff
        self.move_sound = s_crt[0]
        self.bad_move_sound = s_crt[1]
        self.randomize()
        rect_entities.append(self)

    def convert_cords(self):
        self.x = self.bx * cell_size + space_between + self.diff
        self.y = self.by * cell_size + space_between + self.diff

    def b_to_crt(self):
        return (self.bx, self.by)

    def check_collision(self):
        for ent in rect_entities:
            if (self.id != ent.id) and (self.b_to_crt() == ent.b_to_crt()):
                return True
        return False

    def randomize(self):
        self.bx = random.randint(1, cell_width - 2)
        self.by = random.randint(1, cell_height - 2)
        self.convert_cords()
        if self.check_collision():
            self.randomize()

    def move(self, x=0, y=0):
        if 0 < self.bx + x < cell_width - 1 and 0 < self.by + y < cell_height - 1:
            self.bx += x
            self.by += y
            self.convert_cords()
            self.move_sound.play()
        else:
            self.bad_move_sound.play()


class Note(Base_entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__("note.png")
        self.x, self.y = x, y

    def to_b(self, val: int):
        return (val - space_between) // cell_size

    def to_bcrt(self):
        return (self.to_b(self.x), self.to_b(self.y))

    def move(self, to_obj: Pos):  # check player collision before it!!!
        if self.x < to_obj.x:
            self.x += 1
        else:
            self.x -= 1
        if self.y < to_obj.y:
            self.y += 1
        else:
            self.y -= 1
