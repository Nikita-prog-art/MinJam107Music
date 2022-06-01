import random

import pygame

import entity
from common import *


def draw_ramka(self: entity.Box_entity):
    draw_rect(
        self.x - 1.5 * space_between,
        self.y - 1.5 * space_between,
        cell_size,
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    )


def draw_rect(x, y, size, color):
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, rect)


def get_text_surf(text: str):
    return my_font.render(text, False, (0, 0, 0))


def draw_map():
    for y in range(1, cell_width - 1):
        for x in range(1, cell_height - 1):
            draw_rect(
                x * cell_size + space_between,
                y * cell_size + space_between,
                tile_size,
                tile_color,
            )
    draw_ramka(music_block)
    music_block.draw(screen)
    player.draw(screen)
    screen.blit(
        get_text_surf(f"score: {score}"),
        ((cell_width - 4) * cell_size + space_between, cell_size / 2),
    )
    for note in entity.notes:
        note.draw(screen)
    for i in range(health):
        h_players[i].draw(screen)


def upd():
    global score, health
    if music_block.check_collision():
        score += 1
        if health < 3:
            health += 1
        music_block.randomize()
    for note in entity.notes:
        if note.to_bcrt() == player.b_to_crt():
            heat.play()
            if score > 0:
                score -= 1
            health -= 1
            if health == 0:
                return True
            player.randomize()
            entity.notes = []
            break
        crt = player.to_crt() if not gravity_superpower_runned else mouse_pos
        note.move(entity.Pos(crt[0], crt[1]))
    draw_map()
    return False


def create_note():
    def generate_note() -> entity.Note:
        return entity.Note(
            music_block.x + random.randint(-cell_size, cell_size),
            music_block.y + random.randint(-cell_size, cell_size),
        )

    def check_note(note: entity.Note):
        for r_ent in entity.rect_entities:
            if r_ent.b_to_crt() == note.to_bcrt():
                return True
        return False

    note = generate_note()
    while check_note(note):
        note = generate_note()
    entity.notes.append(note)


def check_sp():
    global i, gravity_superpower_ready, gravity_superpower_runned
    if not gravity_superpower_ready and not gravity_superpower_runned:
        if i == 3:
            gravity_superpower_ready = True
            super_ready.play()
            i -= 2
        i += 1
    elif gravity_superpower_runned:
        if i > 0:
            i -= 1
        else:
            gravity_superpower_runned = False


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((cell_width * cell_size, cell_height * cell_size))
back_color = (113, 188, 225)
tile_color = (204, 204, 196)
my_font = pygame.font.SysFont("Comic Sans MS", 30)

s_crt = (pygame.mixer.Sound("res/move.wav"), pygame.mixer.Sound("res/bad_move.wav"))
heat = pygame.mixer.Sound("res/heat.wav")
music_block = entity.Box_entity("music_block.png", space_between / 2)
player = entity.Box_entity("player.png", s_crt=s_crt)
h_players = (
    entity.Box_entity("player.png"),
    entity.Box_entity("player.png"),
    entity.Box_entity("player.png"),
)
super_on = pygame.mixer.Sound("res/super.wav")
super_ready = pygame.mixer.Sound("res/super_ready.wav")
clock = pygame.time.Clock()

health = 3
mouse_pos = entity.Pos(0, 0)
gravity_superpower_ready = False
gravity_superpower_runned = False
i = 0
score, max_score = 0, 0

ONE_SECOND = pygame.USEREVENT
pygame.time.set_timer(ONE_SECOND, 1000)


def game():
    global mouse_pos, gravity_superpower_runned, gravity_superpower_ready
    gameRunning = True
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
            if event.type == ONE_SECOND:
                create_note()
                check_sp()
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = entity.Pos(event.pos[0], event.pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    player.move(y=-1)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    player.move(y=1)
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    player.move(x=-1)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.move(x=1)
                if event.key == pygame.K_g:
                    if gravity_superpower_ready == True:
                        gravity_superpower_ready = False
                        gravity_superpower_runned = True
                        super_on.play
                    else:
                        s_crt[1].play()

        screen.fill(back_color)
        if upd():
            gameRunning = False
        pygame.display.update()
        clock.tick(30)


My_clock = pygame.time.Clock()
gameRunning = True
while gameRunning:
    runGame = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                runGame = True
    screen.fill(back_color)
    screen.blit(
        get_text_surf(f"Max score is {max_score}. Press space to start"),
        ((cell_width // 4) * cell_size, (cell_height // 2) * cell_size),
    )
    pygame.display.update()
    if runGame:
        runGame = False
        for i in range(len(h_players)):
            h_players[i].bx = i + 1
            h_players[i].by = 0
            h_players[i].convert_cords()
        game()
        max_score = max(score, max_score)
        score = 0
        health = 3
        mouse_pos = entity.Pos(0, 0)
        gravity_superpower_ready = False
        gravity_superpower_runned = False
        i = 0
        score = 0
        entity.rect_entities = []
        entity.notes = []
    My_clock.tick(30)


pygame.quit()
