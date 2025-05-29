import pygame
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("CSP1123-TT3L-3-11/MAP/bgm/background_music(rps).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

action_sound = pygame.mixer.Sound("CSP1123-TT3L-3-11/MAP/bgm/rps.mp3")
trigger_sound = pygame.mixer.Sound("CSP1123-TT3L-3-11/MAP/bgm/trigger.mp3")
victory_sound = pygame.mixer.Sound("CSP1123-TT3L-3-11/MAP/bgm/victory.mp3")
defeat_sound = pygame.mixer.Sound("CSP1123-TT3L-3-11/MAP/bgm/defeat.mp3")
sound_channel = None

width, height = 1280, 720
window = pygame.display.set_mode((width, height))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)
brown = (165, 42, 42)

font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)
versus_font = pygame.font.SysFont("Impact", 70)

rock_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/rock1.png")
paper_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/paper2.png")
scissors_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/scissors3.png")
center_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/All.png")
background_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/dtc.png")
char_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/character.png")
npc_img = pygame.image.load("CSP1123-TT3L-3-11/MAP/images/fatguyR.png")

img_size = (200, 200)
rock_img = pygame.transform.scale(rock_img, img_size)
paper_img = pygame.transform.scale(paper_img, img_size)
scissors_img = pygame.transform.scale(scissors_img, img_size)

center_img = pygame.transform.scale(center_img, (960, 350))
background_img = pygame.transform.scale(background_img, (1280, 720))
char_img = pygame.transform.scale(char_img, (200, 200))
npc_img = pygame.transform.scale(npc_img, (200, 200))

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center=(x, y))
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

def get_round_outcome(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "tie"
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
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
        if get_round_outcome(player_choice, new_choice) != "computer_win":
            return new_choice

    if remaining_luck > 0 and random.randint(1, 100) <= remaining_luck:
        new_choice = random.choice(choices)
        if get_round_outcome(player_choice, new_choice) != "computer_win":
            return new_choice

    return new_choice

class RPS:
    @staticmethod
    def game_loop():
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

        while playing:
            mouse_clicked = False
            window.blit(background_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            if not round_in_progress:
                center_rect = center_img.get_rect(center=(640, height // 2))
                window.blit(center_img, center_rect)
                draw_text("Score 5 points to win!", large_font, black, width // 2, 80)
                draw_text("Make a choice.", font, black, width // 2, 120)
                rock_button = draw_button("Rock", 240, 550, 200, 100, red)
                paper_button = draw_button("Paper", 540, 550, 200, 100, green)
                scissors_button = draw_button("Scissors", 840, 550, 200, 100, blue)

                if mouse_clicked and not click_handled:
                    if rock_button:
                        player_choice = "rock"
                    elif paper_button:
                        player_choice = "paper"
                    elif scissors_button:
                        player_choice = "scissors"

                    if player_choice:
                        round_in_progress = True
                        action_sound.play()
                        computer_choice = random.choice(["rock", "paper", "scissors"])
                        if get_round_outcome(player_choice, computer_choice) == "computer_win":
                            computer_choice = luck_system(computer_choice, 100, player_choice)
                            if get_round_outcome(player_choice, computer_choice) != "computer_win":
                                luck_triggered = True
                                luck_effect_alpha = 255
                                luck_effect_radius = 1000

                        outcome = get_round_outcome(player_choice, computer_choice)
                        if outcome == "tie":
                            result = "It's a tie."
                        elif outcome == "player_win":
                            result = "You win!"
                            player_score += 1
                        else:
                            result = "NPC win!"
                            computer_score += 1
                        click_handled = True
            else:
                player_img = rock_img if player_choice == "rock" else paper_img if player_choice == "paper" else scissors_img
                player_rect = player_img.get_rect(center=(380, height - 150))
                window.blit(player_img, player_rect)

                computer_img = rock_img if computer_choice == "rock" else paper_img if computer_choice == "paper" else scissors_img
                computer_rect = computer_img.get_rect(center=(width - 380, 220))
                window.blit(computer_img, computer_rect)

                window.blit(char_img, (50, 470))
                window.blit(npc_img, (width - 240, 100))
                draw_text("VS", versus_font, red, width // 2, height // 2)
                draw_text(result, large_font, black, width // 2, 100)

                if player_score >= 5 or computer_score >= 5:
                    if player_score >= 5:
                        draw_box("Victory", 160, 310, 960, 100, green)
                        if not victory_sound_play:
                            victory_sound_play = True
                            sound_channel = victory_sound.play()
                    else:
                        draw_box("Defeat", 160, 310, 960, 100, brown)
                        if not defeat_sound_play:
                            defeat_sound_play = True
                            sound_channel = defeat_sound.play()

                    draw_text("Click anywhere to continue", font, black, 640, 650)
                    if mouse_clicked and not click_handled:
                        sound_channel.stop()
                        playing = False  # <== Exit the mini-game and return to main game
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

                draw_text(f"Max: {player_score}", font, black, 100, 420)
                draw_text(f"NPC: {computer_score}", font, black, width - 120, 50)

            if luck_triggered and luck_effect_alpha > 0:
                gold_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.ellipse(gold_surface, (255, 239, 184, luck_effect_alpha),
                                    (width // 2 - luck_effect_radius, height // 2 - luck_effect_radius,
                                     luck_effect_radius * 2, luck_effect_radius * 2))
                window.blit(gold_surface, (0, 0))
                luck_effect_radius += 8
                luck_effect_alpha = max(luck_effect_alpha - 8, 0)
                trigger_sound.play()

            pygame.display.update()
            if not mouse_clicked:
                click_handled = False

# Use this to launch from another script (like DialogueView)
def run():
    RPS.game_loop()