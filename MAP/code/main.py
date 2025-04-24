import pygame
import input
from player import Player
from sprite import sprites, Sprite
from map import TileKind, Map
from camera import create_screen
from entity import Entity, active_objs
from physics import Body

# Set up
pygame.init()

screen = create_screen(1280, 720, "MMU X Secret")

clear_color = (30, 150, 50)
running = True

player = Entity(Player(), Sprite("CSP1123-TT3L-3-11/MAP/images/character.png", scale=(64, 64) ), Body(15, 32, 32, 32), x=32*11, y=32*7)

tile_kinds = [
    TileKind("dirt", "CSP1123-TT3L-3-11/MAP/images/dirt.png", False), # 0
    TileKind("grass", "CSP1123-TT3L-3-11/MAP/images/grass.png", False), # 1
    TileKind("road", "CSP1123-TT3L-3-11/MAP/images/road.png", False), # 2
    TileKind("longkang", "CSP1123-TT3L-3-11/MAP/images/longkang.png", True), # 3 
    TileKind("stairL", "CSP1123-TT3L-3-11/MAP/images/stairL.png", False), # 4
    TileKind("stairM", "CSP1123-TT3L-3-11/MAP/images/stairM.png", False), # 5
    TileKind("stairR", "CSP1123-TT3L-3-11/MAP/images/stairR.png", False), # 6
    TileKind("blueWall", "CSP1123-TT3L-3-11/MAP/images/blueWall.png", True), # 7
    TileKind("whiteWall", "CSP1123-TT3L-3-11/MAP/images/whiteWall.png", True) # 8
]
map = Map("CSP1123-TT3L-3-11/MAP/maps/start.map", tile_kinds, 32)

def make_cat(x, y):
    Entity(Sprite("CSP1123-TT3L-3-11/MAP/images/cat.png"), Body(0, 0, 32, 32), x=x, y=y)

make_cat(10 * 32, 15 * 32)

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
    map.draw(screen)
    for s in sprites:
        s.draw(screen)


    pygame.display.flip()

    pygame.time.delay(17)

pygame.quit()
