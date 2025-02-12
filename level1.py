import pygame
import sys
from menu import level_pause_menu
from enemy import Enemy  # import your Enemy class

def start_level1(screen, player, all_sprites):
    clock = pygame.time.Clock()
    running = True

    # 1) Place Player
    player.rect.topleft = (0, screen.get_height() - player.rect.height)
    all_sprites.add(player)

    # 2) Create an enemy group
    enemy_group = pygame.sprite.Group()
    enemy = Enemy((400, screen.get_height() - 100))  # Example position
    enemy_group.add(enemy)

    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        # 3) Event Loop
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
                if event.button == 1:  # Left mouse = Attack
                    player.attack()
                    attack_width = 40
                    attack_height = player.rect.height

                    # If your Player class has a facing direction:
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

                    # Check collisions with enemies
                    for enemy in enemy_group:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.take_damage(1)

        # 4) Update all sprites (player, etc.)
        keys = pygame.key.get_pressed()
        all_sprites.update(keys, dt)

        # 5) Update enemies (pass player so they can chase/attack)
        enemy_group.update(dt, player)

        # 6) Draw everything
        screen.fill((100, 100, 255))  # same blue background
        all_sprites.draw(screen)
        enemy_group.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
