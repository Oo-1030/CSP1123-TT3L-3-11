import pygame
from sprite import sprites, Sprite
from map import TileKind, Map

pygame.init()

def up_edge():
    return y >=0
def down_edge():
    return y <=720-64
def left_edge():
    return x >=0
def right_edge():
    return x <=1280-64

x=725
y=375
speed=7

run = True

jumpcount = 8
Isjump = False


char_img = pygame.image.load("CSP1123-TT3L-3-11/Character/character.png")  
char_img = pygame.transform.scale(char_img, (64, 64))

char_back_img = pygame.image.load("CSP1123-TT3L-3-11/Character/char.back.png")  
char_back_img = pygame.transform.scale(char_back_img, (64, 64))

pygame.display.set_caption("MMU X Secret")
screen = pygame.display.set_mode((1280, 720))
clear_color = (30, 150, 50)
running = True
tile_kinds = [
    TileKind("dirt", "CSP1123-TT3L-3-11/MAP/images/dirt.png", False), # 0
    TileKind("grass", "CSP1123-TT3L-3-11/MAP/images/grass.png", False), # 1
    TileKind("road", "CSP1123-TT3L-3-11/MAP/images/road.png", False), # 2
    TileKind("longkang", "CSP1123-TT3L-3-11/MAP/images/longkang.png", False), # 3 
    TileKind("stairL", "CSP1123-TT3L-3-11/MAP/images/stairL.png", False), # 4
    TileKind("stairM", "CSP1123-TT3L-3-11/MAP/images/stairM.png", False), # 5
    TileKind("stairR", "CSP1123-TT3L-3-11/MAP/images/stairR.png", False), # 6
    TileKind("blueWall", "CSP1123-TT3L-3-11/MAP/images/blueWall.png", False), # 7
    TileKind("whiteWall", "CSP1123-TT3L-3-11/MAP/images/whiteWall.png", False) # 8
]
map = Map("CSP1123-TT3L-3-11/MAP/maps/start.map", tile_kinds, 32)
Sprite("CSP1123-TT3L-3-11/MAP/images/cat.png", 10 * 32, 15 * 32)

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

    #screen.blit(char_back_img, (x, y))

    screen.blit(char_img, (x, y))

    key = pygame.key.get_pressed()
    if key[pygame.K_a] and left_edge():
        x-=speed
    if key[pygame.K_d] and right_edge():
        x+=speed
    if not(Isjump):
        if key[pygame.K_w] and up_edge():
            y-=speed
        if key[pygame.K_s] and down_edge():
            y+=speed
        if key[pygame.K_SPACE]:
            Isjump = True
    else:
        if jumpcount >= -8:
            neg = 1
            if jumpcount <0:
                neg = -1
            y-=(jumpcount ** 2) * 0.3 * neg
            jumpcount -=1
        else:
            Isjump = False
            jumpcount = 8

    pygame.display.flip()

    pygame.time.delay(17)


pygame.quit()