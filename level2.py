import pygame
import sys
from menu import level_pause_menu, death_screen
from enemy import Enemy

# Screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Floor level: the top of the ground sprite
GROUND_LEVEL = 500

# Gravity constant
GRAVITY = 0.5

class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        # Create a surface from y to the bottom of the screen
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - y))
        self.image.fill((150, 75, 0))  # Brown floor
        self.rect = self.image.get_rect(topleft=(0, y))

def draw_player_health_bar(screen, player):
    """Draw a simple health bar for the player."""
    bar_width = 200
    bar_height = 20
    outline_rect = pygame.Rect(20, 20, bar_width, bar_height)
    health_ratio = player.health / player.max_health
    health_rect = pygame.Rect(20, 20, int(bar_width * health_ratio), bar_height)

    pygame.draw.rect(screen, (255, 0, 0), outline_rect)        # Red background
    pygame.draw.rect(screen, (0, 255, 0), health_rect)           # Green health
    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)   # White border

def start_level2(screen, player, all_sprites):
    """
    Starts Level 2 with an actual floor and boundary checks.
      - A ground sprite is created at y = GROUND_LEVEL.
      - The player and enemies are clamped to stand on this floor.
      - Additionally, horizontal boundary checks prevent running off-screen.
    """
    clock = pygame.time.Clock()
    running = True

    # Load and scale the background image
    background = pygame.image.load("origbig_level2.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create the floor and add it to the overall sprite group
    ground = Ground(GROUND_LEVEL)
    all_sprites.add(ground)

    # Create an enemy group for level2 enemies
    enemy_group = pygame.sprite.Group()

    # Example enemy positions; they start at y=0 and fall due to gravity
    enemy_positions = [
        (400, 0),
        (600, 0),
    ]
    for pos in enemy_positions:
        enemy = Enemy(pos)
        enemy_group.add(enemy)
        all_sprites.add(enemy)

    # Place the player at a starting x position and clamp their bottom to the floor
    player.rect.x = 100
    player.rect.bottom = GROUND_LEVEL
    player.velocity.y = 0

    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        # Check if player died
        if player.health <= 0:
            action = death_screen(screen)
            if action == "respawn":
                player.health = player.max_health
                player.is_dead = False
                player.rect.bottom = GROUND_LEVEL
                player.set_action("Idle")
                player.respawn_invulnerability_timer = 2.0
            else:
                break

        # Event handling
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
                        running = False
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    player.attack()
                    # Create an attack rectangle based on player's facing direction
                    if player.facing_right:
                        attack_rect = pygame.Rect(
                            player.rect.right - 10, player.rect.y, 40, player.rect.height
                        )
                    else:
                        attack_rect = pygame.Rect(
                            player.rect.left - 30, player.rect.y, 40, player.rect.height
                        )
                    # Check collisions with each enemy
                    for enemy in enemy_group:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.take_damage(1)

        keys = pygame.key.get_pressed()

        # --- Update the Player ---
        # Apply gravity to the player
        player.velocity.y += GRAVITY
        player.rect.y += player.velocity.y

        # Let the player's update function handle input/animation
        player.update(keys, dt)

        # Clamp the player to the floor (vertical)
        if player.rect.bottom >= ground.rect.top:
            player.rect.bottom = ground.rect.top
            player.velocity.y = 0
            player.is_jumping = False

        # --- Horizontal Boundary Checks for the Player ---
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # --- Update Enemies ---
        for enemy in enemy_group:
            # Apply gravity to the enemy
            enemy.velocity.y += GRAVITY
            enemy.rect.y += enemy.velocity.y

            # Update enemy AI/animation (passing player if needed)
            enemy.update(dt, player)

            # Clamp the enemy to the floor (vertical)
            if enemy.rect.bottom >= ground.rect.top:
                enemy.rect.bottom = ground.rect.top
                enemy.velocity.y = 0

            # --- Horizontal Boundary Checks for the Enemy ---
            if enemy.rect.left < 0:
                enemy.rect.left = 0
            if enemy.rect.right > SCREEN_WIDTH:
                enemy.rect.right = SCREEN_WIDTH

        # --- Drawing ---
        screen.blit(background, (0, 0))  # Draw the background
        all_sprites.draw(screen)         # Draw all sprites (floor, player, enemies)
        draw_player_health_bar(screen, player)
        pygame.display.flip()

    enemy_group.empty()
