import random
import pygame
import os
import math

npc_path = os.path.join("assets")

npc_assets = {
    "Fat Guy": {
        "name": "Fat Guy",
        "image": pygame.transform.scale(pygame.image.load(os.path.join(npc_path, "fatguyR.png")), (200, 200))
    }
}

def game1(npc_key = None):
    pygame.init()
    pygame.mixer.init()

    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, "assets")
    game_bgm = pygame.mixer.Sound(os.path.join(assets_path, "background_music(rps).mp3"))
    game_channel = pygame.mixer.Channel(1)
    game_channel.play(game_bgm, loops=-1)
    game_channel.set_volume(0.4)
    action_sound = pygame.mixer.Sound(os.path.join(assets_path, "rps.mp3"))
    trigger_sound = pygame.mixer.Sound(os.path.join(assets_path, "trigger.mp3"))
    victory_sound = pygame.mixer.Sound(os.path.join(assets_path, "victory.mp3"))
    defeat_sound = pygame.mixer.Sound(os.path.join(assets_path, "defeat.mp3"))
    sound_channel = None

    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    grey = (128, 128, 128)

    font = pygame.font.SysFont(None, 40)
    large_font = pygame.font.SysFont(None, 60)
    versus_font = pygame.font.SysFont("Impact", 70)

    rock_img = pygame.image.load(os.path.join(assets_path, "rock1.png"))
    paper_img = pygame.image.load(os.path.join(assets_path, "paper2.png"))
    scissors_img = pygame.image.load(os.path.join(assets_path, "scissors3.png"))
    center_img = pygame.image.load(os.path.join(assets_path, "All.png"))
    background_img = pygame.image.load(os.path.join(assets_path, "dtc.png"))
    char_img = pygame.image.load(os.path.join(assets_path, "character.png"))

    img_size = (200, 200)
    rock_img = pygame.transform.scale(rock_img, img_size)
    paper_img = pygame.transform.scale(paper_img, img_size)
    scissors_img = pygame.transform.scale(scissors_img, img_size)

    center_img_size = (960, 350)
    center_img = pygame.transform.scale(center_img, center_img_size)

    background_img_size = (1280, 720)
    background_img = pygame.transform.scale(background_img, background_img_size)

    char_size = (200, 200)
    char_img = pygame.transform.scale(char_img, char_size)

    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        text_rect = img.get_rect(center = (x, y))
        window.blit(img, text_rect)

    def draw_button(text, x, y, w, h, color):
        mouse = pygame.mouse.get_pos()

        pygame.draw.rect(window, color, (x, y, w, h))

        text_surf = font.render(text, True, black)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        window.blit(text_surf, text_rect)

        return x + w > mouse[0] > x and y + h > mouse[1] > y

    def draw_special_box(text, x, y, w, h, color):
        snapshot = window.copy()

        scale = 0.1
        small = pygame.transform.smoothscale(snapshot, (int(window.get_width() * scale), int(window.get_height() * scale)))
        blur = pygame.transform.smoothscale(small, window.get_size())

        window.blit(blur, (0, 0))

        pygame.draw.rect(window, color, (x, y, w, h))

        text_surf = font.render(text, True, black)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        window.blit(text_surf, text_rect)

    def get_round_outcome(player_choice, computer_choice):
        if player_choice == computer_choice:
            return "tie"
        elif (player_choice == "rock" and computer_choice == "scissors"):
            return "player_win"
        elif(player_choice == "paper" and computer_choice == "rock"):
            return "player_win"
        elif(player_choice == "scissors" and computer_choice == "paper"):
            return "player_win"
        else:
            return "computer_win"

    def luck_system(original_choice, luck, player_choice):
        choices = ["rock", "paper", "scissors"]
        total_rerolls = luck // 100
        remaining_luck = luck % 100

        new_choice = original_choice

        for _ in range(total_rerolls):
            new_choice = random.choice(choices)
            outcome = get_round_outcome(player_choice, new_choice)
            if outcome != "computer_win":
                return new_choice

        if remaining_luck > 0 and random.randint(1, 100) <= remaining_luck:
            new_choice = random.choice(choices)
            outcome = get_round_outcome(player_choice, new_choice)
            if outcome != "computer_win":
                return new_choice

        return new_choice

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "saves")
    os.makedirs(save_dir, exist_ok=True)
    coin_path = os.path.join(save_dir, "coins.txt")
    level_path = os.path.join(save_dir, "level.txt")
    exp_path = os.path.join(save_dir, "exp.txt")
    luck_path = os.path.join(save_dir, "luck.txt")

    #load coins
    def load_coins():
        try:
            with open(coin_path, "r") as f:
                return int(f.read())
        except:
            return 0

    def save_coins(coins):
        with open(coin_path, "w") as f:
            f.write(str(coins))

    #load level
    def load_level():
        try:
            with open(level_path, "r") as f:
                return int(f.read())
        except:
            return 1  # Default to level 1 if file doesn't exist

    def save_level(level):
        with open(level_path, "w") as f:
            f.write(str(level))

    #load exp
    def load_exp():
        try:
            with open(exp_path, "r") as f:
                return int(f.read())
        except:
            return 0  # Default to 0 EXP if file doesn't exist

    def save_exp(exp):
        with open(exp_path, "w") as f:
            f.write(str(exp))

    #load luck
    def load_luck():
        try:
            with open(luck_path, "r") as f:
                return int(f.read())
        except:
            return 0  # Default to 0 luck if file doesn't exist

    def save_luck(luck):
        with open(luck_path, "w") as f:
            f.write(str(luck))

    level = 1
    max_exp = 100 * level
    max_level = 20

    font_exp = pygame.font.SysFont('microsoftyahei', 20)

    def exp_system():
        global max_exp, exp, level,luck

        max_exp = 100 * level
        if level < max_level:
            if exp >= max_exp:
                exp_left = exp - max_exp
                exp = exp_left
                level += 1
                luck += 10
                save_luck(luck)
                save_level(level)
        
            ratio = exp / max_exp
            level_text = font_exp.render(f"Level:{level}", True, (255,255,255))
            window.blit(level_text, (55, 685))

            pygame.draw.rect(window,(0,50,255),(135,685,1010,30)) # outline
            pygame.draw.rect(window,(250,250,250),(140,690,1000,20)) # max
            pygame.draw.rect(window,(85,160,255),(140,690,1000*ratio,20)) # ratio

            exp_text = font_exp.render(f"{exp}/{max_exp}",True,(0, 0, 0))
            window.blit(exp_text, (590, 685))

        else:
            level_text = font.render(f"Level:{level}", True, (0,0,0))
            window.blit(level_text, (55, 685))
            exp_text = font.render("max/max",True,(0,0,0))
            window.blit(exp_text, (590, 685))
            pygame.draw.rect(window,(0,50,255),(135,685,1010,30)) # outline
            pygame.draw.rect(window,(85,160,255),(140,690,1000,20)) # ratio
        
        exp_text = font_exp.render(f"Luck:{luck}",True,(255,255,255))
        window.blit(exp_text, (1165,685))

    def game_loop(npc_key):
        global max_exp, exp, level,luck
        level = load_level() 
        exp = load_exp()      
        luck = load_luck()   
        coins = load_coins()
        player_choice = None
        computer_choice = None
        result = None
        player_score = 0
        computer_score = 0
        round_in_progress = False
        luck_triggered = False
        luck_effect_alpha = 0
        luck_effect_radius = 1000
        victory_sound_play = False
        defeat_sound_play = False
        click_handled = False
        playing = True
        add_coins = False
        trigger_sound_play = False
        npc_img = npc_assets[npc_key]["image"]
        npc_name = npc_assets[npc_key]["name"]

        while playing:
            mouse_clicked = False

            window.blit(background_img, (0, 0))
            exp_system()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_level(level)
                    save_exp(exp)
                    save_coins(coins)
                    save_luck(luck)
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            if not round_in_progress:
                center_rect = center_img.get_rect(center = (640, height // 2))
                window.blit(center_img, center_rect)

                draw_text("Score 5 points to win!", large_font, black, width // 2, 80)
                draw_text("Make a choice.", font, black, width // 2, 120)
                rock_button = draw_button ("Rock", 240, 550, 200, 100, red)
                paper_button = draw_button ("Paper", 540, 550, 200, 100, green)
                scissors_button = draw_button ("Scissors", 840, 550, 200, 100, blue)

                if mouse_clicked and not click_handled:
                    if rock_button:
                        player_choice = "rock"
                        round_in_progress = True
                        action_sound.play()
                    elif paper_button:
                        player_choice = "paper"
                        round_in_progress = True
                        action_sound.play()
                    elif scissors_button:
                        player_choice = "scissors"
                        round_in_progress = True
                        action_sound.play()

                    if round_in_progress:
                        computer_choice = random.choice(("rock", "paper", "scissors"))

                        outcome = get_round_outcome(player_choice, computer_choice)
                        if outcome == "computer_win":
                            rerolled_choice = luck_system(computer_choice, luck, player_choice)
                            rerolled_outcome = get_round_outcome(player_choice, rerolled_choice)

                            if rerolled_outcome != "computer_win":
                                computer_choice = rerolled_choice
                                luck_triggered = True
                                luck_effect_alpha = 255
                                luck_effect_radius = 1000

                        click_handled = True

                        if player_choice == computer_choice:
                            result = "It's a tie."
                        elif player_choice == "rock" and computer_choice == "scissors":
                            result = "You Win!"
                            player_score += 1
                        elif player_choice == "paper" and computer_choice == "rock":
                            result = "You Win!"
                            player_score += 1
                        elif player_choice == "scissors" and computer_choice == "paper":
                            result = "You Win!"
                            player_score += 1
                        else:
                            result = f"{npc_name} Win!"
                            computer_score += 1

            else:
                player_img = rock_img if player_choice == "rock" else paper_img if player_choice == "paper" else scissors_img
                player_rect = player_img.get_rect(center = (380, height - 150))
                window.blit(player_img, player_rect)

                computer_img = rock_img if computer_choice == "rock" else paper_img if computer_choice == "paper" else scissors_img
                computer_rect = computer_img.get_rect(center = (width - 380, 220))
                window.blit(computer_img, computer_rect)

                window.blit(char_img, (50, 470))
                window.blit(npc_img, (width - 240, 100))
                draw_text("VS", versus_font, red, width // 2, height // 2)
                draw_text(result, large_font, black, width // 2, 100)

                game_over = player_score >= 5 or computer_score >= 5
                if game_over:
                    if player_score >= 5:
                        draw_special_box("", 256, 285, 768, 150, green)
                        draw_text("Victory!", font, black, width // 2, 320)
                        draw_text("You get 200 coins.", font, black, width // 2, 360)
                        draw_text("You gain 100 exp.", font, black, width // 2, 390)
                        if not add_coins:
                            add_coins = True
                            coins += 200
                            exp += 100
                            save_coins(coins)
                            save_exp(exp)
                        if not victory_sound_play:
                            sound_channel = victory_sound.play()
                            victory_sound_play = True
                        game_result = True
                    elif computer_score >= 5:
                        draw_special_box("", 256, 285, 768, 150, red)
                        draw_text("Defeat...", font, black, width // 2, 320)
                        draw_text("You get 100 coins.", font, black, width // 2, 360)
                        draw_text("You gain 50 exp.", font, black, width // 2, 390)
                        if not add_coins:
                            add_coins = True
                            coins += 100
                            exp += 50
                            save_coins(coins)
                            save_exp(exp)
                        if not defeat_sound_play:
                            sound_channel = defeat_sound.play()
                            defeat_sound_play = True
                        game_result = False
                        
                    draw_text("Click anywhere to continue", font, black, 640, 685)
                    if mouse_clicked and not click_handled:
                        click_handled = True
                        pygame.mixer.stop()
                        save_level(level)
                        save_exp(exp)
                        save_coins(coins)
                        save_luck(luck)
                        return game_result

                else:
                    next_round_button = draw_button("Next Round", 540, 550, 200, 100, grey)
                    if next_round_button and mouse_clicked and not click_handled:
                        player_choice = None
                        computer_choice = None
                        result = None
                        round_in_progress = False
                        luck_triggered = False
                        luck_effect_alpha = 0
                        luck_effect_radius = 1000
                        click_handled = True
                        trigger_sound_play = False
                        add_coins = False

                draw_text(f"Max: {player_score}/5", large_font, black, 100, 420)
                draw_text(f"{npc_name}: {computer_score}/5", large_font, black, width - 120, 50)

            if luck_triggered and luck_effect_alpha > 0:
                gold_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                glow_color = (255, 239, 184, luck_effect_alpha)

                pygame.draw.ellipse(gold_surface, glow_color, (width // 2 - luck_effect_radius, height // 2 - luck_effect_radius, luck_effect_radius * 2, luck_effect_radius * 2))
                window.blit(gold_surface, (0, 0))

                luck_effect_radius += 8
                luck_effect_alpha = max(luck_effect_alpha - 8, 0)

                if not trigger_sound_play:
                    trigger_sound.play()
                    trigger_sound_play = True

            pygame.display.update()

            if not mouse_clicked:
                click_handled = False

        save_level(level)
        save_exp(exp)
        save_coins(coins)
        save_luck(luck)
        return False
    
    return game_loop(npc_key)

def game2(npc_key = None):
    pygame.init()
    pygame.mixer.init()

    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, "assets")
    game_bgm = pygame.mixer.Sound(os.path.join(assets_path, "background_music(dice).mp3"))
    game_channel = pygame.mixer.Channel(1)
    game_channel.play(game_bgm, loops=-1)
    game_channel.set_volume(0.4)
    action_sound = pygame.mixer.Sound(os.path.join(assets_path, "dice_roll.mp3"))
    trigger_sound = pygame.mixer.Sound(os.path.join(assets_path, "trigger.mp3"))
    victory_sound = pygame.mixer.Sound(os.path.join(assets_path, "victory.mp3"))
    defeat_sound = pygame.mixer.Sound(os.path.join(assets_path, "defeat.mp3"))
    sound_channel = None

    width, height = (1280, 720)
    window = pygame.display.set_mode((width, height))

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)

    font = pygame.font.SysFont(None, 40)
    large_font = pygame.font.SysFont(None, 60)
    versus_font = pygame.font.SysFont("Impact", 70)

    img_size = (150, 150)
    dice_img = [
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "1.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "2.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "3.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "4.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "5.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "6.png")), img_size),
    ]
    roll_img = [
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "roll1.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "roll2.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "roll3.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "roll4.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "roll5.png")), img_size),
        pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "roll6.png")), img_size),
    ]

    background_size= (1280, 720)
    background_img = pygame.image.load(os.path.join(assets_path, "mmu_table().png"))
    background_img = pygame.transform.scale(background_img, background_size)

    char_size = (200, 200)
    char_img = pygame.image.load(os.path.join(assets_path, "character.png"))
    char_img = pygame.transform.scale(char_img, char_size)

    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        text_rect = img.get_rect(center = (x, y))
        window.blit(img, text_rect)

    def draw_button(text, x, y, w, h, color):
        mouse = pygame.mouse.get_pos()

        pygame.draw.rect(window, color, (x, y, w, h))

        text_surf = font.render(text, True, black)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        window.blit(text_surf, text_rect)

        return x + w > mouse[0] > x and y + h > mouse[1] > y
    
    def draw_special_box(text, x, y, w, h, color):
        snapshot = window.copy()

        scale = 0.1
        small = pygame.transform.smoothscale(snapshot, (int(window.get_width() * scale), int(window.get_height() * scale)))
        blur = pygame.transform.smoothscale(small, window.get_size())

        window.blit(blur, (0, 0))

        pygame.draw.rect(window, color, (x, y, w, h))

        text_surf = font.render(text, True, black)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        window.blit(text_surf, text_rect)

    def get_round_outcome(player_dice, computer_dice):
        if player_dice > computer_dice:
            return "You Win!"
        elif computer_dice > player_dice:
            return "Computer Win!"
        else:
            return "It's a tie!"
        
    def luck_system(original_dice, luck, player_dice):
        total_rerolls = luck // 100
        remaining_luck = luck % 100

        new_choice = original_dice

        for _ in range(total_rerolls):
            new_choice = random.randint(0, 5)
            outcome = get_round_outcome(player_dice, new_choice)
            if outcome != "Computer Win!":
                return new_choice

        if remaining_luck > 0 and random.randint(1, 100) <= remaining_luck:
            new_choice = random.randint(0, 5)
            outcome = get_round_outcome(player_dice, new_choice)
            if outcome != "Computer Win!":
                return new_choice

        return new_choice

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "saves")
    os.makedirs(save_dir, exist_ok=True)
    coin_path = os.path.join(save_dir, "coins.txt")
    level_path = os.path.join(save_dir, "level.txt")
    exp_path = os.path.join(save_dir, "exp.txt")
    luck_path = os.path.join(save_dir, "luck.txt")

    #load coins
    def load_coins():
        try:
            with open(coin_path, "r") as f:
                return int(f.read())
        except:
            return 0

    def save_coins(coins):
        with open(coin_path, "w") as f:
            f.write(str(coins))

    #load level
    def load_level():
        try:
            with open(level_path, "r") as f:
                return int(f.read())
        except:
            return 1  # Default to level 1 if file doesn't exist

    def save_level(level):
        with open(level_path, "w") as f:
            f.write(str(level))

    #load exp
    def load_exp():
        try:
            with open(exp_path, "r") as f:
                return int(f.read())
        except:
            return 0  # Default to 0 EXP if file doesn't exist

    def save_exp(exp):
        with open(exp_path, "w") as f:
            f.write(str(exp))

    #load luck
    def load_luck():
        try:
            with open(luck_path, "r") as f:
                return int(f.read())
        except:
            return 0  # Default to 0 luck if file doesn't exist

    def save_luck(luck):
        with open(luck_path, "w") as f:
            f.write(str(luck))

    level = 1
    max_exp = 100 * level
    max_level = 20

    font_exp = pygame.font.SysFont('microsoftyahei', 20)

    def exp_system():
        global max_exp, exp, level,luck

        max_exp = 100 * level
        if level < max_level:
            if exp >= max_exp:
                exp_left = exp - max_exp
                exp = exp_left
                level += 1
                luck += 10
                save_luck(luck)
                save_level(level)
        
            ratio = exp / max_exp
            level_text = font_exp.render(f"Level:{level}", True, (255,255,255))
            window.blit(level_text, (55, 685))

            pygame.draw.rect(window,(0,50,255),(135,685,1010,30)) # outline
            pygame.draw.rect(window,(250,250,250),(140,690,1000,20)) # max
            pygame.draw.rect(window,(85,160,255),(140,690,1000*ratio,20)) # ratio

            exp_text = font_exp.render(f"{exp}/{max_exp}",True,(0, 0, 0))
            window.blit(exp_text, (590, 685))

        else:
            level_text = font.render(f"Level:{level}", True, (0,0,0))
            window.blit(level_text, (55, 685))
            exp_text = font.render("max/max",True,(0,0,0))
            window.blit(exp_text, (590, 685))
            pygame.draw.rect(window,(0,50,255),(135,685,1010,30)) # outline
            pygame.draw.rect(window,(85,160,255),(140,690,1000,20)) # ratio
        
        exp_text = font_exp.render(f"Luck:{luck}",True,(255,255,255))
        window.blit(exp_text, (1165,685))

    def game_loop(npc_key):
        global max_exp, exp, level,luck
        level = load_level() 
        exp = load_exp()      
        luck = load_luck()   
        coins = load_coins()
        player_dice = 0
        computer_dice = 0
        player_score = 0
        computer_score = 0
        result = ""
        roll_timer = 0
        roll_duration = 100
        show_result = False
        click_handled = False
        rolling = False
        luck_triggered = False
        luck_effect_alpha = 0
        luck_effect_radius = 1000
        victory_sound_play = False
        defeat_sound_play = False
        playing = True
        add_coins = False
        trigger_sound_play = False
        npc_img = npc_assets[npc_key]["image"]
        npc_name = npc_assets[npc_key]["name"]

        while playing:
            mouse_clicked = False

            window.blit(background_img, (0, 0))
            exp_system()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_level(level)
                    save_exp(exp)
                    save_coins(coins)
                    save_luck(luck)
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            window.blit(char_img, (20, 300))
            window.blit(npc_img, (width - 220, 200))
            draw_text("VS", versus_font, red, width // 2, height // 2)

            if not rolling and not show_result:
                click_button = draw_button("Roll", 540, 550, 200, 100, red)
                draw_text("Score 5 points to win!", large_font, black, width // 2, 80)
                draw_text("Roll the dice.", font, black, width // 2, 120)
                start_rect1 = dice_img[0].get_rect(center = (380, height // 2))
                window.blit(dice_img[0], start_rect1)
                start_rect2 = dice_img[0].get_rect(center = (width - 380, height // 2))
                window.blit(dice_img[0], start_rect2)

                if mouse_clicked and not click_handled:
                    if click_button:
                        rolling = True
                        roll_timer = 0
                        click_handled = True
                        action_sound.play()

            elif rolling:
                roll_timer += 3

                temp_player = random.randint(0, 5)
                temp_computer = random.randint(0, 5)

                player_rect = roll_img[temp_player].get_rect(center = (380, height // 2))
                window.blit(roll_img[temp_player], player_rect)

                computer_rect = roll_img[temp_computer].get_rect(center = (width - 380, height // 2))
                window.blit(roll_img[temp_computer], computer_rect)

                if roll_timer >= roll_duration:
                    rolling = False
                    player_dice = random.randint(0, 5)
                    computer_dice = random.randint(0, 5)

                    outcome = get_round_outcome(player_dice, computer_dice)
                    if outcome == "Computer Win!":
                        rerolled_choice = luck_system(computer_dice, luck, player_dice)
                        rerolled_outcome = get_round_outcome(player_dice, rerolled_choice)

                        if rerolled_outcome != "Computer Win!":
                            computer_dice = rerolled_choice
                            luck_triggered = True
                            luck_effect_alpha = 255
                            luck_effect_radius = 1000
                    
                    if player_dice > computer_dice:
                        result = "You Win!"
                        player_score += 1
                    elif computer_dice > player_dice:
                        result = f"{npc_name} Win!"
                        computer_score += 1
                    else:
                        result = "It's a tie!"

                    show_result = True

            else:
                player_rect = dice_img[player_dice].get_rect(center = (380, height // 2))
                window.blit(dice_img[player_dice], player_rect)

                computer_rect = dice_img[computer_dice].get_rect(center = (width - 380, height // 2))
                window.blit(dice_img[computer_dice], computer_rect)

                draw_text(result, large_font, black, width // 2, 100)

                game_over = player_score >= 5 or computer_score >= 5
                if not game_over:
                    click_button2 = draw_button("Roll Again", 540, 550, 200, 100, red)
                    if click_button2 and mouse_clicked and not click_handled:
                        player_dice = 0
                        computer_dice = 0
                        result = ""
                        roll_timer = 0
                        show_result = False
                        rolling = False
                        click_handled = True
                        luck_triggered = False
                        luck_effect_alpha = 0
                        luck_effect_radius = 1000
                        add_coins = False
                        trigger_sound_play = False

                else:
                    if player_score >= 5:
                        draw_special_box("", 256, 285, 768, 150, green)
                        draw_text("Victory!", font, black, width // 2, 320)
                        draw_text("You get 200 coins.", font, black, width // 2, 360)
                        draw_text("You gain 100 exp.", font, black, width // 2, 390)
                        if not add_coins:
                            add_coins = True
                            coins += 200
                            exp += 100
                            save_coins(coins)
                            save_exp(exp)
                        if not victory_sound_play:
                            victory_sound_play = True
                            sound_channel = victory_sound.play()
                        game_result = True
                    elif computer_score >= 5:
                        draw_special_box("", 256, 285, 768, 150, red)
                        draw_text("Defeat...", font, black, width // 2, 320)
                        draw_text("You get 100 coins.", font, black, width // 2, 360)
                        draw_text("You gain 50 exp.", font, black, width // 2, 390)
                        if not add_coins:
                            add_coins = True
                            coins += 100
                            exp += 50
                            save_coins(coins)
                            save_exp(exp)
                        if not defeat_sound_play:
                            defeat_sound_play = True
                            sound_channel = defeat_sound.play()
                        game_result = False

                    draw_text("Click anywhere to continue", font, black, 640, 685)
                    if mouse_clicked and not click_handled:
                        click_handled = True
                        pygame.mixer.stop()
                        save_level(level)
                        save_exp(exp)
                        save_coins(coins)
                        save_luck(luck)
                        return game_result

                draw_text(f"Max: {player_score}/5", large_font, black, 100, 50)
                draw_text(f"{npc_name}: {computer_score}/5", large_font, black, width - 120, 50)

            if luck_triggered and luck_effect_alpha > 0:
                gold_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                glow_color = (255, 239, 184, luck_effect_alpha)

                pygame.draw.ellipse(gold_surface, glow_color, (width // 2 - luck_effect_radius, height // 2 - luck_effect_radius, luck_effect_radius * 2, luck_effect_radius * 2))
                window.blit(gold_surface, (0, 0))

                luck_effect_radius += 8
                luck_effect_alpha = max(luck_effect_alpha - 8, 0)

                if not trigger_sound_play:
                    trigger_sound.play()
                    trigger_sound_play = True
            
            pygame.display.update()

            if not mouse_clicked:
                click_handled = False

        save_level(level)
        save_exp(exp)
        save_coins(coins)
        save_luck(luck)
        return False
    
    return game_loop(npc_key)

def game3(npc_key = None):
    pygame.init()
    pygame.mixer.init()

    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, "assets")
    game_bgm = pygame.mixer.Sound(os.path.join(assets_path, "background_music(coin).mp3"))
    game_channel = pygame.mixer.Channel(1)
    game_channel.play(game_bgm, loops=-1)
    game_channel.set_volume(0.4)
    action_sound = pygame.mixer.Sound(os.path.join(assets_path, "coin_flip.mp3"))
    trigger_sound = pygame.mixer.Sound(os.path.join(assets_path, "trigger.mp3"))
    victory_sound = pygame.mixer.Sound(os.path.join(assets_path, "victory.mp3"))
    defeat_sound = pygame.mixer.Sound(os.path.join(assets_path, "defeat.mp3"))
    sound_channel = None

    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))

    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    grey = (128, 128, 128)

    font = pygame.font.SysFont(None, 40)
    large_font = pygame.font.SysFont(None, 60)

    head_img = pygame.image.load(os.path.join(assets_path, "head2.png"))
    tail_img = pygame.image.load(os.path.join(assets_path, "tail2.png"))
    spining_img = pygame.image.load(os.path.join(assets_path, "spining2.png"))
    background_img = pygame.image.load(os.path.join(assets_path, "mmu_table().png"))
    char_img = pygame.image.load(os.path.join(assets_path, "character.png"))

    img_size = (350, 350)
    head_img = pygame.transform.scale(head_img, img_size)
    tail_img = pygame.transform.scale(tail_img, img_size)
    spining_img = pygame.transform.scale(spining_img, img_size)

    background_size = (1280, 720)
    background_img = pygame.transform.scale(background_img, background_size)

    char_size = (200, 200)
    char_img = pygame.transform.scale(char_img, char_size)

    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        text_rect = img.get_rect(center = (x, y))
        window.blit(img, text_rect)

    def draw_button(text, x, y, w, h, color):
        mouse = pygame.mouse.get_pos()

        pygame.draw.rect(window, color, (x, y, w, h))

        text_surf = font.render(text, True, black)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        window.blit(text_surf, text_rect)

        return x + w > mouse[0] > x and y + h > mouse[1] > y

    def draw_special_box(text, x, y, w, h, color):
        snapshot = window.copy()

        scale = 0.1
        small = pygame.transform.smoothscale(snapshot, (int(window.get_width() * scale), int(window.get_height() * scale)))
        blur = pygame.transform.smoothscale(small, window.get_size())

        window.blit(blur, (0, 0))

        pygame.draw.rect(window, color, (x, y, w, h))

        text_surf = font.render(text, True, black)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        window.blit(text_surf, text_rect)

    def get_round_outcome(result, player_choice):
        if result == player_choice:
            return "You guessed right!"
        else:
            return "You guessed wrong!"

    def luck_system(original_choice, luck, player_choice):
        choices = ["Head", "Tail"]
        total_rerolls = luck // 100
        remaining_luck = luck % 100

        new_choice = original_choice

        for _ in range(total_rerolls):
            new_choice = random.choice(choices)
            outcome = get_round_outcome(new_choice, player_choice)
            if outcome != "You guessed wrong!":
                return new_choice

        if remaining_luck > 0 and random.randint(1, 100) <= remaining_luck:
            new_choice = random.choice(choices)
            outcome = get_round_outcome(new_choice, player_choice)
            if outcome != "You guessed wrong!":
                return new_choice

        return new_choice

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "saves")
    os.makedirs(save_dir, exist_ok=True)
    coin_path = os.path.join(save_dir, "coins.txt")
    level_path = os.path.join(save_dir, "level.txt")
    exp_path = os.path.join(save_dir, "exp.txt")
    luck_path = os.path.join(save_dir, "luck.txt")

    #load coins
    def load_coins():
        try:
            with open(coin_path, "r") as f:
                return int(f.read())
        except:
            return 0

    def save_coins(coins):
        with open(coin_path, "w") as f:
            f.write(str(coins))

    #load level
    def load_level():
        try:
            with open(level_path, "r") as f:
                return int(f.read())
        except:
            return 1  # Default to level 1 if file doesn't exist

    def save_level(level):
        with open(level_path, "w") as f:
            f.write(str(level))

    #load exp
    def load_exp():
        try:
            with open(exp_path, "r") as f:
                return int(f.read())
        except:
            return 0  # Default to 0 EXP if file doesn't exist

    def save_exp(exp):
        with open(exp_path, "w") as f:
            f.write(str(exp))

    #load luck
    def load_luck():
        try:
            with open(luck_path, "r") as f:
                return int(f.read())
        except:
            return 0  # Default to 0 luck if file doesn't exist

    def save_luck(luck):
        with open(luck_path, "w") as f:
            f.write(str(luck))

    level = 1
    max_exp = 100 * level
    max_level = 20

    font_exp = pygame.font.SysFont('microsoftyahei', 20)

    def exp_system():
        global max_exp, exp, level,luck

        max_exp = 100 * level
        if level < max_level:
            if exp >= max_exp:
                exp_left = exp - max_exp
                exp = exp_left
                level += 1
                luck += 10
                save_luck(luck)
                save_level(level)
        
            ratio = exp / max_exp
            level_text = font_exp.render(f"Level:{level}", True, (255,255,255))
            window.blit(level_text, (55, 685))

            pygame.draw.rect(window,(0,50,255),(135,685,1010,30)) # outline
            pygame.draw.rect(window,(250,250,250),(140,690,1000,20)) # max
            pygame.draw.rect(window,(85,160,255),(140,690,1000*ratio,20)) # ratio

            exp_text = font_exp.render(f"{exp}/{max_exp}",True,(0, 0, 0))
            window.blit(exp_text, (590, 685))

        else:
            level_text = font.render(f"Level:{level}", True, (0,0,0))
            window.blit(level_text, (55, 685))
            exp_text = font.render("max/max",True,(0,0,0))
            window.blit(exp_text, (590, 685))
            pygame.draw.rect(window,(0,50,255),(135,685,1010,30)) # outline
            pygame.draw.rect(window,(85,160,255),(140,690,1000,20)) # ratio
        
        exp_text = font_exp.render(f"Luck:{luck}",True,(255,255,255))
        window.blit(exp_text, (1165,685))

    def game_loop(npc_key):
        global max_exp, exp, level,luck
        level = load_level() 
        exp = load_exp()      
        luck = load_luck()   
        coins = load_coins()
        flipping = False
        result = None
        angle = 0
        spin_speed = 30
        spin_duration = 100
        frame_counter = 0
        player_choice = None
        player_score = 0
        computer_score = 0
        outcome_text = ""
        show_result = False
        luck_triggered = False
        luck_effect_alpha = 0
        luck_effect_radius = 1000
        victory_sound_play = False
        defeat_sound_play = False
        playing = True
        add_coins = False
        trigger_sound_play = False
        npc_img = npc_assets[npc_key]["image"]
        npc_name = npc_assets[npc_key]["name"]
        clock = pygame.time.Clock()

        while playing:
            clock.tick(60)
            mouse_clicked = False

            window.blit(background_img, (0, 0))
            exp_system()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_level(level)
                    save_exp(exp)
                    save_coins(coins)
                    save_luck(luck)
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            window.blit(char_img, (20, 300))
            window.blit(npc_img, (width - 220, 200))

            if not flipping and not show_result:
                draw_text("Score 5 points to win!", large_font, black, width // 2, 80)
                draw_text("Guess Head or Tail.", font, black, width // 2, 120)
                start_rect = head_img.get_rect(center = (width // 2, height // 2))
                window.blit(head_img, start_rect)

                head_button = draw_button("Head", 300, 550, 200, 100, red)
                tail_button = draw_button("Tail", 780, 550, 200, 100, blue)

                if mouse_clicked:
                    if head_button:
                        player_choice = "Head"
                        flipping = True
                        frame_counter = 0
                        action_sound.play()
                    elif tail_button:
                        player_choice = "Tail"
                        flipping = True
                        frame_counter = 0
                        action_sound.play()

            elif flipping:
                angle += spin_speed
                frame_counter += 3

                scale_x = abs(math.cos(math.radians(angle * 1.5)))
                if scale_x < 0.1:
                    scale_x = 0.1

                scaled_width = int(350 * scale_x)
                scaled_coin = pygame.transform.scale(spining_img, (scaled_width, 400))
                coin_rect = scaled_coin.get_rect(center=(width // 2, height // 2))
                window.blit(scaled_coin, coin_rect)

                if frame_counter >= spin_duration:
                    flipping = False
                    result = random.choice(["Head", "Tail"])

                    outcome = get_round_outcome(result, player_choice)
                    if outcome == "You guessed wrong!":
                        rerolled_choice = luck_system(result, luck, player_choice)
                        rerolled_outcome = get_round_outcome(player_choice, rerolled_choice)

                        if rerolled_outcome != "You guessed wrong!":
                            result = rerolled_choice
                            luck_triggered = True
                            luck_effect_alpha = 255
                            luck_effect_radius = 1000
        
                    show_result = True

                    if result == player_choice:
                        outcome_text = "You guessed right!"
                        player_score += 1
                    else:
                        outcome_text = "You guessed wrong!"
                        computer_score += 1

            else:
                result_img = head_img if result == "Head" else tail_img
                result_rect = result_img.get_rect(center=(width // 2, height // 2))
                window.blit(result_img, result_rect)

                draw_text(outcome_text, large_font, black, width // 2, 100)

                game_over = player_score >= 5 or computer_score >= 5
                if game_over:
                    if player_score >= 5:
                        draw_special_box("", 256, 285, 768, 150, green)
                        draw_text("Victory!", font, black, width // 2, 320)
                        draw_text("You get 200 coins.", font, black, width // 2, 360)
                        draw_text("You gain 100 exp.", font, black, width // 2, 390)
                        if not add_coins:
                            add_coins = True
                            coins += 200
                            exp += 100
                            save_coins(coins)
                            save_exp(exp)
                        if not victory_sound_play:
                            victory_sound_play = True
                            sound_channel = victory_sound.play()
                        game_result = True
                    elif computer_score >= 5:
                        draw_special_box("", 256, 285, 768, 150, red)
                        draw_text("Defeat...", font, black, width // 2, 320)
                        draw_text("You get 100 coins.", font, black, width // 2, 360)
                        draw_text("You gain 50 exp.", font, black, width // 2, 390)
                        if not add_coins:
                            add_coins = True
                            coins += 100
                            exp += 50
                            save_coins(coins)
                            save_exp(exp)
                        if not defeat_sound_play:
                            defeat_sound_play = True
                            sound_channel = defeat_sound.play()
                        game_result = False

                    draw_text("Click anywhere to continue", font, black, 640, 685)
                    if mouse_clicked:
                        pygame.mixer.stop()
                        save_level(level)
                        save_exp(exp)
                        save_coins(coins)
                        save_luck(luck)
                        return game_result

                else:
                    next_round_button = draw_button("Flip Again", 540, 550, 200, 100, grey)
                    if next_round_button and mouse_clicked:
                        flipping = False
                        result = None
                        player_choice = None
                        outcome_text = ""
                        show_result = False
                        angle = 0
                        frame_counter = 0
                        luck_triggered = False
                        luck_effect_alpha = 0
                        luck_effect_radius = 1000
                        add_coins = False
                        trigger_sound_play = False

                draw_text(f"Max: {player_score}/5", large_font, black, 100, 50)
                draw_text(f"{npc_name}: {computer_score}/5", large_font, black, width - 120, 50)

            if luck_triggered and luck_effect_alpha > 0:
                gold_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                glow_color = (255, 239, 184, luck_effect_alpha)

                pygame.draw.ellipse(gold_surface, glow_color, (width // 2 - luck_effect_radius, height // 2 - luck_effect_radius, luck_effect_radius * 2, luck_effect_radius * 2))
                window.blit(gold_surface, (0, 0))

                luck_effect_radius += 8
                luck_effect_alpha = max(luck_effect_alpha - 8, 0)

                if not trigger_sound_play:
                    trigger_sound.play()
                    trigger_sound_play = True

            pygame.display.update()

        save_level(level)
        save_exp(exp)
        save_coins(coins)
        save_luck(luck)
        return False
    
    return game_loop(npc_key)

width, height = 1280, 720
window = pygame.display.set_mode((width, height))

base_path = os.path.dirname(__file__)
assets_path = os.path.join(base_path, "assets")
table_png = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "table.png")), (1280, 720))
manga_img_size = (1080, 600)
manga_img = pygame.image.load(os.path.join(assets_path, "fat_tutorial.png"))
manga_img = pygame.transform.scale(manga_img, manga_img_size)

black = (0, 0, 0)
font = pygame.font.SysFont(None, 40)

def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        text_rect = img.get_rect(center = (x, y))
        window.blit(img, text_rect)

def main_game_loop(win_count):
    running = True

    while running:
        if win_count >= 0:
            window.blit(manga_img, (100, 60))

        draw_text("Click anywhere to exit", font, black, 640, 685)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                running = False

def play_all_gamesFG(npc_key):
    win_count = 0
    game_list = [game1, game2, game3]

    for game in game_list:
        game_result = game(npc_key)
        if game_result:
            win_count += 1

    window.blit(table_png, (0, 0))
    pygame.display.update()

    main_game_loop(win_count)