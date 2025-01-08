import pygame
import sys
import json

from menu import main_menu, pause_menu, options_menu
from character import Character
from environment import Environment
from save_system import save_game, load_game

def start_game(is_fullscreen):
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Environment Demo")

    clock = pygame.time.Clock()

    # Initialize the player and environment
    player = Character((100, 300))
    environment = Environment(screen)
    all_sprites = pygame.sprite.Group(player)

    # progress load
    progress = load_game()
    if progress:
        player.rect.topleft = progress.get("player_position", (100, 300))

    running = True

    while running:
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu(screen)
                    if action == "resume":
                        continue
                    elif action == "options":
                        is_fullscreen = options_menu(screen, is_fullscreen)
                        screen = pygame.display.set_mode((0, 0),
                        pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode((800, 600))
                    elif action == "exit":
                        save_game({"player_position": player.rect.topleft})
                        return
                if event.key == pygame.K_e:
                    for npc in environment.npcs:
                        if player.rect.colliderect(npc.rect):
                            show_dialog(screen, "Hello, adventurer!")
                            chosen_option = show_options(screen, ["Option 1", "Option 2", "Option 3"])
                            print(f"Chosen option: {chosen_option}")

            # Trigger Attack with Left Mouse Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    player.attack() #Call the attack button

        #Update player
        environment.update(dt)
        all_sprites.update(keys, dt)

        #Draw everything
        screen.fill((50, 50, 50))
        environment.draw() #Draw the environment first
        all_sprites.draw(screen) #Draw the player and npc on top
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def show_dialog(screen, text):
    #dialog text with box
    dialog_width = screen.get_width() - 40
    dialog_height = 100
    dialog_x = 20
    dialog_y = screen.get_height() - dialog_height - 20

    font = pygame.font.Font(None, 36)
    dialog_box = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
    pygame.draw.rect(screen, (0, 0, 0), dialog_box)
    pygame.draw.rect(screen, (255, 255, 255), dialog_box, 2)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + dialog_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    pygame.time.wait(2000)  # 2 sec wait

def show_options(screen, options):
    #options for player to choose
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
        screen.fill((0, 0, 0), pygame.Rect(0, dialog_y, screen_width, dialog_height))
        for button_rect, option in buttons:
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
            text_surface = font.render(option, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, option in buttons:
                    if button_rect.collidepoint(event.pos):
                        return option

if __name__ == "__main__":
    main_menu(start_game)
