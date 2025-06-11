import pygame
import sys

def show_pause_menu(screen):
    font = pygame.font.SysFont(None, 40)
    button_color = (70, 130, 180)
    hover_color = (100, 149, 237)
    text_color = (255, 255, 255)

    clock = pygame.time.Clock()

    # GUI panel settings
    panel_width = 400
    panel_height = 300
    screen_width, screen_height = screen.get_size()
    panel_rect = pygame.Rect(
        (screen_width - panel_width) // 2,
        (screen_height - panel_height) // 2,
        panel_width,
        panel_height
    )

    def draw_button(rect, text, hovered):
        color = hover_color if hovered else button_color
        pygame.draw.rect(screen, color, rect, border_radius=10)
        txt = font.render(text, True, text_color)
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)

    def draw_main_menu():
        # Button positions relative to panel
        continue_rect = pygame.Rect(panel_rect.x + 100, panel_rect.y + 80, 200, 50)
        exit_rect = pygame.Rect(panel_rect.x + 100, panel_rect.y + 160, 200, 50)

        while True:
            screen.fill((0, 0, 0, 180))  # dim background
            pygame.draw.rect(screen, (50, 50, 50), panel_rect, border_radius=15)

            mouse_pos = pygame.mouse.get_pos()

            draw_button(continue_rect, "Continue Game", continue_rect.collidepoint(mouse_pos))
            draw_button(exit_rect, "Exit Game", exit_rect.collidepoint(mouse_pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_rect.collidepoint(mouse_pos):
                        return
                    elif exit_rect.collidepoint(mouse_pos):
                        confirm_exit()

            pygame.display.flip()
            clock.tick(60)

    def confirm_exit():
        yes_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 180, 100, 50)
        no_rect = pygame.Rect(panel_rect.x + 250, panel_rect.y + 180, 100, 50)

        while True:
            screen.fill((0, 0, 0, 180))  # dim background
            pygame.draw.rect(screen, (50, 50, 50), panel_rect, border_radius=15)

            prompt_text = font.render("Are you sure you want to exit?", True, text_color)
            prompt_rect = prompt_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 100))
            screen.blit(prompt_text, prompt_rect)

            mouse_pos = pygame.mouse.get_pos()
            draw_button(yes_rect, "Yes", yes_rect.collidepoint(mouse_pos))
            draw_button(no_rect, "No", no_rect.collidepoint(mouse_pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif no_rect.collidepoint(mouse_pos):
                        return

            pygame.display.flip()
            clock.tick(60)

    draw_main_menu()