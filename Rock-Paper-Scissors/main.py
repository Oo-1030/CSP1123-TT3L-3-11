import pygame
import random
import os

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("background_music(rps).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)
action_sound = pygame.mixer.Sound("rps.mp3")
trigger_sound = pygame.mixer.Sound("trigger.mp3")
victory_sound = pygame.mixer.Sound("victory.mp3")
defeat_sound = pygame.mixer.Sound("defeat.mp3")
sound_channel = None

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
versus_font = pygame.font.SysFont("Impact", 70)

rock_img = pygame.image.load("rock1.png")
paper_img = pygame.image.load("paper2.png")
scissors_img = pygame.image.load("scissors3.png")
center_img = pygame.image.load("All.png")
background_img = pygame.image.load("dtc.png")
char_img = pygame.image.load("character.png")
npc_img = pygame.image.load("fatguy.png")

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

save_dir = os.path.expanduser(r"~\Project\CSP1123")
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
    coins = load_coins()

    while playing:
        mouse_clicked = False

        window.blit(background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                        luck = 100
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
                        result = "You win!"
                        player_score += 1
                    elif player_choice == "paper" and computer_choice == "rock":
                        result = "You win!"
                        player_score += 1
                    elif player_choice == "scissors" and computer_choice == "paper":
                        result = "You win!"
                        player_score += 1
                    else:
                        result = "NPC win!"
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
                    draw_box("", 256, 285, 768, 150, green)
                    draw_text("Victory!", font, black, width // 2, 320)
                    draw_text("You get 200 coins.", font, black, width // 2, 360)
                    draw_text("You gain 10 exp.", font, black, width // 2, 390)
                    if not add_coins:
                        add_coins = True
                        coins += 200
                        save_coins(coins)
                    draw_text(f"Coins: {coins}", font, black, width - 250, 50)
                    if not victory_sound_play:
                        sound_channel = victory_sound.play()
                        victory_sound_play = True
                elif computer_score >= 5:
                    draw_box("", 256, 285, 768, 150, brown)
                    draw_text("Defeat...", font, black, width // 2, 320)
                    draw_text("You get 100 coins.", font, black, width // 2, 360)
                    draw_text("You gain 5 exp.", font, black, width // 2, 390)
                    if not add_coins:
                        add_coins = True
                        coins += 100
                        save_coins(coins)
                    if not defeat_sound_play:
                        sound_channel = defeat_sound.play()
                        defeat_sound_play = True
                    
                draw_text("Click anywhere to continue", font, black, 640, 650)
                if mouse_clicked and not click_handled:
                    sound_channel.stop()
                    player_score = 0
                    computer_score = 0
                    player_choice = None
                    computer_choice = None
                    result = None
                    round_in_progress = False
                    luck_triggered = False
                    luck_effect_alpha = 0
                    luck_effect_radius = 1000
                    victory_sound_play = False
                    defeat_sound_play = False
                    trigger_sound_play = False
                    click_handled = True
                    add_coins = False
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

            draw_text(f"Max: {player_score}", font, black, 100, 420)
            draw_text(f"NPC: {computer_score}", font, black, width - 120, 50)

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