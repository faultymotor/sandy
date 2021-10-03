import pygame
import numpy as np
from math import sqrt

from sandy import world

WIDTH, HEIGHT = 600, 300
GRAVITY = 8
FPS = 120

world_obj = world.World(WIDTH, HEIGHT, GRAVITY)

def draw_array_to_screen(array, display):    
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, (0, 0))

clock = pygame.time.Clock()
 
pygame.init()
pygame.display.set_caption('sandy')

display = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
is_mouse_dragging = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            is_mouse_dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_mouse_dragging = True

    cur_x, cur_y = pygame.mouse.get_pos()
    del_x, del_y = pygame.mouse.get_rel()

    if is_mouse_dragging and world_obj.get_num_awake() < 1200: 
        world_obj.set_cells(cur_x, cur_y, del_x, del_y, world.SAND)
        
    draw_array_to_screen(world_obj.get_rgbs(), display)

    pygame.display.update()
    world_obj.tick()
    clock.tick(FPS)
