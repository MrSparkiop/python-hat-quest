import pygame
import os


# Character Class for Animations
class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Load all animations
        self.animations = {
            "Attack_1": self.load_animation("Attack_1.png", 6),
            "Attack_2": self.load_animation("Attack_2.png", 3),
            "Attack_3": self.load_animation("Attack_3.png", 4),
            "Dead": self.load_animation("Dead.png", 4),
            "Hurt": self.load_animation("Hurt.png", 3),
            "Idle": self.load_animation("Idle.png", 8),
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

        # Animation properties
        self.animation_speed = 0.1
        self.time_elapsed = 0

        # Movement and physics
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.5
        self.jump_force = -10
        self.is_jumping = False

    def load_animation(self, filename, frame_count):
        """ Load animation frames correctly from a sprite sheet """
        asset_folder = os.path.join("Asset", "character", filename)
        sprite_sheet = pygame.image.load(asset_folder).convert_alpha()
        frames = []

        # Calculate frame dimensions
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        # Extract each frame without shifting or cropping
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames

    def set_action(self, action):
        """ Switch animation only when the action changes """
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0  # Reset to the first frame
            self.image = self.images[self.image_index]
            self.time_elapsed = 0  # Reset animation timer

    def apply_gravity(self):
        """ Apply gravity to the character """
        self.velocity.y += self.gravity
        if self.rect.bottom >= 300:  # Simulated ground level
            self.rect.bottom = 300
            self.is_jumping = False
            self.velocity.y = 0

    def update(self, keys, dt):
        """ Update character movement and animation """
        # Reset horizontal velocity
        self.velocity.x = 0

        # Movement controls
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.set_action("Walk")
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.set_action("Walk")
        elif keys[pygame.K_SPACE] and not self.is_jumping:  # Jumping
            self.velocity.y = self.jump_force
            self.is_jumping = True
            self.set_action("Jump")
        else:
            # Switch to Idle if no keys are pressed and not jumping
            if not self.is_jumping:
                if self.current_action != "Idle":
                    self.set_action("Idle")
            # Ensure no movement in idle state
            self.velocity.x = 0

            # Update position based on velocity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Apply gravity
        self.apply_gravity()

        # Update animation frames
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
