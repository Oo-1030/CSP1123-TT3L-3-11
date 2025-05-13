import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("gacha_sound.mp3")

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Glow Effect in Center")

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (1280, 720))

font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center = (x, y))
    window.blit(img, text_rect)

def draw_button(text, x, y, w, h, color):
    mouse = pygame.mouse.get_pos()

    pygame.draw.rect(window, color, (x, y, w, h))

    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
    window.blit(text_surf, text_rect)

    return x + w > mouse[0] > x and y + h > mouse[1] > y

def draw_glow_layered(center_x, center_y, radius, alpha, color_base):
    glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for i in range(7):
        current_alpha = max(alpha - i * 5, 0)
        current_radius = radius + i * 5
        color = (*color_base, current_alpha)
        pygame.draw.circle(glow_surface, color, (center_x, center_y), current_radius)
    
    window.blit(glow_surface, (0, 0))

def animation():
    running = True
    effect_triggered = False
    effect_show = False
    effect_alpha = 0
    effect_radius = 0
    effect_center = (width // 2, height // 2)
    effect_color = (0, 0, 0)

    while running:
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if effect_triggered and effect_show:
            window.blit(background_img, (0, 0))

            if effect_alpha > 0:
                draw_glow_layered(effect_center[0], effect_center[1], effect_radius, effect_alpha, effect_color)
                effect_radius += 8
                effect_alpha = max(effect_alpha - 8, 0)

            draw_text("Click anywhere to continue", font, (0, 0, 0,), 640, 650)

            if mouse_clicked:
                    effect_triggered = False
                    effect_show = False
                    effect_alpha = 0
                    effect_radius = 0
                    effect_color = (0, 0, 0)

        else:
            window.fill((255, 255, 255))

            V_hovered = draw_button("V_stars", 240, 550, 200, 100, (200, 30, 30))
            IV_hovered = draw_button("IV_stars", 540, 550, 200, 100, (30, 120, 200))
            III_hovered = draw_button("III_stars", 840, 550, 200, 100, (30, 200, 120))

            if mouse_clicked:
                if V_hovered:
                    effect_triggered = True
                    effect_alpha = 255
                    effect_radius = 0
                    effect_color = (255, 223, 100)
                    pygame.mixer.music.play()
                    effect_show = True
                elif IV_hovered:
                    effect_triggered = True
                    effect_alpha = 255
                    effect_radius = 0
                    effect_color = (200, 160, 255)
                    pygame.mixer.music.play()
                    effect_show = True
                elif III_hovered:
                    effect_triggered = True
                    effect_alpha = 255
                    effect_radius = 0
                    effect_color = (135, 206, 235)
                    pygame.mixer.music.play()
                    effect_show = True

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

animation()