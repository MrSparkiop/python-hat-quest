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

        #Бутончета
        video_button = pygame.Rect(300, 200, 200, 50)
        audio_button = pygame.Rect(300, 300, 200, 50)
        controls_button = pygame.Rect(300, 400, 200, 50)
        back_button = pygame.Rect(300, 500, 200, 50)

        pygame.draw.rect(screen, GREEN, video_button)
        pygame.draw.rect(screen, GREEN, audio_button)
        pygame.draw.rect(screen, GREEN, controls_button)
        pygame.draw.rect(screen, GREEN, back_button)

        draw_text("Video", button_font, DARK_GREEN, screen, 400, 225)
        draw_text("Audio", button_font, DARK_GREEN, screen, 400, 325)
        draw_text("Controls", button_font, DARK_GREEN, screen, 400, 425)
        draw_text("Back", button_font, DARK_GREEN, screen, 400, 525)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if video_button.collidepoint(event.pos):
                    video_menu(screen)  #Video
                if back_button.collidepoint(event.pos):
                    return  # Връща към главно меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Връща към главно меню

        pygame.display.update()

def video_menu(screen):
    fullscreen = False

    while True:
        screen.fill(LIGHT_GREEN)
        draw_text("Video Settings", font, DARK_GREEN, screen, 400, 100)

        # Текст за резолюцията
        draw_text("Resolution: 800x600", button_font, DARK_GREEN, screen, 400, 200)

        # Fullscreen текст и бутон
        draw_text("Fullscreen:", button_font, DARK_GREEN, screen, 300, 300)
        fullscreen_button = pygame.Rect(400, 275, 100, 50)
        pygame.draw.rect(screen, GREEN, fullscreen_button)

        # Текст ON/OFF
        fullscreen_text = "ON" if fullscreen else "OFF"
        draw_text(fullscreen_text, button_font, DARK_GREEN, screen, 450, 300)

        # Back бутон
        back_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text("Back", button_font, DARK_GREEN, screen, 400, 425)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_button.collidepoint(event.pos):
                    fullscreen = not fullscreen  # Превключва ON/OFF
                    if fullscreen:
                        pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((800, 600))
                if back_button.collidepoint(event.pos):
                    return  # Връща към менюто "Options"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Връща към менюто "Options"

        pygame.display.update()

