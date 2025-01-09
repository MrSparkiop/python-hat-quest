import sys
import pygame

from menu import GREEN, DARK_GREEN, LIGHT_GREEN


def dialog_screen(screen, text):
    # Window for dialog
    dialog_width = screen.get_width() - 40
    dialog_height = 100
    dialog_x = 20
    dialog_y = screen.get_height() - dialog_height - 20

    font = pygame.font.Font(None, 36)
    dialog_box = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
    pygame.draw.rect(screen, GREEN, dialog_box)
    pygame.draw.rect(screen, LIGHT_GREEN, dialog_box, 2)

    text_surface = font.render(text, True, DARK_GREEN)
    text_rect = text_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + dialog_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # Wait for player input to close dialog
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                return

def option_screen(screen, options):
    # Options for player to choose
    screen_width = screen.get_width()
    dialog_height = 150
    dialog_y = screen.get_height() - dialog_height - 20

    font = pygame.font.Font(None, 36)
    button_width = 200
    button_height = 50
    spacing = 20
    button_x_start = (screen_width - (button_width * len(options) + spacing * (len(options) - 1))) // 2

    buttons = []
    for i, option in enumerate(options):
        button_x = button_x_start + i * (button_width + spacing)
        button_y = dialog_y + 50
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        buttons.append((button_rect, option))

    while True:
        screen.fill(GREEN, pygame.Rect(0, dialog_y, screen_width, dialog_height))
        for button_rect, option in buttons:
            pygame.draw.rect(screen, DARK_GREEN, button_rect)
            text_surface = font.render(option, True, (0,0,0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for button_rect, option in buttons:
                    if button_rect.collidepoint(event.pos):
                        return option
