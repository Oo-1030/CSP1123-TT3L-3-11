import random
import pygame

image_width = 100
image_height = 100

# 3 star image
Rice_img = pygame.transform.scale(pygame.image.load('Rice2.png'), (image_width, image_height))
Coffee_img = pygame.transform.scale(pygame.image.load('Coffee2.png'), (image_width, image_height))
full_mark_img = pygame.transform.scale(pygame.image.load('Full_mark2.png'), (image_width, image_height))
Eraser_img = pygame.transform.scale(pygame.image.load('Eraser.png'), (image_width, image_height))

# 4 star image
Umbrella_img = pygame.transform.scale(pygame.image.load('Umbrella2.png'), (image_width, image_height))
Coupon_img = pygame.transform.scale(pygame.image.load('Coupon2.png'), (image_width, image_height))
Tissue_img = pygame.transform.scale(pygame.image.load('Tissue.png'), (image_width, image_height))

# 5 star image
Clover_img = pygame.transform.scale(pygame.image.load('Clover2.png'), (image_width, image_height))
Black_card_img = pygame.transform.scale(pygame.image.load('Black_card2.png'), (image_width, image_height))
Underwear_img = pygame.transform.scale(pygame.image.load('Underwear2.png'), (image_width, image_height))
Koi_fish_img = pygame.transform.scale(pygame.image.load('Koi_fish2.png'), (image_width, image_height))

image_map = {
    "Rice": Rice_img,
    "Coffee": Coffee_img,
    "full_mark": full_mark_img,
    "Eraser": Eraser_img,
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
        self.weights = [157, 8.5, 1]
        self.pool = {
            3:["Rice", "Coffee", "full_mark","Eraser"],
            4:["Umbrella", "Coupon","Tissue"],
            5:["Clover","Black_card","Underwear","Koi_fish"]
        }
        self.pity_4 = 0
        self.pity_5 = 0
        self.results = []
        self.screen = screen
        self.pull_remaining = 0
        self.new_pull_started = False

    def set_pull(self, count):
        self.pull_remaining = count 
        self.results.clear()
        self.new_pull_started = False
    

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
            item = random.choice(self.pool[star])
            self.results.append(item)
            self.pull_remaining -= 1
            return item
            
    
    def draw(self):
        x, y = 100, 310
        for item in self.results[-10:]:  
            item_image = image_map[item]
            self.screen.blit(item_image, (x, y))
            x += 110
        




