import pygame
import random
import math

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flip Coin")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
grey = (128, 128, 128)
brown = (165, 42, 42)

font = pygame.font.SysFont(None, 50)

head_img = pygame.image.load("head.png")
tail_img = pygame.image.load("tail.png")
spining_img = pygame.image.load("spining.png")
head_img = pygame.transform.scale(head_img, (400, 400))
tail_img = pygame.transform.scale(tail_img, (400, 400))
spining_img = pygame.transform.scale(spining_img, (400, 400))

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

def game_loop():
    flipping = False
    result = None
    angle = 0
    spin_speed = 10
    spin_duration = 500
    frame_counter = 0
    player_choice = None
    player_score = 0
    computer_score = 0
    outcome_text = ""
    show_result = False
    luck_triggered = False
    luck_effect_alpha = 0
    luck_effect_radius = 1000
    playing = True

    while playing:
        mouse_clicked = False

        window.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if not flipping and not show_result:
            draw_text("Choose Head or Tail", font, black, width // 2, 100)
            start_rect = head_img.get_rect(center = (width // 2, height // 2))
            window.blit(head_img, start_rect)

            head_button = draw_button("Head", 300, 550, 200, 100, red)
            tail_button = draw_button("Tail", 780, 550, 200, 100, blue)

            if mouse_clicked:
                if head_button:
                    player_choice = "Head"
                    flipping = True
                    frame_counter = 0
                elif tail_button:
                    player_choice = "Tail"
                    flipping = True
                    frame_counter = 0

        elif flipping:
            angle += spin_speed
            frame_counter += 1

            scale_x = abs(math.cos(math.radians(angle)))
            if scale_x < 0.1:
                scale_x = 0.1

            scaled_width = int(400 * scale_x)
            scaled_coin = pygame.transform.scale(spining_img, (scaled_width, 400))
            coin_rect = scaled_coin.get_rect(center=(width // 2, height // 2))
            window.blit(scaled_coin, coin_rect)

            if frame_counter >= spin_duration:
                flipping = False
                result = random.choice(["Head", "Tail"])

                outcome = get_round_outcome(result, player_choice)
                if outcome == "You guessed wrong!":
                    luck = 100
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

            draw_text(outcome_text, font, black, width // 2, 100)

            game_over = player_score >= 3 or computer_score >= 3
            if game_over:
                if player_score >= 3:
                    draw_box("Victory", 160, 310, 960, 100, green)
                elif computer_score >= 3:
                    draw_box("Defeat", 160, 310, 960, 100, brown)

                draw_text("Click anywhere to continue", font, black, 640, 650)
                if mouse_clicked:
                    flipping = False
                    result = None
                    player_choice = None
                    player_score = 0
                    computer_score = 0
                    outcome_text = ""
                    show_result = False
                    angle = 0
                    frame_counter = 0
                    luck_triggered = False
                    luck_effect_alpha = 0
                    luck_effect_radius = 1000

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


        draw_text(f"Player: {player_score}", font, black, 100, 50)
        draw_text(f"Computer: {computer_score}", font, black, width - 120, 50)

        if luck_triggered and luck_effect_alpha > 0:
            gold_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            glow_color = (255, 239, 184, luck_effect_alpha)

            pygame.draw.ellipse(gold_surface, glow_color, (width // 2 - luck_effect_radius, height // 2 - luck_effect_radius, luck_effect_radius * 2, luck_effect_radius * 2))
            window.blit(gold_surface, (0, 0))

            luck_effect_radius += 6
            luck_effect_alpha = max(luck_effect_alpha - 8, 0)

        pygame.display.flip()
    pygame.quit
game_loop()
