import pygame
import random
import os

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("background_music(dice).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)
action_sound = pygame.mixer.Sound("dice_roll.mp3")
trigger_sound = pygame.mixer.Sound("trigger.mp3")
victory_sound = pygame.mixer.Sound("victory.mp3")
defeat_sound = pygame.mixer.Sound("defeat.mp3")
sound_channel = None

width, height = (1280, 720)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dice Roll")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (128, 128, 128)

font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)
versus_font = pygame.font.SysFont("Impact", 70)

img_size = (150, 150)
dice_img = [
    pygame.transform.scale(pygame.image.load("1.png"), img_size),
    pygame.transform.scale(pygame.image.load("2.png"), img_size),
    pygame.transform.scale(pygame.image.load("3.png"), img_size),
    pygame.transform.scale(pygame.image.load("4.png"), img_size),
    pygame.transform.scale(pygame.image.load("5.png"), img_size),
    pygame.transform.scale(pygame.image.load("6.png"), img_size),
]
roll_img = [
    pygame.transform.scale(pygame.image.load("roll1.png"), img_size),
    pygame.transform.scale(pygame.image.load("roll2.png"), img_size),
    pygame.transform.scale(pygame.image.load("roll3.png"), img_size),
    pygame.transform.scale(pygame.image.load("roll4.png"), img_size),
    pygame.transform.scale(pygame.image.load("roll5.png"), img_size),
    pygame.transform.scale(pygame.image.load("roll6.png"), img_size),
]

background_size= (1280, 720)
background_img = pygame.image.load("mmu_table().png")
background_img = pygame.transform.scale(background_img, background_size)

char_size = (200, 200)
char_img = pygame.image.load("character.png")
npc_img = pygame.image.load("fatguy.png")
char_img = pygame.transform.scale(char_img, char_size)
npc_img = pygame.transform.scale(npc_img, char_size)

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

def draw_box(text, x, y, w, h, color):
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

save_dir = os.path.join(os.path.expanduser("~"), "Documents", "CSP1123 3-11")
os.makedirs(save_dir, exist_ok=True)
coin_path = os.path.join(save_dir, "coins.txt")

def load_coins():
    try:
        with open(coin_path, "r") as f:
            return int(f.read())
    except:
        return 0

def save_coins(coins):
    with open(coin_path, "w") as f:
        f.write(str(coins))

def game_loop():
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
    coins = load_coins()

    while playing:
        mouse_clicked = False

        window.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        window.blit(char_img, (20, 300))
        window.blit(npc_img, (width - 220, 200))

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
                    luck = 100
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
                    result = "NPC Win!"
                    computer_score += 1
                else:
                    result = "It's a tie!"

                show_result = True

        else:
            player_rect = dice_img[player_dice].get_rect(center = (380, height // 2))
            window.blit(dice_img[player_dice], player_rect)

            computer_rect = dice_img[computer_dice].get_rect(center = (width - 380, height // 2))
            window.blit(dice_img[computer_dice], computer_rect)

            draw_text("VS", versus_font, red, width // 2, height // 2)
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
                    draw_box("", 256, 285, 768, 150, green)
                    draw_text("Victory!", font, black, width // 2, 320)
                    draw_text("You get 200 coins.", font, black, width // 2, 360)
                    draw_text("You gain 100 exp.", font, black, width // 2, 390)
                    if not add_coins:
                        add_coins = True
                        coins += 200
                        save_coins(coins)
                    if not victory_sound_play:
                        victory_sound_play = True
                        sound_channel = victory_sound.play()
                elif computer_score >= 5:
                    draw_box("", 256, 285, 768, 150, red)
                    draw_text("Defeat...", font, black, width // 2, 320)
                    draw_text("You get 100 coins.", font, black, width // 2, 360)
                    draw_text("You gain 50 exp.", font, black, width // 2, 390)
                    if not add_coins:
                        add_coins = True
                        coins += 100
                        save_coins(coins)
                    if not defeat_sound_play:
                        defeat_sound_play = True
                        sound_channel = defeat_sound.play()

                draw_text(f"Coins: {coins}", font, black, width - 350, 50)

                draw_text("Click anywhere to continue", font, black, 640, 650)
                if mouse_clicked and not click_handled:
                    sound_channel.stop()
                    player_dice = 0
                    computer_dice = 0
                    player_score = 0
                    computer_score = 0
                    roll_timer = 0
                    result = ""
                    show_result = False
                    rolling = False
                    click_handled = True
                    luck_triggered = False
                    luck_effect_alpha = 0
                    luck_effect_radius = 1000
                    victory_sound_play = False
                    defeat_sound_play = False
                    add_coins = False
                    trigger_sound_play = False

            draw_text(f"Max: {player_score}", large_font, black, 100, 50)
            draw_text(f"NPC: {computer_score}", large_font, black, width - 120, 50)

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

    pygame.quit()

game_loop()

