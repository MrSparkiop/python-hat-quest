import pygame
import sys
from menu import level_pause_menu, death_screen
from enemy import Enemy

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 40  # Height of the ground
GRAVITY = 0.5

class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        self.image.fill((150, 75, 0))  # Brown ground
        self.rect = self.image.get_rect(topleft=(0, y))

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))  # Placeholder size
        self.image.fill((0, 255, 0))  # Green color for NPC
        self.rect = self.image.get_rect(topleft=(x, y))


def draw_player_health_bar(screen, player):
    bar_width = 200
    bar_height = 20
    outline_rect = pygame.Rect(20, 20, bar_width, bar_height)
    health_ratio = player.health / player.max_health
    health_rect = pygame.Rect(20, 20, int(bar_width * health_ratio), bar_height)
    pygame.draw.rect(screen, (255, 0, 0), outline_rect)
    pygame.draw.rect(screen, (0, 255, 0), health_rect)
    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)


def start_level2(screen, player, all_sprites):
    clock = pygame.time.Clock()
    running = True

    ground_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    npc_group = pygame.sprite.Group()

    # Add ground
    ground = Ground(SCREEN_HEIGHT - GROUND_HEIGHT)
    ground_group.add(ground)
    all_sprites.add(ground)

    # Add enemies on the ground
    enemies = [
        Enemy((200, SCREEN_HEIGHT - GROUND_HEIGHT - 50)),
        Enemy((400, SCREEN_HEIGHT - GROUND_HEIGHT - 50)),
        Enemy((600, SCREEN_HEIGHT - GROUND_HEIGHT - 50))
    ]
    for enemy in enemies:
        enemy_group.add(enemy)
        all_sprites.add(enemy)

    # Add NPC at the far right
    npc = NPC(SCREEN_WIDTH - 80, SCREEN_HEIGHT - GROUND_HEIGHT - 60)
    npc_group.add(npc)
    all_sprites.add(npc)

    # Player starts on the left side
    player.rect.midbottom = (50, SCREEN_HEIGHT - GROUND_HEIGHT)
    player.velocity.y = 0

    while running:
        dt = clock.tick(60) / 1000.0

        if player.health <= 0:
            action = death_screen(screen)
            if action == "respawn":
                player.health = player.max_health
                player.is_dead = False
                player.rect.midbottom = (50, SCREEN_HEIGHT - GROUND_HEIGHT)
                player.set_action("Idle")
                player.respawn_invulnerability_timer = 2.0
            else:
                break  # Exit level

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.attack()
                attack_rect = pygame.Rect(
                    player.rect.right - 10, player.rect.y, 40, player.rect.height
                ) if player.facing_right else pygame.Rect(
                    player.rect.left - 30, player.rect.y, 40, player.rect.height
                )
                for enemy in enemy_group:
                    if attack_rect.colliderect(enemy.rect):
                        enemy.take_damage(1)

        keys = pygame.key.get_pressed()
        player.update(keys, dt)

        # Apply gravity
        player.velocity.y += GRAVITY
        player.rect.y += player.velocity.y

        # Collision detection with ground
        if player.rect.colliderect(ground.rect) and player.velocity.y > 0:
            player.rect.bottom = ground.rect.top
            player.velocity.y = 0

        # Restart player if they fall
        if player.rect.top > SCREEN_HEIGHT:
            player.rect.midbottom = (50, SCREEN_HEIGHT - GROUND_HEIGHT)
            player.velocity.y = 0
            player.set_action("Idle")

        # Update enemies safely
        for enemy in enemy_group:
            if hasattr(player, "rect"):
                enemy.update(dt, player)
            else:
                print("Warning: player is not a valid object")

        # Draw everything
        screen.fill((255, 100, 100))  # Red background for Level 2
        ground_group.draw(screen)
        enemy_group.draw(screen)
        npc_group.draw(screen)
        screen.blit(player.image, player.rect.topleft)
        draw_player_health_bar(screen, player)
        pygame.display.flip()

    # Cleanup after exiting level
    ground_group.empty()
    enemy_group.empty()
    npc_group.empty()
