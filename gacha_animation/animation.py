import pygame
import random
from SaveLoadManager import SaveLoadSystem 
from bagsystem import BagSystem


pygame.init()
pygame.mixer.init()

saveloadmanager = SaveLoadSystem(".save", "save_data")
items_saved = saveloadmanager.load_game_data(["items_saved", "pity_4", "pity_5"], [[], 0, 0])[0] or []

pygame.mixer.music.load("gacha_sound.mp3")

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Secret X: Let's Go Gacha!")

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (1280, 720))

Tekun_background_img = pygame.image.load("Tekun_background.png")
Tekun_background_img = pygame.transform.scale(Tekun_background_img, (1280, 720))

image_width = 100
image_height = 100

# 3 star image
Rice_img = pygame.transform.scale(pygame.image.load('Rice.png'), (image_width, image_height))
Coffee_img = pygame.transform.scale(pygame.image.load('Coffee.png'), (image_width, image_height))
Full_mark_img = pygame.transform.scale(pygame.image.load('Full_mark.png'), (image_width, image_height))
Eraser_img = pygame.transform.scale(pygame.image.load('Eraser.png'), (image_width, image_height))
Watch_img = pygame.transform.scale(pygame.image.load('Watch.png'), (image_width, image_height))
Cola_img = pygame.transform.scale(pygame.image.load('Cola.png'), (image_width, image_height))
Calculator_img = pygame.transform.scale(pygame.image.load('Calculaotr.png'), (image_width, image_height))
Cat_img = pygame.transform.scale(pygame.image.load('Cat.png'), (image_width, image_height))
Icecream_img = pygame.transform.scale(pygame.image.load('Icecream.png'), (image_width, image_height))

# 4 star image
Umbrella_img = pygame.transform.scale(pygame.image.load('Umbrella.png'), (image_width, image_height))
Coupon_img = pygame.transform.scale(pygame.image.load('Coupon.png'), (image_width, image_height))
Tissue_img = pygame.transform.scale(pygame.image.load('Tissue.png'), (image_width, image_height))

# 5 star image
Clover_img = pygame.transform.scale(pygame.image.load('Clover.png'), (image_width, image_height))
Black_card_img = pygame.transform.scale(pygame.image.load('Black_card.png'), (image_width, image_height))
Underwear_img = pygame.transform.scale(pygame.image.load('Underwear.png'), (image_width, image_height))
Koi_fish_img = pygame.transform.scale(pygame.image.load('Koi_fish.png'), (image_width, image_height))

One_pull_img = pygame.transform.scale(pygame.image.load('One_pull.png'), (200, 100))
Ten_pull_img = pygame.transform.scale(pygame.image.load('Ten_pull.png'), (200, 100))

item_descriptions = {
    "Rice": "You found the only food can eat in campus, but you also don't want to eat this if you can eat outside.",
    "Coffee": "This coffee give you energy for a day. No sleepy lectures anymore!",
    "Full_mark": "You get 100 mark in exam. This is not luck, is the result of your hardwork!",
    "Eraser": "You don't need to borrow an eraser from your friend anymore. You've got the aura!",
    "Watch": "Imagine wearing this luxury watch as you walk - you'll be the most eye-catching guy in MMU!",
    "Cola":"When you have this on a sunny day, you'll know what heaven feels like.",
    "Calculator":"Your best partner in exam, you know you can't without it.",
    "Cat":"It's so cute that your day brightened when you found it on the way to the lecturer.",
    "Icecream":"On a hot day, having an ice cream is the best treat!",
    "Umbrella": "Imagine you found this on rainy day! It rescue you from becoming a drowned rat.",
    "Coupon": "An MC0 coupon. You can get a 70% discount on buying burger combos with this coupon at any MC0 branch.",
    "Clover": "Only 1/10000 clover has four leafs.You are the lucky one!",
    "Tissue": "Tissue saves you from spilled drinks, sneezing, and crying, you won't know how important it is until you need it.",
    "Black_card": "You found someone's black card and a note beside it reads you can use it however you want!",
    "Underwear": "Not anyone can found a random underwear beside the road of campus, I think you are lucky! (Based on true story)",
    "Koi_fish": "You found this golden fish in the pond in campus. It will bring good luck and wealth to you!"
}

image_map = {
    "Rice": Rice_img,
    "Coffee": Coffee_img,
    "Full_mark": Full_mark_img,
    "Eraser": Eraser_img,
    "Watch": Watch_img,
    "Cola": Cola_img,
    "Calculator": Calculator_img,
    "Cat": Cat_img,
    "Icecream": Icecream_img,
    "Umbrella": Umbrella_img,
    "Coupon": Coupon_img,
    "Clover": Clover_img,
    "Tissue": Tissue_img,
    "Black_card": Black_card_img,
    "Underwear": Underwear_img,
    "Koi_fish": Koi_fish_img
}

class GachaSystem():
    def __init__(self, screen):
        self.stars = [3, 4, 5]
        self.weights = [943, 51, 6] # 5star(0.6%), 4star(5.1%)
        self.pool = {
            3:["Rice", "Coffee", "Full_mark","Eraser","Watch","Cola","Calculator","Cat","Icecream"],
            4:["Umbrella", "Coupon","Tissue"],
            5:["Clover","Black_card","Underwear","Koi_fish"]
        }
        self.pity_4 = saveloadmanager.load_game_data(["pity_4"], [0]) or 0
        self.pity_5 = saveloadmanager.load_game_data(["pity_5"], [0]) or 0
        self.results = []
        self.rect_map = {}
        self.screen = screen
        self.pull_remaining = 0
        self.new_pull_started = False
        self.current_star = None
        self.highest_star_in_pull = None 
        self.one_pull = False
        

    def set_pull(self, count):
        self.pull_remaining = count 
        self.results.clear()
        self.new_pull_started = True
        self.highest_star_in_pull = None
        self.one_pull = False
    
    def pull(self):
        if self.pull_remaining <= 0:
            return None
        
        if self.new_pull_started:
            self.results.clear()
            self.new_pull_started = False
        
        if self.pull_remaining > 0:    
            self.pity_4 += 1
            self.pity_5 += 1
            
            if self.pity_5 >= 90:
                star = 5
                self.pity_5 = 0
                self.pity_4 = 0
            elif self.pity_4 >= 10:
                star = 4
                self.pity_4 = 0
            else:
                star = random.choices(self.stars, weights=self.weights, k=1)[0]
                if star == 5:
                    self.pity_5 = 0
                    self.pity_4 = 0
                elif star == 4:
                    self.pity_4 = 0
            if self.highest_star_in_pull is None or star > self.highest_star_in_pull:
                self.highest_star_in_pull = star
            item = random.choice(self.pool[star])
            self.results.append(item)
            items_saved.append(item)
            self.pull_remaining -= 1
            saveloadmanager.save_game_data([items_saved], ["items_saved"])
            saveloadmanager.save_game_data([items_saved, self.pity_4, self.pity_5], 
                                         ["items_saved", "pity_4", "pity_5"])

            return item
            
    
    def draw(self):
        x, y = 95, 310
        if self.one_pull:
            x = 590
        self.rect_map = {} 
        for item in self.results[-10:]:  
            item_image = image_map[item]
            rect = item_image.get_rect(topleft=(x, y))
            self.screen.blit(item_image, rect) 
            self.rect_map[rect.topleft] = item 
            x += 110

gacha = GachaSystem(window)
bag_system = BagSystem(window,item_descriptions)


font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont("Comic Sans MS", 28)
clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center = (x, y))
    window.blit(img, text_rect)

def draw_wrapped_text(text, font, color, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())
    
    # 计算文本实际需要的最大宽度
    max_line_width = max(font.size(line)[0] for line in lines) if lines else 0
    
    # 计算总高度
    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    
    # 绘制边框背景（调整这些数字来改变边框大小）
    border_padding = 20  # 边框与文字的间距
    border_rect = pygame.Rect(
        x - max_line_width//2 - border_padding,  # 左边位置
        y - border_padding,                      # 上边位置
        max_line_width + border_padding*2,       # 宽度
        total_height + border_padding*2 - 35          # 高度 -35 是为了底部不要留太多白
    )
    
    pygame.draw.rect(window, (255, 255, 255), border_rect)  # 白色背景
    pygame.draw.rect(window, (0, 0, 0), border_rect, 2)     # 黑色边框
    
    # 绘制文本
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, color)
        text_rect = text_surf.get_rect(center=(x, y + i * line_height))
        window.blit(text_surf, text_rect)

def draw_button(text, x, y, w, h, color):
    mouse = pygame.mouse.get_pos()

    pygame.draw.rect(window, color, (x, y, w, h))

    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
    window.blit(text_surf, text_rect)

    return x + w > mouse[0] > x and y + h > mouse[1] > y

def draw_glow_layered(center_x, center_y, radius, alpha, color_base):
    glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for i in range(7):
        current_alpha = max(alpha - i * 5, 0)
        current_radius = radius + i * 5
        color = (*color_base, current_alpha)
        pygame.draw.circle(glow_surface, color, (center_x, center_y), current_radius)
    
    window.blit(glow_surface, (0, 0))

def animation():
    running = True
    effect_triggered = False
    effect_show = False
    effect_alpha = 0
    effect_radius = 0
    effect_center = (width // 2, height // 2)
    effect_color = (0, 0, 0)
    result_displayed = False
    confirm_dialog = None 

    while running:
        mouse_clicked = False
        window.blit(Tekun_background_img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveloadmanager.save_game_data([items_saved], ["items_saved"])
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            if event.type == pygame.KEYDOWN and not(effect_triggered) and not(confirm_dialog):
                if event.key == pygame.K_b:
                    bag_system.open(items_saved)

        if effect_triggered and effect_show:
            window.blit(background_img, (0, 0))
            gacha.draw()
            mouse_pos = pygame.mouse.get_pos()
            description_to_show = None
            for topleft, item in gacha.rect_map.items():
                rect = pygame.Rect(topleft, (image_width, image_height))
                if rect.collidepoint(mouse_pos):
                    description_to_show = item_descriptions.get(item, "")
                    break

            if description_to_show:
                draw_wrapped_text(description_to_show, small_font, (0,0,0), width // 2, 610, 1000)


            if effect_alpha > 0:
                draw_glow_layered(effect_center[0], effect_center[1], effect_radius, effect_alpha, effect_color)
                effect_radius += 8
                effect_alpha = max(effect_alpha - 8, 0)
                
            draw_text("Click anywhere to continue", font, (0, 0, 0,), 640, 550)

            if effect_alpha == 0:
                result_displayed = True

            if mouse_clicked and result_displayed:
                    effect_triggered = False
                    effect_show = False
                    effect_alpha = 0
                    effect_radius = 0
                    effect_color = (0, 0, 0)
                    result_displayed = False

        else:
            One_pull = window.blit(One_pull_img,(240,550))
            
            Ten_pull = window.blit(Ten_pull_img, (840, 550))

            if confirm_dialog:
                overlay = pygame.Surface((width, height))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                window.blit(overlay, (0, 0))

                dialog_rect = pygame.Rect(width//2 - 250, height//2 - 100, 500, 200)
                pygame.draw.rect(window, (255, 255, 255), dialog_rect)
                pygame.draw.rect(window, (0, 0, 0), dialog_rect, 3)

                if confirm_dialog == "one":
                    prompt_text = "Spend 160 M Coins for one pull?"
                else:
                    prompt_text = "Spend 1600 M Coins for ten pulls?"
                draw_text(prompt_text, font, (0, 0, 0), width//2, height//2 - 50)


                confirm_button = pygame.Rect(width//2 - 120, height//2 + 30, 100, 40)
                cancel_button = pygame.Rect(width//2 + 20, height//2 + 30, 100, 40)
                pygame.draw.rect(window, (0, 200, 0), confirm_button)
                pygame.draw.rect(window, (200, 0, 0), cancel_button)

                draw_text("Confirm", font, (255, 255, 255), confirm_button.centerx, confirm_button.centery)
                draw_text("Cancel", font, (255, 255, 255), cancel_button.centerx, cancel_button.centery)


            if mouse_clicked:
                if confirm_dialog:
                    if confirm_button.collidepoint(pygame.mouse.get_pos()):
                        if confirm_dialog == "one":
                            gacha.set_pull(1)
                            gacha.one_pull = True
                        elif confirm_dialog == "ten":
                            gacha.set_pull(10)
                            gacha.one_pull = False
                        confirm_dialog = None  
                    elif cancel_button.collidepoint(pygame.mouse.get_pos()):
                        confirm_dialog = None  
                else:
                    if One_pull.collidepoint(pygame.mouse.get_pos()):
                        confirm_dialog = "one"
                    elif Ten_pull.collidepoint(pygame.mouse.get_pos()):
                        confirm_dialog = "ten"



            if gacha.pull_remaining > 0:
                result = gacha.pull()
                if result and gacha.pull_remaining == 0:
                    if gacha.highest_star_in_pull == 5:
                        effect_triggered = True
                        effect_alpha = 255
                        effect_radius = 0
                        effect_color = (255, 223, 100)
                        pygame.mixer.music.play()
                        effect_show = True
                    elif gacha.highest_star_in_pull == 4:
                        effect_triggered = True
                        effect_alpha = 255
                        effect_radius = 0
                        effect_color = (200, 160, 255)
                        pygame.mixer.music.play()
                        effect_show = True
                    elif gacha.highest_star_in_pull == 3:
                        effect_triggered = True
                        effect_alpha = 255
                        effect_radius = 0
                        effect_color = (135, 206, 235)
                        pygame.mixer.music.play()
                        effect_show = True

        pygame.display.update()
        clock.tick(60)
        

    pygame.quit()

animation()
