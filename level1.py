import pygame
import sys
from menu import level_pause_menu, death_screen
from enemy import Enemy

def draw_player_health_bar(screen, player):
    """ Draw the player's health bar at the top left corner """
    bar_width = 200
    bar_height = 20
    outline_rect = pygame.Rect(20, 20, bar_width, bar_height)
    health_ratio = player.health / player.max_health  # Calculate health percentage
    health_rect = pygame.Rect(20, 20, int(bar_width * health_ratio), bar_height)

    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    # Draw health bar
    pygame.draw.rect(screen, RED, outline_rect)  # Background bar
    pygame.draw.rect(screen, GREEN, health_rect)  # Health portion
    pygame.draw.rect(screen, WHITE, outline_rect, 2)  # Outline

def start_level1(screen, player, all_sprites):
    clock = pygame.time.Clock()
    running = True

    # Place Player
    player.rect.topleft = (0, screen.get_height() - player.rect.height)
    all_sprites.add(player)

    # Create an enemy group
    enemy_group = pygame.sprite.Group()
    enemy = Enemy((400, screen.get_height() - 100))
    enemy_group.add(enemy)

    while running:
        dt = clock.tick(60) / 1000.0

        # Check if Player is Dead
        if player.health <= 0:
            action = death_screen(screen)
            if action == "respawn":
                player.health = player.max_health
                player.is_dead = False
                player.rect.topleft = (0, screen.get_height() - player.rect.height)
                player.set_action("Idle")

                # Give 2 seconds of invulnerability after respawn
                player.respawn_invulnerability_timer = 2.0
            else:
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = level_pause_menu(screen)
                    if action == "resume":
                        continue
                    elif action == "leave":
                        return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.attack()
                    attack_width = 40
                    attack_height = player.rect.height

                    if player.facing_right:
                        attack_rect = pygame.Rect(
                            player.rect.right - 10,
                            player.rect.y,
                            attack_width,
                            attack_height
                        )
                    else:
                        attack_rect = pygame.Rect(
                            player.rect.left - (attack_width - 10),
                            player.rect.y,
                            attack_width,
                            attack_height
                        )

                    for enemy in enemy_group:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.take_damage(1)

        keys = pygame.key.get_pressed()
        all_sprites.update(keys, dt)
        enemy_group.update(dt, player)

        screen.fill((100, 100, 255))
        all_sprites.draw(screen)
        enemy_group.draw(screen)

        # Draw Player's Health Bar
        draw_player_health_bar(screen, player)

        pygame.display.flip()

    pygame.quit()
    sys.exit()