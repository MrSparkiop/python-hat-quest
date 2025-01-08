import pygame
import os

class NPC(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Load animations
        self.animations = {
            "Idle": self.load_animation("Idle.png", 5)  # Example: 4 frames in idle animation
        }

        # Default animation setup
        self.current_action = "Idle"
        self.images = self.animations[self.current_action]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=position)

        # Animation properties
        self.animation_speed = 0.2  # Time per frame in seconds
        self.time_elapsed = 0

    def load_animation(self, filename, frame_count):
        #Load animation frames from sprite sheet
        asset_folder = os.path.join("Asset", "npc", filename)
        sprite_sheet = pygame.image.load(asset_folder).convert_alpha()
        frames = []

        # Calculate frame dimensions
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        # Extract frames
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def set_action(self, action):
        #Switch animation only when action changes
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.time_elapsed = 0

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
