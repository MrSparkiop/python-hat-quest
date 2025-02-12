import pygame
import sys
import json

from menu import main_menu, pause_menu, options_menu, GREEN, LIGHT_GREEN, DARK_GREEN
from character import Character
from environment import Environment
from save_system import save_game, load_game
from dialog import handle_npc_interaction

def death_screen(screen):
    """ Display the death screen with a respawn option """
    font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)

    screen_width, screen_height = screen.get_size()
    title_text = font.render("You Died!", True, (255, 0, 0))
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))

    # Buttons
    respawn_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
    exit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 80, 200, 50)

    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(title_text, title_rect)

        # Draw buttons
        pygame.draw.rect(screen, (100, 100, 100), respawn_button)
        pygame.draw.rect(screen, (100, 100, 100), exit_button)

        respawn_text = button_font.render("Respawn", True, (255, 255, 255))
        exit_text = button_font.render("Exit", True, (255, 255, 255))

        screen.blit(respawn_text, respawn_button.move(50, 10))
        screen.blit(exit_text, exit_button.move(70, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if respawn_button.collidepoint(event.pos):
                    return "respawn"  # ✅ Restart the level
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

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

        # ✅ Check if Player Died
        if player.health <= 0:
            action = death_screen(screen)  # Show death screen
            if action == "respawn":
                # ✅ Reset Player's Health & Position
                player.health = player.max_health
                player.is_dead = False
                player.rect.topleft = (screen.get_width() // 2 - 100, screen.get_height() - 100)
                player.set_action("Idle")

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
