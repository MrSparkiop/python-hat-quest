import pygame
import sys

def start_level1(screen, player):
    clock = pygame.time.Clock()
    running = True

    # Set player position for level 1
    player.rect.topleft = (100, 300)
    all_sprites = pygame.sprite.Group(player)

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to main game/menu

        # Update
        all_sprites.update(pygame.key.get_pressed(), dt)

        # Draw
        screen.fill((100, 100, 255))  # Blue background
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
