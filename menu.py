import pygame
import sys

# Цветове
LIGHT_GREEN = (184, 195, 136)
DARK_GREEN = (76, 107, 91)
GREEN = (126, 153, 106)

# Шрифтове
pygame.font.init()
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Функции за рисуване на текст
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Главно меню
def main_menu(start_game):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hat Quest")

    while True:
        screen.fill(LIGHT_GREEN)
        draw_text("Hat Quest", font, DARK_GREEN, screen, 400, 100)

        # Опции за менюто
        play_button = pygame.Rect(300, 200, 200, 50)
        options_button = pygame.Rect(300, 300, 200, 50)
        quit_button = pygame.Rect(300, 400, 200, 50)

        pygame.draw.rect(screen, GREEN, play_button)
        pygame.draw.rect(screen, GREEN, options_button)
        pygame.draw.rect(screen, GREEN, quit_button)

        draw_text("Play", button_font, DARK_GREEN, screen, 400, 225)
        draw_text("Options", button_font, DARK_GREEN, screen, 400, 325)
        draw_text("Quit", button_font, DARK_GREEN, screen, 400, 425)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    start_game()  # Старт
                if options_button.collidepoint(event.pos):
                    options_menu(screen)
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Опциите
def options_menu(screen):
    while True:
        screen.fill(LIGHT_GREEN)
        draw_text("Options", font, DARK_GREEN, screen, 400, 100)

        back_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text("Back", button_font, DARK_GREEN, screen, 400, 425)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Връща към главно меню

        pygame.display.update()
