import pygame
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("background_music(dice).mp3")
pygame.mixer.music.play(-1)

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

img_size = (300, 300)
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

img_size2= (1280, 720)
background = pygame.image.load("table.png")
background = pygame.transform.scale(background, img_size2)

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
        return "You Lose..."
    else:
        return "It's a tie!"
    
def luck_system(original_dice, luck, player_dice):
    total_rerolls = luck // 100
    remaining_luck = luck % 100

    new_choice = original_dice

    for _ in range(total_rerolls):
        new_choice = random.randint(0, 5)
        outcome = get_round_outcome(player_dice, new_choice)
        if outcome != "You Lose...":
            return new_choice

    if remaining_luck > 0 and random.randint(1, 100) <= remaining_luck:
        new_choice = random.randint(0, 5)
        outcome = get_round_outcome(player_dice, new_choice)
        if outcome != "You Lose...":
            return new_choice

    return new_choice

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
    playing = True

    while playing:
        mouse_clicked = False

        window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if not rolling and not show_result:
            click_button = draw_button("Roll", 540, 550, 200, 100, red)
            draw_text("Roll the dice", large_font, black, width // 2, 100)
            start_rect1 = dice_img[0].get_rect(center = (300, height // 2))
            window.blit(dice_img[0], start_rect1)
            start_rect2 = dice_img[0].get_rect(center = (width - 300, height // 2))
            window.blit(dice_img[0], start_rect2)

            if mouse_clicked and not click_handled:
                if click_button:
                    rolling = True
                    roll_timer = 0
                    click_handled = True

        elif rolling:
            roll_timer += 1

            temp_player = random.randint(0, 5)
            temp_computer = random.randint(0, 5)

            player_rect = roll_img[temp_player].get_rect(center = (300, height // 2))
            window.blit(roll_img[temp_player], player_rect)

            computer_rect = roll_img[temp_computer].get_rect(center = (width - 300, height // 2))
            window.blit(roll_img[temp_computer], computer_rect)

            if roll_timer >= roll_duration:
                rolling = False
                player_dice = random.randint(0, 5)
                computer_dice = random.randint(0, 5)

                outcome = get_round_outcome(player_dice, computer_dice)
                if outcome == "You Lose...":
                    luck = 100
                    rerolled_choice = luck_system(computer_dice, luck, player_dice)
                    rerolled_outcome = get_round_outcome(player_dice, rerolled_choice)

                    if rerolled_outcome != "You Lose...":
                        computer_dice = rerolled_choice
                        luck_triggered = True
                        luck_effect_alpha = 255
                        luck_effect_radius = 1000
                
                if player_dice > computer_dice:
                    result = "You Win!"
                    player_score += 1
                elif computer_dice > player_dice:
                    result = "You Lose..."
                    computer_score += 1
                else:
                    result = "It's a tie!"

                show_result = True

        else:
            player_rect = dice_img[player_dice].get_rect(center = (300, height // 2))
            window.blit(dice_img[player_dice], player_rect)

            computer_rect = dice_img[computer_dice].get_rect(center = (width - 300, height // 2))
            window.blit(dice_img[computer_dice], computer_rect)

            draw_text(result, large_font, black, width // 2, 100)

            game_over = player_score >= 3 or computer_score >= 3
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

            else:
                if player_score >= 3:
                    draw_box("Victory", 160, 310, 960, 100, green)
                elif computer_score >= 3:
                    draw_box("Defeat", 160, 310, 960, 100, grey)

                draw_text("Click anywhere to continue", font, black, 640, 650)
                if mouse_clicked and not click_handled:
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

        draw_text(f"Player: {player_score}", font, black, 100, 50)
        draw_text(f"Computer: {computer_score}", font, black, width - 120, 50)

        if luck_triggered and luck_effect_alpha > 0:
            gold_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            glow_color = (255, 239, 184, luck_effect_alpha)

            pygame.draw.ellipse(gold_surface, glow_color, (width // 2 - luck_effect_radius, height // 2 - luck_effect_radius, luck_effect_radius * 2, luck_effect_radius * 2))
            window.blit(gold_surface, (0, 0))

            luck_effect_radius += 6
            luck_effect_alpha = max(luck_effect_alpha - 8, 0)
        
        pygame.display.update()

        if not mouse_clicked:
            click_handled = False

    pygame.quit()

game_loop()


