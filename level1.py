import pygame
import sys
from menu import level_pause_menu  # Import pause menu

def start_level1(screen, player, all_sprites):
    clock = pygame.time.Clock()
    running = True

    # Set the player's position to the far left of the screen
    player.rect.topleft = (0, screen.get_height() - player.rect.height)
    all_sprites.add(player)

    while running:
        dt = clock.tick(60) / 1000  # Frame time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = level_pause_menu(screen)  # Open pause menu
                    if action == "resume":
                        continue  # Resume the game
                    elif action == "leave":
                        return  # Leave the level

        # Update all sprites
        all_sprites.update(pygame.key.get_pressed(), dt)

        # Draw everything
        screen.fill((100, 100, 255))  # Blue background for level 1
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
