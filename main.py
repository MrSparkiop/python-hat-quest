import pygame
import sys
import json

from menu import main_menu, pause_menu, options_menu, GREEN, LIGHT_GREEN, DARK_GREEN
from character import Character
from environment import Environment
from save_system import save_game, load_game
from dialog import handle_npc_interaction

def start_game(is_fullscreen):
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Environment Demo")

    clock = pygame.time.Clock()

    # Initialize the player and environment
    player = Character((screen.get_width() // 2 - 100, screen.get_height() - 100))
    environment = Environment(screen)
    all_sprites = pygame.sprite.Group(player)

    # Progress load
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
                    handle_npc_interaction(screen, player, environment.npcs, all_sprites)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse
                    player.attack()

                    attack_rect = pygame.Rect(player.rect.centerx - 20, player.rect.y, 40, player.rect.height)

                    for enemy in environment.enemies:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.take_damage(1)  # or whichever damage value you prefer
        # Update player and environment
        environment.update(dt, player)
        all_sprites.update(keys, dt)

        # Draw everything
        screen.fill((50, 50, 50))
        environment.draw()  # Draw the environment first
        all_sprites.draw(screen)  # Draw the player and NPCs on top
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu(start_game)