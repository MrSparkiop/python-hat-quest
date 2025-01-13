import pygame
import os
import random
from npc import NPC

class Environment:
    def __init__(self, screen):
        self.screen = screen
        self.load_assets()
        self.npcs = pygame.sprite.Group()
        self.add_npcs()

    def load_assets(self):
        """Load the background image."""
        asset_folder = os.path.join("Asset", "nature_1")
        self.background = pygame.image.load(os.path.join(asset_folder, "orig.png")).convert()

    def draw(self):
        """Draw the background and NPCs."""
        screen_width, screen_height = self.screen.get_size()

        # Scale the background to fit the entire screen
        background_scaled = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.screen.blit(background_scaled, (0, 0))

        # Draw NPCs
        self.npcs.draw(self.screen)

    def add_npcs(self):
        """Add NPCs to the environment."""
        screen_width, screen_height = self.screen.get_size()
        ground_level = screen_height - 100  # Same ground level as the player
        self.npcs.add(NPC((screen_width // 2 + 100, ground_level - 50)))


    def update(self, dt):
        """Update NPCs in the environment."""
        self.npcs.update(dt)

    def resize(self, new_size):
        """Handle resizing of the screen and adjust the background and NPCs accordingly."""
        self.npcs.empty()
        self.add_npcs()

        for npc in self.npcs:
            npc.rect.bottom = pygame.display.get_surface().get_height() - 100  # Reposition NPC to the new ground level
            npc.velocity.y = 0  # Reset velocity to prevent falling