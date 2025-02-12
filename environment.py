import pygame
import os
from npc import NPC
from enemy import Enemy  # <--- import your new Enemy class

class Environment:
    def __init__(self, screen):
        self.screen = screen
        self.load_assets()

        self.npcs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.add_npcs()
        self.add_enemies()

    def load_assets(self):
        # Load your background image
        asset_folder = os.path.join("Asset", "nature_1")
        self.background = pygame.image.load(os.path.join(asset_folder, "orig.png")).convert()

    def add_npcs(self):
        # Example NPC
        screen_width, screen_height = self.screen.get_size()
        ground_level = screen_height - 100
        self.npcs.add(NPC((screen_width // 2 + 100, ground_level - 50)))

    def add_enemies(self):
        # Example enemies
        screen_width, screen_height = self.screen.get_size()
        ground_level = screen_height - 100

        enemy1 = Enemy((300, ground_level - 50))
        enemy2 = Enemy((600, ground_level - 50))
        self.enemies.add(enemy1, enemy2)

    def update(self, dt, player=None):
        # Update NPCs
        self.npcs.update(dt)

        # Update Enemies (pass player so they can chase/attack)
        self.enemies.update(dt, player)

    def draw(self):
        # Scale background to screen, then draw
        screen_width, screen_height = self.screen.get_size()
        background_scaled = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.screen.blit(background_scaled, (0, 0))

        # Draw NPCs & Enemies
        self.npcs.draw(self.screen)
        self.enemies.draw(self.screen)

    def resize(self, new_size):
        self.npcs.empty()
        self.enemies.empty()

        # Re-add NPCs and Enemies so they reposition for the new screen size
        self.add_npcs()
        self.add_enemies()

        for npc in self.npcs:
            npc.rect.bottom = pygame.display.get_surface().get_height() - 100
            npc.velocity.y = 0
        for enemy in self.enemies:
            enemy.rect.bottom = pygame.display.get_surface().get_height() - 100
            enemy.velocity.y = 0
