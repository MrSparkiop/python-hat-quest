import pygame
import sys
import json

from menu import main_menu, pause_menu, options_menu, GREEN, LIGHT_GREEN, DARK_GREEN
from character import Character
from environment import Environment
from save_system import save_game, load_game
from dialog import dialog_screen, option_screen
from level1 import start_level1
from level2 import start_level2
from level3 import start_level3

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
                            dialog_screen(screen, "Hello, adventurer!")
                            chosen_option = option_screen(screen, ["Level 1", "Level 2", "Level 3"])
                            if chosen_option == "Level 1":
                                start_level1(screen, player)
                            elif chosen_option == "Level 2":
                                start_level2(screen, player)
                            elif chosen_option == "Level 3":
                                start_level3(screen, player)

            # Trigger Attack with Left Mouse Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    player.attack()  # Call the attack method

        #Update player and environment
        environment.update(dt)
        all_sprites.update(keys, dt)

        #Draw everything
        screen.fill((50, 50, 50))
        environment.draw()  # Draw the environment first
        all_sprites.draw(screen)  # Draw the player and npc on top
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu(start_game)
