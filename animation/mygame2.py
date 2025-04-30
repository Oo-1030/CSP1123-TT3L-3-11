import pygame
pygame.init()

screen_width=1280
screen_height=720

screen=pygame.display.set_mode((screen_width,screen_height))

htcboss1 = pygame.transform.scale(pygame.image.load('htcboss1.png'),(64,64))
htcboss2 = pygame.transform.scale(pygame.image.load('htcboss2.png'),(70,64))
htcboss3 = pygame.transform.scale(pygame.image.load('htcboss3.png'),(70,64))

redguy1_img = pygame.image.load("redguy1.png")  
redguy1_img = pygame.transform.scale(redguy1_img, (64, 64))

redguy2_img = pygame.image.load("redguy2.png")  
redguy2_img = pygame.transform.scale(redguy2_img, (64, 80))

pinkgirl1_img = pygame.image.load("pinkgirl1.png")  
pinkgirl1_img = pygame.transform.scale(pinkgirl1_img, (64, 64))

pinkgirl2_img = pygame.image.load("pinkgirl2.png")  
pinkgirl2_img = pygame.transform.scale(pinkgirl2_img, (64, 64))

lionguy1_img = pygame.image.load("lionguy1.png")  
lionguy1_img = pygame.transform.scale(lionguy1_img, (64, 64))

lionguy65_img = pygame.image.load("lionguy65.png")  
lionguy65_img = pygame.transform.scale(lionguy65_img, (64, 64))
lionguy64_img = pygame.image.load("lionguy64.png")  
lionguy64_img = pygame.transform.scale(lionguy64_img, (64, 64))


walkLeft = [pygame.transform.scale(pygame.image.load('char_left1.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_left3.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_left5.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_left2.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_left4.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_left5.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_left3.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_left2.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_left5.png'),(64,64))]

walkRight = [pygame.transform.scale(pygame.image.load('char_right1.png'),(64, 64)),
             pygame.transform.scale(pygame.image.load('char_right3.png'), (64, 64)), 
             pygame.transform.scale(pygame.image.load('char_right5.png'), (64, 64)),
             pygame.transform.scale(pygame.image.load('char_right2.png'), (64, 64)),
             pygame.transform.scale(pygame.image.load('char_right4.png'), (64, 64)),
             pygame.transform.scale(pygame.image.load('char_right5.png'), (64, 64)), 
             pygame.transform.scale(pygame.image.load('char_right3.png'), (64, 64)), 
             pygame.transform.scale(pygame.image.load('char_right2.png'), (64, 64)), 
             pygame.transform.scale(pygame.image.load('char_right5.png'),(64,64))]

walkDown = [pygame.transform.scale(pygame.image.load('char_down1.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_down2.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_down3.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_down4.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_down2.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_down1.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_down2.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_down3.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_down4.png'),(64,64))]

walkUp = [pygame.transform.scale(pygame.image.load('char_up1.png'), (64, 64)),
          pygame.transform.scale(pygame.image.load('char_up2.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_up3.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_up4.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_up2.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_up1.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_up2.png'), (64, 64)), 
            pygame.transform.scale(pygame.image.load('char_up3.png'), (64, 64)),
            pygame.transform.scale(pygame.image.load('char_up4.png'),(64,64))]

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

jumpcount = 7
Isjump = False

left = False
right = False
up = False
down = False
walkcount = 0
walkcount2 = 0

level = 1
exp = 0
max_exp = 100
max_level = 20
luck = 0

font = pygame.font.SysFont('microsoftyahei', 20)

def exp_system():
    global max_exp, exp, level,luck

    if level < max_level:
        if exp >= max_exp:
            exp_left = exp - max_exp
            exp = exp_left
            level += 1
            max_exp = 100 * level
            luck += 10 * level
        ratio = exp / max_exp
        level_text = font.render(f"Level:{level}", True, (0,0,0))
        screen.blit(level_text, (55, 685))

        exp_text = font.render(f"{exp}/{max_exp}",True,(0,0,0))
        screen.blit(exp_text, (1165, 685))

        pygame.draw.rect(screen,(0,50,255),(135,685,1010,30)) # outline
        pygame.draw.rect(screen,(250,250,250),(140,690,1000,20)) # max
        pygame.draw.rect(screen,(85,160,255),(140,690,1000*ratio,20)) # ratio

    else:
        level_text = font.render(f"Level:{level}", True, (0,0,0))
        screen.blit(level_text, (55, 685))
        exp_text = font.render("max/max",True,(0,0,0))
        screen.blit(exp_text, (1165, 685))
        pygame.draw.rect(screen,(0,50,255),(135,685,1010,30)) # outline
        pygame.draw.rect(screen,(85,160,255),(140,690,1000,20)) # ratio
    
    exp_text = font.render(f"Luck:{luck}",True,(0,0,0))
    screen.blit(exp_text, (20, 20))

        

      

htcboss_ani = False
htcboss_x = 300
htcboss_y = 500
new_htcboss_x = htcboss_x - 12 #for fixing drawing issue

redguy_ani = False
redguy_x = 350
redguy_y = 100
new_redguy_y = redguy_y -16 #for fixing drawing issue

pinkgirl_ani = False
pinkgirl_x = 150
pinkgirl_y = 500

clock = pygame.time.Clock()

fatguy_img = pygame.image.load("fatguy.png")  
fatguy_img = pygame.transform.scale(fatguy_img, (64, 64))

char_back_img = pygame.image.load("char_back.png")  
char_back_img = pygame.transform.scale(char_back_img, (64, 64))

htcboss_images = [htcboss2, htcboss3]
htcboss_current_img = 0
htcboss_accumulated_time = 0
htcboss_change_interval = 3000

def htcboss_animation():
    global htcboss_current_img, htcboss_accumulated_time
    if not(htcboss_ani):
        screen.blit(htcboss1,(htcboss_x,htcboss_y))
    else:
        htcboss_accumulated_time += clock.get_time()
        if htcboss_accumulated_time >= htcboss_change_interval:
            htcboss_current_img = 1 - htcboss_current_img
            htcboss_accumulated_time = 0
        if htcboss_current_img == 1:
            screen.blit(htcboss_images[htcboss_current_img], (new_htcboss_x, htcboss_y))
        else:
            screen.blit(htcboss_images[htcboss_current_img], (htcboss_x, htcboss_y))

redguy_images = [redguy1_img, redguy2_img]
redguy_current_img = 0
redguy_accumulated_time = 0
redguy_change_interval = 5000

def redguy_animation():
    global redguy_current_img, redguy_accumulated_time, redguy_y
    redguy_accumulated_time += clock.get_time()
    
    if redguy_accumulated_time >= redguy_change_interval:
        redguy_current_img = 1 - redguy_current_img
        redguy_accumulated_time = 0
    
    if redguy_current_img == 1:
        screen.blit(redguy_images[redguy_current_img], (redguy_x, new_redguy_y))
    else:
        screen.blit(redguy_images[redguy_current_img], (redguy_x, redguy_y))

pinkgirl_images = [pinkgirl1_img, pinkgirl2_img]
pinkgirl_current_img = 0
pinkgirl_accumulated_time = 0
pinkgirl_change_interval = 300

def pinkgirl_animation():
    global pinkgirl_current_img, pinkgirl_accumulated_time
    if not(pinkgirl_ani):
        screen.blit(pinkgirl1_img,(pinkgirl_x,pinkgirl_y))
    else:
        pinkgirl_accumulated_time += clock.get_time()
        if pinkgirl_accumulated_time >= pinkgirl_change_interval:
            pinkgirl_current_img = 1 - pinkgirl_current_img
            pinkgirl_accumulated_time = 0
        screen.blit(pinkgirl_images[pinkgirl_current_img], (pinkgirl_x, pinkgirl_y))
     
def redrawGameWindow():
    global walkcount
    global walkcount2

    screen.fill((100,10,210))
    htcboss_animation()
    redguy_animation()
    pinkgirl_animation()
    screen.blit(fatguy_img,(450,100))
    screen.blit(lionguy1_img,(550,100))
    screen.blit(lionguy65_img,(550,200))
    screen.blit(lionguy64_img,(450,200))

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
    exp_system()
    pygame.display.update()


while run:

    clock.tick(27)

    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if key[pygame.K_RETURN]:
            exp += 10
        if key[pygame.K_p]:
            exp += 270

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
        if jumpcount >= -7:
            neg = 1
            if jumpcount <0:
                neg = -1
            y-=(jumpcount ** 2) * 0.4 * neg
            jumpcount -=1
        else:
            Isjump = False
            jumpcount = 7

    if x < htcboss_x + 128 and x > htcboss_x - 128 and y > htcboss_y - 128 and y < htcboss_y + 128:
        htcboss_ani = True
    else:
        htcboss_ani = False

    if x < pinkgirl_x + 128 and x > pinkgirl_x - 128 and y > pinkgirl_y - 128 and y < pinkgirl_y + 128:
        pinkgirl_ani = True
    else:
        pinkgirl_ani = False

    redrawGameWindow()

    

pygame.quit()

""""
    if x < redguy_x + 128 and x > redguy_x - 128 and y > redguy_y - 128 and y < redguy_y + 128:
        redguy_ani = True
    else:
        redguy_ani = False
"""