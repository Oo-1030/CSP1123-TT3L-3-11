import pygame
pygame.init()

screen_width=1280
screen_height=720

screen=pygame.display.set_mode((screen_width,screen_height))


walkLeft = [pygame.transform.scale(pygame.image.load('char_left1.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_left3.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_left5.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_left2.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_left4.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_left5.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_left3.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_left2.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_left5.png'),(64,64))]
walkRight = [pygame.transform.scale(pygame.image.load('char_right1.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_right3.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_right5.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_right2.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_right4.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_right5.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_right3.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_right2.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_right5.png'),(64,64))]
walkDown = [pygame.transform.scale(pygame.image.load('char_down1.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_down2.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_down3.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_down4.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_down2.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_down1.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_down2.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_down3.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_down4.png'),(64,64))]
walkUp = [pygame.transform.scale(pygame.image.load('char_up1.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_up2.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_up3.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_up4.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_up2.png'), (64, 64)),pygame.transform.scale(pygame.image.load('char_up1.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_up2.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_up3.png'), (64, 64)), pygame.transform.scale(pygame.image.load('char_up4.png'),(64,64))]
char = pygame.image.load('character.png')
char = pygame.transform.scale(char, (64, 64))

def up_edge():
    return y >=0
def down_edge():
    return y<=screen_height-64
def left_edge():
    return x>=0
def right_edge():
    return x<=screen_width-70

x=725
y=375
speed=7

run = True
run2 = False

jumpcount = 10
Isjump = False

left = False
right = False
up = False
down = False
walkcount = 0
walkcount2 = 0

'''
fatguy_img = pygame.image.load("fatguy.png")  
fatguy_img = pygame.transform.scale(fatguy_img, (64, 64))

char_img = pygame.image.load("character.png")  
char_img = pygame.transform.scale(char_img, (64, 64))

pinkgirl_img = pygame.image.load("pinkgirl.png")  
pinkgirl_img = pygame.transform.scale(pinkgirl_img, (64, 64))

char_left1_img = pygame.image.load("char_left1.png")  
char_left1_img = pygame.transform.scale(char_left1_img, (64, 64))

char_left2_img = pygame.image.load("char_left2.png")  
char_left2_img = pygame.transform.scale(char_left2_img, (64, 64))

char_left3_img = pygame.image.load("char_left3.png")  
char_left3_img = pygame.transform.scale(char_left3_img, (64, 64))

'''
char_back_img = pygame.image.load("char_back.png")  
char_back_img = pygame.transform.scale(char_back_img, (64, 64))

def redrawGameWindow():
    global walkcount
    global walkcount2

    screen.fill((210,180,210))

    if not left and not right and not up and not down:
        screen.blit(char, (x,y))

    if not(left) and not(right):
        if walkcount2 + 1 >= 27:
            walkcount2 = 0
        if up:
            screen.blit(walkUp[walkcount2 // 3],(x,y))
            walkcount2 += 1

        if down:
            screen.blit(walkDown[walkcount2 // 3],(x,y))
            walkcount2 += 1

    if left or right:
        if walkcount + 1 >= 27:
            walkcount = 0

        if left:
            screen.blit(walkLeft[walkcount//3],(x,y))
            walkcount += 1
        elif right:
            screen.blit(walkRight[walkcount//3],(x,y))
            walkcount += 1 
        

    pygame.display.update()

clock = pygame.time.Clock()

while run:
    clock.tick(27)

    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_RETURN]:
            run = False

    #screen.blit(char_img, (x, y))

    key = pygame.key.get_pressed()

    if key[pygame.K_a] and left_edge():
        x-=speed
        left = True 
        right = False
    elif key[pygame.K_d] and right_edge():
        x+=speed
        right = True 
        left = False
    else:
        right = False
        left = False
        walkcount = 0

    if not(Isjump):
        if key[pygame.K_w] and up_edge():
            y-=speed
            up = True
            down = False
        elif key[pygame.K_s] and down_edge():
            y+=speed
            down = True
            up = False
        elif key[pygame.K_SPACE]:
            Isjump = True
            right = False
            left = False
            up = False
            down = False
            walkcount2 = 0
        else:
            up = False
            down = False
            walkcount2 = 0
            
    else:
        if jumpcount >= -10:
            neg = 1
            if jumpcount <0:
                neg = -1
            y-=(jumpcount ** 2) * 0.3 * neg
            jumpcount -=1
        else:
            Isjump = False
            jumpcount = 10
    
    redrawGameWindow()

pygame.quit()