import pygame
from sprite import Sprite, Animation
from input import is_key_pressed, keys_down
from camera import camera
from entity import Entity
from label import Label
from physics import Body, triggers
from area import area
from math_ext import distance

movement_speed = 7
message_time_seconds = 3

left = 0
up = 1
right = 2
down = 3
down_frames =  [(0,0), (1,0), (2, 0), (3, 0)]
up_frames =    [(0,1), (1,1), (2, 1), (3, 1)]
right_frames = [(0,2), (1,2), (2, 2), (3, 2)]
left_frames =  [(0,3), (1,3), (2, 3), (3, 3)]
down_still =   [(0,0)]
up_still =     [(0,1)]
right_still =  [(0,2)]
left_still =   [(0,3)]


class Player:
    def __init__(self):
        self.direction = down
        self.is_walking = False
        from engine import engine
        engine.active_objs.append(self)
        self.message_label = Entity(Label("BrunoAce-Regular.ttf", 
                                       area.name)).get(Label)
        

        self.message_label.entity.x = 10
        self.show_message(f"Entering {area.name}")

    def interact(self, mouse_pos):
        from engine import engine
        for usable in engine.usables:
            if usable.entity.has(Sprite):
                usable_sprite = usable.entity.get(Sprite)

                # Get the x, y, width and height of the usable's sprite
                x_sprite = usable.entity.x - camera.x
                y_sprite = usable.entity.y - camera.y
                width_sprite = usable_sprite.image.get_width()
                height_sprite = usable_sprite.image.get_height()

                # Check if the mouse is clicking this
                if x_sprite < mouse_pos[0] < x_sprite + width_sprite and \
                    y_sprite < mouse_pos[1] < y_sprite + height_sprite:

                    # Get our sprite
                    my_sprite = self.entity.get(Sprite)

                    # Calculate the distance between these two sprites, from their feet
                    d = distance(x_sprite + usable_sprite.image.get_width()/2, 
                                 y_sprite + usable_sprite.image.get_height(),
                                 self.entity.x - camera.x + my_sprite.image.get_width()/2,
                                 self.entity.y - camera.y + my_sprite.image.get_height())
                    
                    # Call the usable function
                    usable.on(self.entity, d)

                    # We only want to interact with the first thing we click. 
                    # Return prevents anymore objects being interacted with on this
                    # click
                    return
                
    def show_message(self, message):
        self.message_label.set_text(message)
        self.message_countdown = message_time_seconds * 60

    def walk_animation(self, direction, frame_coords):
        if self.direction != direction:
            self.direction = direction
            self.entity.get(Animation).set_frame_coords(frame_coords)
            self.is_walking = True

    def stop_animation(self):
        a = self.entity.get(Animation)
        self.is_walking = False
        if len(a.frame_coords) != 1:
            if self.direction == left:
                a.set_frame_coords(left_still)
            elif self.direction == right:
                a.set_frame_coords(right_still)
            elif self.direction == down:
                a.set_frame_coords(down_still)
            elif self.direction == up:
                a.set_frame_coords(up_still)

    def update(self):
        if self.message_countdown > 0:
            self.message_countdown -= 1
            if self.message_countdown <= 0:
                self.message_label.set_text("")
        previous_x = self.entity.x
        previous_y = self.entity.y
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)
        future_direction = None
        future_frames = None

        if is_key_pressed(pygame.K_w):
            self.entity.y -= movement_speed
            future_direction = up
            future_frames = up_frames

        if is_key_pressed(pygame.K_s):
            self.entity.y += movement_speed
            future_direction = down
            future_frames = down_frames

        if not body.is_position_valid():
            self.entity.y = previous_y

        from input import is_mouse_just_pressed
        mouse_pos = pygame.mouse.get_pos()
        if is_mouse_just_pressed(1):
            self.interact(mouse_pos)
            
        if is_key_pressed(pygame.K_a):
            self.entity.x -= movement_speed
            future_direction = left
            future_frames = left_frames

        if is_key_pressed(pygame.K_d):
            self.entity.x += movement_speed
            future_direction = right
            future_frames = right_frames

        if is_key_pressed(pygame.K_ESCAPE):
            from gui import show_pause_menu
            screen = pygame.display.get_surface()
            if screen:
                show_pause_menu(screen)
                from input import keys_down, keys_just_pressed, mouse_buttons_down, mouse_buttons_just_pressed
                keys_down.clear()
                keys_just_pressed.clear()
                mouse_buttons_down.clear()
                mouse_buttons_just_pressed.clear()

        if not body.is_position_valid():
            self.entity.x = previous_x
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2

        if is_key_pressed(pygame.K_b):  
            from bagsystem import BagSystem
            from SaveLoadManager import SaveLoadSystem
            screen = pygame.display.get_surface()
            saveloadmanager = SaveLoadSystem(".save", "save_data")
            items_saved = saveloadmanager.load_game_data(["items_saved", "pity_4", "pity_5"], [[], 0, 0])[0] or []

            if screen:
                # Define your item descriptions (you should move this to a config file)
                item_descriptions = {
                    "Rice": "You found the only food can eat in campus, but you also don't want to eat this if you can eat outside.",
                    "Coffee": "This coffee give you energy for a day. No sleepy lectures anymore!",
                    "Full_mark": "You get 100 mark in exam. This is not luck, is the result of your hardwork!",
                    "Eraser": "You don't need to borrow an eraser from your friend anymore. You've got the aura!",
                    "Watch": "Imagine wearing this luxury watch as you walk - you'll be the most eye-catching guy in MMU!",
                    "Cola":"When you have this on a sunny day, you'll know what heaven feels like.",
                    "Calculator": "Your most important parter, you will know it is how important to you in exam! ",
                    "Kitty": "You found this cutie when you going to lecturer class, it shines your day!",
                    "Icecream": "A bite of ice cream on a hot day is one of the most enjoyable things ever!",
                    "Squirrel": "This cutie is not always seen on campus, if you ever seen them, you are lucky!",   
                    "Umbrella": "Imagine you found this on rainy day! It rescue you from becoming a drowned rat.",
                    "Coupon": "An MC0 coupon. You can get a 70% discount on buying burger combos with this coupon at any MC0 branch.",
                    "Clover": "Only 1/10000 clover has four leafs.You are the lucky one!",
                    "Tissue": "Tissue saves you from spilled drinks, sneezing, and crying, you won't know how important it is until you need it.",
                    "Black_card": "You found someone's black card and a note beside it reads you can use it however you want!",
                    "Underwear": "Not anyone can found a random underwear beside the road of campus, I think you are lucky! (Based on true story)",
                    "Koi_fish": "You found this golden fish in the pond in campus. It will bring good luck and wealth to you!"
                }

                bag_system = BagSystem(screen, item_descriptions)
                bag_system.open(items_saved)
                from input import keys_down, keys_just_pressed, mouse_buttons_down, mouse_buttons_just_pressed
                keys_down.clear()
                keys_just_pressed.clear()
                mouse_buttons_down.clear()
                mouse_buttons_just_pressed.clear()


        if future_direction is not None:
            self.walk_animation(future_direction, future_frames)
        elif self.is_walking:
            self.stop_animation()

        for t in triggers:
            if body.is_colliding_with(t):
                t.on(self.entity)

