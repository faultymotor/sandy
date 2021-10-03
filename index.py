import pygame
from pygame.locals import *
from math import sqrt

from sandy import world

WIDTH, HEIGHT = 800, 800
WORLD_WIDTH, WORLD_HEIGHT = 100, 100
TICK_SPEED = 3
BRUSH_SIZE = 3
FPS = 30

assert WIDTH % WORLD_WIDTH == 0
assert HEIGHT % WORLD_HEIGHT == 0
assert WIDTH / WORLD_WIDTH == HEIGHT / WORLD_HEIGHT

SCALE = WIDTH / WORLD_WIDTH

clock = pygame.time.Clock()
 
pygame.init()
pygame.display.set_caption('sandy')

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])

running = True
is_mouse_dragging = False
placing_water = 0

surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill((0, 0, 0))
world_obj = world.World(surface, WORLD_WIDTH, WORLD_HEIGHT, TICK_SPEED)


def draw_array_to_screen(display):    
    display.blit(surface, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            is_mouse_dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_mouse_dragging = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            placing_water = 1 - placing_water

    cur_x, cur_y = pygame.mouse.get_pos()
    del_x, del_y = pygame.mouse.get_rel()

    if is_mouse_dragging and world_obj.get_num_awake() < 1200: 
        placing = world.WATER if placing_water else world.SAND
        world_obj.set_cells(cur_x / SCALE, cur_y / SCALE, del_x // SCALE, del_y // SCALE, placing, BRUSH_SIZE)

    display.blit(world_obj.get_surface(), (0, 0))

    pygame.display.update()
    world_obj.tick()
    clock.tick(FPS)
