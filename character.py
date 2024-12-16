import pygame
import os


# Character Class for Animations
class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.animations = {
            "Attack_1": self.load_animation("Attack_1.png", 6),
            "Attack_2": self.load_animation("Attack_2.png", 3),
            "Attack_3": self.load_animation("Attack_3.png", 4),
            "Dead": self.load_animation("Dead.png", 4),
            "Hurt": self.load_animation("Hurt.png", 3),
            "Idle": self.load_animation("Idle.png", 6),
            "Idle_2": self.load_animation("Idle_2.png", 3),
            "Jump": self.load_animation("Jump.png", 8),
            "Run": self.load_animation("Run.png", 8),
            "Walk": self.load_animation("Walk.png", 8),
        }
        self.current_action = "Idle"
        self.images = self.animations[self.current_action]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=position)

        self.animation_speed = 0.1
        self.time_elapsed = 0
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5

    def load_animation(self, filename, frame_count):
        """ Load animation frames with safe spacing """
        asset_folder = os.path.join("Asset", "character", filename)
        sprite_sheet = pygame.image.load(asset_folder).convert_alpha()
        frames = []
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        for i in range(frame_count):
            # Add a small margin to prevent unwanted pixels
            frame = sprite_sheet.subsurface(
                (i * frame_width + 1, 0, frame_width - 3, frame_height)
            )
            frames.append(frame)
        return frames

    def set_action(self, action):
        """ Switch animation only when the action changes """
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0
            self.image = self.images[self.image_index]

    def update(self, keys, dt):
        """ Handle movement and animation """
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.set_action("Walk")
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.set_action("Walk")
        elif keys[pygame.K_UP]:
            self.velocity.y = -self.speed
            self.set_action("Jump")
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.speed
            self.set_action("Walk")
        else:
            self.set_action("Idle")
            self.image_index = 0  # Stop at the first frame
            self.image = self.images[self.image_index]
            return

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
