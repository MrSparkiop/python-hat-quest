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

    # Fullscreen статус
    is_fullscreen = False
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hat Quest")

    while True:
        # Размерите на екрана
        screen_width, screen_height = screen.get_size()

        # Динамично позициониране
        title_y = screen_height // 6
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) // 2
        play_button_y = screen_height // 2 - 100
        options_button_y = screen_height // 2
        quit_button_y = screen_height // 2 + 100

        # Рендиране
        screen.fill(LIGHT_GREEN)
        draw_text("Hat Quest", font, DARK_GREEN, screen, screen_width // 2, title_y)

        play_button = pygame.Rect(button_x, play_button_y, button_width, button_height)
        options_button = pygame.Rect(button_x, options_button_y, button_width, button_height)
        quit_button = pygame.Rect(button_x, quit_button_y, button_width, button_height)

        pygame.draw.rect(screen, GREEN, play_button)
        pygame.draw.rect(screen, GREEN, options_button)
        pygame.draw.rect(screen, GREEN, quit_button)

        draw_text("Play", button_font, DARK_GREEN, screen, screen_width // 2, play_button_y + button_height // 2)
        draw_text("Options", button_font, DARK_GREEN, screen, screen_width // 2, options_button_y + button_height // 2)
        draw_text("Quit", button_font, DARK_GREEN, screen, screen_width // 2, quit_button_y + button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    start_game(is_fullscreen)  # Старт
                if options_button.collidepoint(event.pos):
                    is_fullscreen = options_menu(screen, is_fullscreen)  # Запис
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Опциите
def options_menu(screen, is_fullscreen):
    while True:
        screen_width, screen_height = screen.get_size()  # Размер на екрана

        # Динамично позициониране
        title_y = screen_height // 6
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) // 2
        video_button_y = screen_height // 2 - 150
        audio_button_y = screen_height // 2 - 50
        controls_button_y = screen_height // 2 + 50
        back_button_y = screen_height // 2 + 150

        # Рендиране
        screen.fill(LIGHT_GREEN)
        draw_text("Options", font, DARK_GREEN, screen, screen_width // 2, title_y)

        video_button = pygame.Rect(button_x, video_button_y, button_width, button_height)
        audio_button = pygame.Rect(button_x, audio_button_y, button_width, button_height)
        controls_button = pygame.Rect(button_x, controls_button_y, button_width, button_height)
        back_button = pygame.Rect(button_x, back_button_y, button_width, button_height)

        pygame.draw.rect(screen, GREEN, video_button)
        pygame.draw.rect(screen, GREEN, audio_button)
        pygame.draw.rect(screen, GREEN, controls_button)
        pygame.draw.rect(screen, GREEN, back_button)

        draw_text("Video", button_font, DARK_GREEN, screen, screen_width // 2, video_button_y + button_height // 2)
        draw_text("Audio", button_font, DARK_GREEN, screen, screen_width // 2, audio_button_y + button_height // 2)
        draw_text("Controls", button_font, DARK_GREEN, screen, screen_width // 2, controls_button_y + button_height // 2)
        draw_text("Back", button_font, DARK_GREEN, screen, screen_width // 2, back_button_y + button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if video_button.collidepoint(event.pos):
                    is_fullscreen = video_menu(screen, is_fullscreen)  # Video
                if back_button.collidepoint(event.pos):
                    return is_fullscreen  # Връща към главно меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return is_fullscreen  # Връща към главно меню

        pygame.display.update()


def video_menu(screen, is_fullscreen):
    while True:
        screen_width, screen_height = screen.get_size()  # Размер на екрана

        # Динамично позициониране
        title_y = screen_height // 6
        resolution_text_y = screen_height // 3
        fullscreen_label_y = screen_height // 2
        fullscreen_button_width, fullscreen_button_height = 100, 50
        fullscreen_button_x = screen_width // 2 + 50
        fullscreen_button_y = fullscreen_label_y - fullscreen_button_height // 2
        back_button_width, back_button_height = 200, 50
        back_button_x = (screen_width - back_button_width) // 2
        back_button_y = screen_height // 2 + 100

        # Рендиране
        screen.fill(LIGHT_GREEN)
        draw_text("Video Settings", font, DARK_GREEN, screen, screen_width // 2, title_y)

        # Текст за резолюция
        draw_text("Resolution: 800x600", button_font, DARK_GREEN, screen, screen_width // 2, resolution_text_y)

        # Fullscreen текст и бутон
        draw_text("Fullscreen:", button_font, DARK_GREEN, screen, screen_width // 2 - 100, fullscreen_label_y)
        fullscreen_button = pygame.Rect(fullscreen_button_x, fullscreen_button_y, fullscreen_button_width, fullscreen_button_height)
        pygame.draw.rect(screen, GREEN, fullscreen_button)

        # Текст ON/OFF
        fullscreen_text = "ON" if is_fullscreen else "OFF"
        draw_text(fullscreen_text, button_font, DARK_GREEN, screen,
                  fullscreen_button_x + fullscreen_button_width // 2, fullscreen_button_y + fullscreen_button_height // 2)

        # Back бутон
        back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text("Back", button_font, DARK_GREEN, screen, screen_width // 2, back_button_y + back_button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_button.collidepoint(event.pos):
                    is_fullscreen = not is_fullscreen  # Превключва ON/OFF
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600))
                if back_button.collidepoint(event.pos):
                    return is_fullscreen  # Връща към менюто "Options"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return is_fullscreen  # Връща към менюто "Options"

        pygame.display.update()


