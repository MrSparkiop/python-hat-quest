import pygame
import sys
from menu import main_menu
from character import Character
from environment import Environment

def start_game(is_fullscreen):
    # Initialize screen
    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Environment Demo")

    clock = pygame.time.Clock()

    # Initialize the player and environment
    player = Character((100, 300))
    environment = Environment(screen)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Back to menu

            # Trigger Attack with Left Mouse Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    player.attack()  # Call the attack method

        # Update player
        all_sprites.update(keys, dt)

        # Draw everything
        screen.fill((50, 50, 50))
        environment.draw()  # Draw the environment first
        all_sprites.draw(screen)  # Draw the player on top
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu(start_game)
