import sys
import pygame

def dialog_screen(screen, text):
    #window for dialog
    running = True
    while running:
        screen_width, screen_height = screen.get_size()
        dialog_width, dialog_height = screen_width - 100, 150
        dialog_x, dialog_y = 50, screen_height - dialog_height - 50

        # Draw dialog window
        pygame.draw.rect(screen, (50, 50, 50), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, (200, 200, 200), (dialog_x, dialog_y, dialog_width, dialog_height), 5)

        # Render dialog text
        font = pygame.font.Font(None, 36)
        draw_text(text, font, (255, 255, 255), screen, dialog_x + dialog_width // 2, dialog_y + dialog_height // 2)

        # Handle input to exit dialog
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:  # Exit with E or ESC
                    running = False

        pygame.display.update()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
