import pygame
import sys
from menu import level_pause_menu  # Import pause menu

def start_level2(screen, player, all_sprites):
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = level_pause_menu(screen)
                    if action == "resume":
                        continue
                    elif action == "leave":
                        return

        # Update
        all_sprites.update(pygame.key.get_pressed(), dt)

        # Draw
        screen.fill((255, 100, 100))  # Red background
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
