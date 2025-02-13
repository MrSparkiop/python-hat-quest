import pygame
import sys
import json

# Adjust imports based on your actual file structure
from menu import main_menu, pause_menu, options_menu, death_screen, GREEN, LIGHT_GREEN, DARK_GREEN
from character import Character
from environment import Environment
from save_system import save_game, load_game
from dialog import handle_npc_interaction

def draw_health_bar(screen, x, y, health, max_health, bar_width=200, bar_height=20):
    """Draw the player's health bar."""
    border_color = (0, 0, 0)
    background_color = (100, 100, 100)
    health_color = (255, 0, 0)  # Red health bar

    health_ratio = max(health / max_health, 0)
    health_length = int(bar_width * health_ratio)

    pygame.draw.rect(screen, background_color, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, border_color, (x, y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, health_color, (x, y, health_length, bar_height))

def start_game(is_fullscreen):
    # Create the display
    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Environment Demo")

    clock = pygame.time.Clock()

    # Set the ground level so player/enemies share the same floor
    GROUND_LEVEL = 500

    # 1) Initialize the player, placing them so their feet are on GROUND_LEVEL
    player = Character((screen.get_width() // 2, 0))
    player.rect.bottom = GROUND_LEVEL

    # 2) Create or load your environment (which has enemies, NPCs, etc.)
    environment = Environment(screen)

    # Put the player in a group so we can call update/draw easily
    all_sprites = pygame.sprite.Group(player)

    # 3) If there's saved progress, load it and clamp player to GROUND_LEVEL
    progress = load_game()
    if progress:
        player.rect.topleft = progress.get("player_position", (100, 300))
        # Clamp to ground in case the save put us too low
        if player.rect.bottom > GROUND_LEVEL:
            player.rect.bottom = GROUND_LEVEL

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
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
                        if is_fullscreen:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((800, 600))
                    elif action == "exit":
                        save_game({"player_position": player.rect.topleft})
                        return

                if event.key == pygame.K_e:
                    handle_npc_interaction(screen, player, environment.npcs, all_sprites)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    player.attack()
                    # Example attack rect in front of the player
                    attack_rect = pygame.Rect(player.rect.centerx - 20,
                                              player.rect.y,
                                              40,
                                              player.rect.height)
                    # Check collisions with enemies
                    for enemy in environment.enemies:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.take_damage(1)

        # Check if player died
        if player.health <= 0:
            action = death_screen(screen)
            if action == "respawn":
                player.health = player.max_health
                player.is_dead = False
                # Place them back on ground
                player.rect.bottom = GROUND_LEVEL
                player.set_action("Idle")
                player.respawn_invulnerability_timer = 2

        # 4) Update environment (which might update enemies) and update player
        environment.update(dt, player)
        all_sprites.update(keys, dt)

        # 5) Clamp the PLAYER to ground level
        if player.rect.bottom >= GROUND_LEVEL:
            player.rect.bottom = GROUND_LEVEL
            player.velocity.y = 0
            player.is_jumping = False

        # 6) Clamp each ENEMY to ground level as well
        for enemy in environment.enemies:
            # If you store enemy velocity in enemy.velocity.y
            if enemy.rect.bottom >= GROUND_LEVEL:
                enemy.rect.bottom = GROUND_LEVEL
                enemy.velocity.y = 0  # stop falling if you have gravity
                # If your enemy has a jump or is_jumping, also reset it here
                # enemy.is_jumping = False

        # Draw everything
        screen.fill((50, 50, 50))
        environment.draw()           # draws background, NPCs, etc.
        all_sprites.draw(screen)     # draws the player
        draw_health_bar(screen, 20, 20, player.health, player.max_health)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Launch via your main menu
    main_menu(start_game)
