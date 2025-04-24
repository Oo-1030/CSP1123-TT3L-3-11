import pygame
import random

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock, Paper, Scissors")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)
brown = (165, 42, 42)
purple = (186, 85, 211)

font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)

rock_img = pygame.image.load("rock.png")
paper_img = pygame.image.load("paper.png")
scissors_img = pygame.image.load("scissors.png")
center_img = pygame.image.load("All.png")

img_size = (400, 400)
rock_img = pygame.transform.scale(rock_img, img_size)
paper_img = pygame.transform.scale(paper_img, img_size)
scissors_img = pygame.transform.scale(scissors_img, img_size)

center_img_size = (960, 350)
center_img = pygame.transform.scale(center_img, center_img_size)

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

def luck_system(original_choice, luck):
    choices = ["rock", "paper", "scissors"]
    total_rerolls = luck // 100
    remaining_luck = luck % 100

    new_choice = original_choice

    for _ in range(total_rerolls):
        new_choice = random.choice(choices)

    if remaining_luck > 0 and random.randint(1, 100) <= remaining_luck:
        new_choice = random.choice(choices)

    return new_choice

def game_loop():
    player_choice = None
    computer_choice = None
    result = None
    player_score = 0
    computer_score = 0
    round_in_progress = False
    click_handled = False
    playing = True

    while playing:
        mouse_clicked = False

        window.fill(purple)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if not round_in_progress:
            center_rect = center_img.get_rect(center = (640, height // 2))
            window.blit(center_img, center_rect)
                
            rock_button = draw_button ("Rock", 240, 550, 200, 100, red)
            paper_button = draw_button ("Paper", 540, 550, 200, 100, green)
            scissors_button = draw_button ("Scissors", 840, 550, 200, 100, blue)

            if mouse_clicked and not click_handled:
                if rock_button:
                    player_choice = "rock"
                    round_in_progress = True
                elif paper_button:
                    player_choice = "paper"
                    round_in_progress = True
                elif scissors_button:
                    player_choice = "scissors"
                    round_in_progress = True

                if round_in_progress:
                    computer_choice = random.choice(("rock", "paper", "scissors"))
                    click_handled = True

                    luck = 180
                    computer_choice = luck_system(computer_choice, luck)

                    if player_choice == computer_choice:
                        result = "It's a tie."
                    elif (player_choice == "rock" and computer_choice == "scissors"):
                        result = "You win!"
                        player_score += 1
                    elif (player_choice == "paper" and computer_choice == "rock"):
                        result = "You win!"
                        player_score += 1
                    elif (player_choice == "scissors" and computer_choice == "paper"):
                        result = "You win!"
                        player_score += 1
                    else:
                        result = "Computer win!"
                        computer_score += 1

        else:
            player_img = rock_img if player_choice == "rock" else paper_img if player_choice == "paper" else scissors_img
            player_rect = player_img.get_rect(center = (300, height // 2))
            window.blit(player_img, player_rect)

            computer_img = rock_img if computer_choice == "rock" else paper_img if computer_choice == "paper" else scissors_img
            computer_rect = computer_img.get_rect(center = (width - 300, height // 2))
            window.blit(computer_img, computer_rect)

            draw_text(result, large_font, black, width // 2, 100)

            game_over = player_score >= 5 or computer_score >= 5
            if game_over:
                if player_score >= 5:
                    draw_box("Victory", 160, 310, 960, 100, green)
                elif computer_score >= 5:
                    draw_box("Defeat", 160, 310, 960, 100, brown)
                    
                draw_text("Click anywhere to continue", font, black, 640, 650)

                if mouse_clicked and not click_handled:
                    player_score = 0
                    computer_score = 0
                    player_choice = None
                    computer_choice = None
                    result = None
                    round_in_progress = False
                    click_handled = True
            else:
                next_round_button = draw_button("Next Round", 540, 550, 200, 70, grey)
                if next_round_button and mouse_clicked and not click_handled:
                    player_choice = None
                    computer_choice = None
                    result = None
                    round_in_progress = False
                    click_handled = True

        draw_text(f"Player: {player_score}", font, black, 100, 50)
        draw_text(f"Computer: {computer_score}", font, black, width - 120, 50)

        pygame.display.update()

        if not mouse_clicked:
            click_handled = False

    pygame.quit()

game_loop()