import pygame
import sys

# colors
LIGHT_GREEN = (184, 195, 136)
DARK_GREEN = (76, 107, 91)
GREEN = (126, 153, 106)

# fonts
pygame.font.init()
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# functions for drawing text on screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# main menu
def main_menu(start_game):
    pygame.init()

    # Fullscreen
    is_fullscreen = False
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hat Quest")

    while True:
        screen_width, screen_height = screen.get_size()
        title_y = screen_height // 6
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) // 2
        play_button_y = screen_height // 2 - 100
        options_button_y = screen_height // 2
        quit_button_y = screen_height // 2 + 100

        # render
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
                    start_game(is_fullscreen)  # start
                if options_button.collidepoint(event.pos):
                    is_fullscreen = options_menu(screen, is_fullscreen)  # save
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# options
def options_menu(screen, is_fullscreen):
    while True:
        screen_width, screen_height = screen.get_size()

        # dynamic positioning
        title_y = screen_height // 6
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) // 2
        video_button_y = screen_height // 2 - 150
        audio_button_y = screen_height // 2 - 50
        controls_button_y = screen_height // 2 + 50
        back_button_y = screen_height // 2 + 150

        # render again
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
                if audio_button.collidepoint(event.pos):
                    audio_menu(screen)  # Audio
                if controls_button.collidepoint(event.pos):
                    controls_menu(screen)  # Controls
                if back_button.collidepoint(event.pos):
                    return is_fullscreen  # back to main menu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return is_fullscreen  # back to main menu

        pygame.display.update()

def video_menu(screen, is_fullscreen):
    while True:
        screen_width, screen_height = screen.get_size()

        # dynamic pos
        title_y = screen_height // 6
        resolution_text_y = screen_height // 3
        fullscreen_label_y = screen_height // 2
        fullscreen_button_width, fullscreen_button_height = 100, 50
        fullscreen_button_x = screen_width // 2 + 50
        fullscreen_button_y = fullscreen_label_y - fullscreen_button_height // 2
        back_button_width, back_button_height = 200, 50
        back_button_x = (screen_width - back_button_width) // 2
        back_button_y = screen_height // 2 + 100

        # render
        screen.fill(LIGHT_GREEN)
        draw_text("Video Settings", font, DARK_GREEN, screen, screen_width // 2, title_y)

        # buttons
        draw_text("Resolution: 800x600", button_font, DARK_GREEN, screen, screen_width // 2, resolution_text_y)

        draw_text("Fullscreen:", button_font, DARK_GREEN, screen, screen_width // 2 - 100, fullscreen_label_y)
        fullscreen_button = pygame.Rect(fullscreen_button_x, fullscreen_button_y, fullscreen_button_width, fullscreen_button_height)
        pygame.draw.rect(screen, GREEN, fullscreen_button)

        fullscreen_text = "ON" if is_fullscreen else "OFF"
        draw_text(fullscreen_text, button_font, DARK_GREEN, screen,
                  fullscreen_button_x + fullscreen_button_width // 2, fullscreen_button_y + fullscreen_button_height // 2)

        back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text("Back", button_font, DARK_GREEN, screen, screen_width // 2, back_button_y + back_button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_button.collidepoint(event.pos):
                    is_fullscreen = not is_fullscreen  # ON/OFF
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600))
                if back_button.collidepoint(event.pos):
                    return is_fullscreen  # back to options

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return is_fullscreen  # back to options

        pygame.display.update()

def audio_menu(screen):
    volume = 50
    dragging = False

    while True:
        screen_width, screen_height = screen.get_size()  #

        # dynamic
        title_y = screen_height // 6
        slider_label_y = screen_height // 3
        slider_y = slider_label_y + 50
        slider_width, slider_height = 300, 20
        slider_x = (screen_width - slider_width) // 2
        handle_width, handle_height = 20, 40
        handle_x = slider_x + (volume / 100) * slider_width - handle_width // 2
        handle_y = slider_y - (handle_height - slider_height) // 2
        back_button_width, back_button_height = 200, 50
        back_button_x = (screen_width - back_button_width) // 2
        back_button_y = screen_height // 2 + 100

        # render
        screen.fill(LIGHT_GREEN)
        draw_text("Audio Settings", font, DARK_GREEN, screen, screen_width // 2, title_y)

        # design
        draw_text(f"Volume: {volume}", button_font, DARK_GREEN, screen, screen_width // 2, slider_label_y)
        pygame.draw.rect(screen, DARK_GREEN, (slider_x, slider_y, slider_width, slider_height))  # Slider background
        pygame.draw.rect(screen, GREEN, (handle_x, handle_y, handle_width, handle_height))  # Slider handle

        # button
        back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text("Back", button_font, DARK_GREEN, screen, screen_width // 2, back_button_y + back_button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # slider code
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if handle_x <= event.pos[0] <= handle_x + handle_width and handle_y <= event.pos[1] <= handle_y + handle_height:
                    dragging = True
                if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y <= event.pos[1] <= slider_y + slider_height:
                    volume = int((event.pos[0] - slider_x) / slider_width * 100)

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x = event.pos[0]
                    volume = int((mouse_x - slider_x) / slider_width * 100)
                    volume = max(0, min(volume, 100))

            #Escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # back to options

        pygame.display.update()

def controls_menu(screen):
    while True:
        screen_width, screen_height = screen.get_size()

        # dynamic
        title_y = screen_height // 6
        text_start_y = screen_height // 3
        text_line_spacing = 40
        back_button_width, back_button_height = 200, 50
        back_button_x = (screen_width - back_button_width) // 2
        back_button_y = screen_height - 100

        # render
        screen.fill(LIGHT_GREEN)
        draw_text("Controls", font, DARK_GREEN, screen, screen_width // 2, title_y)

        # text
        controls_text = [
            "Move Left: A",
            "Move Right: D",
            "Jump: Space",
            "Attack: left mouse button",
            "Interact: E",
            "Back to menu: Escape"
        ]
        for i, line in enumerate(controls_text):
            draw_text(line, button_font, DARK_GREEN, screen, screen_width // 2, text_start_y + i * text_line_spacing)

        # Back
        back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text("Back", button_font, DARK_GREEN, screen, screen_width // 2, back_button_y + back_button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # back options

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # back options

        pygame.display.update()

# pause menu
def pause_menu(screen):
    is_fullscreen = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN

    while True:
        screen_width, screen_height = screen.get_size()
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) // 2
        resume_button_y = screen_height // 2 - 100
        options_button_y = screen_height // 2
        exit_button_y = screen_height // 2 + 100

        screen.fill(LIGHT_GREEN)
        draw_text("Paused", font, DARK_GREEN, screen, screen_width // 2, screen_height // 4.5)

        resume_button = pygame.Rect(button_x, resume_button_y, button_width, button_height)
        options_button = pygame.Rect(button_x, options_button_y, button_width, button_height)
        exit_button = pygame.Rect(button_x, exit_button_y, button_width, button_height)

        pygame.draw.rect(screen, GREEN, resume_button)
        pygame.draw.rect(screen, GREEN, options_button)
        pygame.draw.rect(screen, GREEN, exit_button)

        draw_text("Resume", button_font, DARK_GREEN, screen, screen_width // 2, resume_button_y + button_height // 2)
        draw_text("Options", button_font, DARK_GREEN, screen, screen_width // 2, options_button_y + button_height // 2)
        draw_text("Exit", button_font, DARK_GREEN, screen, screen_width // 2, exit_button_y + button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    return "resume"
                if options_button.collidepoint(event.pos):
                    is_fullscreen = options_menu(screen, is_fullscreen)  # options back
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode((800, 600))
                if exit_button.collidepoint(event.pos):
                    return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

        pygame.display.update()


# Level pause menu
def level_pause_menu(screen):
    """ Pause menu for levels """
    while True:
        screen_width, screen_height = screen.get_size()
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) // 2
        resume_button_y = screen_height // 2 - 100
        options_button_y = screen_height // 2
        leave_button_y = screen_height // 2 + 100

        screen.fill(LIGHT_GREEN)

        # Title
        draw_text("Paused", font, DARK_GREEN, screen, screen_width // 2, screen_height // 4.5)

        # Buttons
        resume_button = pygame.Rect(button_x, resume_button_y, button_width, button_height)
        options_button = pygame.Rect(button_x, options_button_y, button_width, button_height)
        leave_button = pygame.Rect(button_x, leave_button_y, button_width, button_height)

        pygame.draw.rect(screen, GREEN, resume_button)
        pygame.draw.rect(screen, GREEN, options_button)
        pygame.draw.rect(screen, GREEN, leave_button)

        draw_text("Resume", button_font, DARK_GREEN, screen, screen_width // 2, resume_button_y + button_height // 2)
        draw_text("Options", button_font, DARK_GREEN, screen, screen_width // 2, options_button_y + button_height // 2)
        draw_text("Leave Level", button_font, DARK_GREEN, screen, screen_width // 2,
                  leave_button_y + button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    return "resume"
                if options_button.collidepoint(event.pos):
                    options_menu(screen, is_fullscreen=False)
                if leave_button.collidepoint(event.pos):
                    return "leave"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

        pygame.display.update()