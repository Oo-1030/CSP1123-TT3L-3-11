import pygame
import random
import time

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock, Paper, Scissors")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)

rock_img = pygame.image.load("rock.png")
paper_img = pygame.image.load("paper.png")
scissors_img = pygame.image.load("scissors.png")

img_size = (500, 500)
rock_img = pygame.transform.scale(rock_img, img_size)
paper_img = pygame.transform.scale(paper_img, img_size)
scissors_img = pygame.transform.scale(scissors_img, img_size)

def draw_text(text, font,color,x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center = (x, y))
    window.blit(img, text_rect)

def draw_button(text, x, y, w, h, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > y and y+h > mouse[1] > y:
        pygame.draw.rect(window, active_color, (x, y, w, h))
    else:
        pygame.draw.rect(window, inactive_color, (x, y, w, h))

    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    window.blit(text_surf, text_rect)

    return x+w > mouse[0] > x and y+h > mouse[1] > y

def game_loop():
    player_choice = None
    computer_choice = None
    result = None
    player_score = 0
    computer_score = 0
    round_in_progress = False

    animation_images = [rock_img, paper_img, scissors_img]
    animation_index = 0
    last_animation_time = time.time()

    click_handled = False

    playing = True

    while playing:
        current_time = time.time()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            window.fill(white)

            if not round_in_progress:
                if current_time - last_animation_time >= 1:
                    animation_index = (animation_index + 1) % 3
                    last_animation_time = current_time

                animation_rect = animation_images[animation_index].get_rect(center = (width // 2, height // 2.5))
                window.blit(animation_images[animation_index], animation_rect)
                
                rock_hover = draw_button ("Rock", 50, 450, 200, 100, red, (255, 100, 100))
                paper_hover = draw_button ("Paper", 300, 450, 200, 100, green, (100, 255, 100))
                scissors_hover = draw_button ("Scissors", 550, 450, 200, 100, blue, (100, 100, 255))

                if mouse_clicked and not click_handled:
                    if rock_hover:
                        player_choice = "rock"
                        round_in_progress = True
                    elif paper_hover:
                        player_choice = "paper"
                        round_in_progress = True
                    elif scissors_hover:
                        player_choice = "scissors"
                        round_in_progress = True

                    if round_in_progress:
                        computer_choice = random.choice(("rock", "paper", "scissors"))
                        click_handled = True

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

        if round_in_progress:
            player_img = rock_img if player_choice == "rock" else paper_img if player_choice == "paper" else scissors_img
            player_rect = player_img.get_rect(center = (200, height // 2))
            window.blit(player_img, player_rect)

            computer_img = rock_img if computer_choice == "rock" else paper_img if computer_choice == "paper" else scissors_img
            computer_rect = computer_img.get_rect(center = (width - 200, height // 2))
            window.blit(computer_img, computer_rect)

            draw_text(result, large_font, black, width // 2, 100)
            next_round_hover = draw_button("Next Round", 300, 500, 200, 70, (200, 200, 200), (150, 150, 150))

            if next_round_hover and mouse_clicked and not click_handled:
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