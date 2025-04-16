import pygame
from sprite import sprites, Sprite
from map import TileKind, Map

pygame.init()

pygame.display.set_caption("MMU X Secret")
screen = pygame.display.set_mode((1280, 720))
clear_color = (30, 150, 50)
running = True
tile_kinds = [
    TileKind("dirt", "MAP/images/dirt.png", False), # 0
    TileKind("grass", "MAP/images/grass.png", False), # 1
    TileKind("road", "MAP/images/road.png", False), # 2
    TileKind("longkang", "MAP/images/longkang.png", False), # 3 
    TileKind("stairL", "MAP/images/stairL.png", False), # 4
    TileKind("stairM", "MAP/images/stairM.png", False), # 5
    TileKind("stairR", "MAP/images/stairR.png", False), # 6
    TileKind("blueWall", "MAP/images/blueWall.png", False), # 7
    TileKind("whiteWall", "MAP/images/whiteWall.png", False) # 8
]
map = Map("MAP/maps/start.map", tile_kinds, 32)
Sprite("MAP/images/cat.png", 10 * 32, 15 * 32)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Draw Code
    screen.fill(clear_color)
    map.draw(screen)
    for s in sprites:
        s.draw(screen)
    pygame.display.flip()

    pygame.time.delay(17)

pygame.quit()
