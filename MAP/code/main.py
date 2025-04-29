import pygame
import input
from player import Player
from sprite import sprites, Sprite
from map import TileKind, Map
from camera import create_screen
from entity import Entity, active_objs
from physics import Body
from area import Area, area
from data.tile_types import tile_kinds

# Set up
pygame.init()

screen = create_screen(1280, 720, "MMU X Secret")

clear_color = (30, 150, 240)
running = True

area = Area("start.map", tile_kinds)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)

    # Update code
    for a in active_objs:
        a.update()

    # Draw Code
    screen.fill(clear_color)
    area.map.draw(screen)
    for s in sprites:
        s.draw(screen)


    pygame.display.flip()

    pygame.time.delay(17)

pygame.quit()
