import pygame
pygame.init()

screen_width=1280
screen_height=720

screen=pygame.display.set_mode((screen_width,screen_height))

def up_edge():
    return y >=radius
def down_edge():
    return y<=screen_height-radius
def left_edge():
    return x>=0+radius
def right_edge():
    return x<=screen_width-radius

x=725
y=375
radius=50
speed=7

run = True
run2 = False

while run:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if key[pygame.K_RETURN]:
            run = False
            run2 = True
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))
    pygame.display.flip()



screen2 = pygame.display.set_mode((screen_width,screen_height))

jumpcount = 10
Isjump = False


char_img = pygame.image.load("character.png")  
char_img = pygame.transform.scale(char_img, (64, 64))

char_back_img = pygame.image.load("char.back.png")  
char_back_img = pygame.transform.scale(char_back_img, (64, 64))


while run2:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_RETURN]:
            run2 = False
    screen2.fill((180,220,220))

    #screen.blit(char_back_img, (x, y))

    screen.blit(char_img, (x, y))
        

    #pygame.draw.circle(screen,(211,211,211),(x,y),radius)

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