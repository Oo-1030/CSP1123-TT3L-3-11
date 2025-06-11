import pygame
import sys

def show_pause_menu(screen, background_image=None):
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
        # Create a surface with per-pixel alpha for the panel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        # Semi-transparent dark background (last number is alpha: 0-255)
        panel_surface.fill((50, 50, 50, 200))
        
        # Button positions relative to panel
        continue_rect = pygame.Rect(100, 80, 200, 50)
        exit_rect = pygame.Rect(100, 160, 200, 50)

        while True:
            # Draw background image if provided, otherwise use dimmed screen
            if background_image:
                # Scale background image to fit screen if needed
                bg = pygame.transform.scale(background_image, (screen_width, screen_height))
                screen.blit(bg, (0, 0))
            else:
                # Fallback to dimmed background
                dim_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                dim_surface.fill((0, 0, 0, 128))
                screen.blit(dim_surface, (0, 0))
            
            # Draw the semi-transparent panel
            screen.blit(panel_surface, panel_rect)

            mouse_pos = pygame.mouse.get_pos()
            
            # Adjust button positions to screen coordinates
            screen_continue_rect = continue_rect.move(panel_rect.x, panel_rect.y)
            screen_exit_rect = exit_rect.move(panel_rect.x, panel_rect.y)
            
            # Draw buttons directly on screen (not on panel_surface)
            draw_button(screen_continue_rect, "Continue", screen_continue_rect.collidepoint(mouse_pos))
            draw_button(screen_exit_rect, "Exit", screen_exit_rect.collidepoint(mouse_pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if screen_continue_rect.collidepoint(mouse_pos):
                        return
                    elif screen_exit_rect.collidepoint(mouse_pos):
                        confirm_exit()

            pygame.display.flip()
            clock.tick(60)

    def confirm_exit():
        # Create a surface with per-pixel alpha for the panel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        # Semi-transparent dark background
        panel_surface.fill((50, 50, 50, 200))
        
        yes_rect = pygame.Rect(50, 180, 100, 50)
        no_rect = pygame.Rect(250, 180, 100, 50)

        while True:
            # Draw background image if provided
            if background_image:
                bg = pygame.transform.scale(background_image, (screen_width, screen_height))
                screen.blit(bg, (0, 0))
            else:
                # Fallback to dimmed background
                dim_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                dim_surface.fill((0, 0, 0, 128))
                screen.blit(dim_surface, (0, 0))
            
            # Draw the panel
            screen.blit(panel_surface, panel_rect)

            # Draw prompt text
            prompt_text = font.render("Do you want to return to HB2 to rest?", True, text_color)
            prompt_rect = prompt_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 80))
            screen.blit(prompt_text, prompt_rect)
            
            prompt_text2 = font.render("(Exiting will take you back to HB2)", True, text_color)
            prompt_rect2 = prompt_text2.get_rect(center=(panel_rect.centerx, panel_rect.y + 120))
            screen.blit(prompt_text2, prompt_rect2)

            mouse_pos = pygame.mouse.get_pos()
            # Adjust button positions to screen coordinates
            screen_yes_rect = yes_rect.move(panel_rect.x, panel_rect.y)
            screen_no_rect = no_rect.move(panel_rect.x, panel_rect.y)
            
            # Draw buttons
            draw_button(screen_yes_rect, "Yes", screen_yes_rect.collidepoint(mouse_pos))
            draw_button(screen_no_rect, "No", screen_no_rect.collidepoint(mouse_pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if screen_yes_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif screen_no_rect.collidepoint(mouse_pos):
                        return

            pygame.display.flip()
            clock.tick(60)

    draw_main_menu()