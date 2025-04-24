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

def game_loop():
    flipping = False
    result = None
    angle = 0
    spin_speed = 10
    spin_duration = 500
    frame_counter = 0
    player_choice = None
    show_result = False
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
                result = random.choice(("Head", "Tail"))
                show_result = True

        else:
            result_img = head_img if result == "Head" else tail_img
            result_rect = result_img.get_rect(center=(width // 2, height // 2))
            window.blit(result_img, result_rect)

            draw_text(f"Result: {result}", font, black, width // 2, 100)

            if result == player_choice:
                draw_box("You guessed right!", 160, 310, 960, 100, green)
            else:
                draw_box("You guessed wrong!", 160, 310, 960, 100, brown)

            draw_text("Click anywhere to continue", font, black, 640, 650)
            if mouse_clicked:
                flipping = False
                result = None
                show_result = False
                player_choice = None
                angle = 0
                frame_counter = 0

        pygame.display.flip()
    pygame.quit
game_loop()

