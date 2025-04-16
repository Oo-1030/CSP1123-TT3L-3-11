import pygame
pygame.init()

screen_width=1280
screen_height=720

screen=pygame.display.set_mode((screen_width,screen_height))

def up_edge():
    return y >=64
def down_edge():
    return y<=screen_height
def left_edge():
    return x>=64
def right_edge():
    return x<=screen_width

x=725
y=375
speed=7

run = True

jumpcount = 10
Isjump = False


char_img = pygame.image.load("CSP1123-TT3L-3-11/Character/character.png")  
char_img = pygame.transform.scale(char_img, (64, 64))

char_back_img = pygame.image.load("CSP1123-TT3L-3-11/Character/char.back.png")  
char_back_img = pygame.transform.scale(char_back_img, (64, 64))


while run:
    pygame.time.delay(10)
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_RETURN]:
            run = False
    screen.fill((180,220,220))

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
        if jumpcount >= -10:
            neg = 1
            if jumpcount <0:
                neg = -1
            y-=(jumpcount ** 2) * 0.5 * neg
            jumpcount -=1
        else:
            Isjump = False
            jumpcount = 10

    pygame.display.flip()



pygame.quit()