import pygame
import os

# Character Class for Animations
class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Load all animations
        self.animations = {
            "Attack_1": self.load_animation("Attack_1.png", 6),
            "Idle": self.load_animation("Idle.png", 8),
            "Jump": self.load_animation("Jump.png", 8),
            "Walk": self.load_animation("Walk.png", 8),
        }

        # Default animation setup
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
        self.is_attacking = False  # New: Track if currently attacking
        self.facing_right = True  # ✅ New: Track facing direction

    def load_animation(self, filename, frame_count):
        """ Load animation frames correctly from a sprite sheet """
        asset_folder = os.path.join("Asset", "character", filename)
        sprite_sheet = pygame.image.load(asset_folder).convert_alpha()
        frames = []

        # Calculate frame dimensions
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        # Extract each frame
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def set_action(self, action):
        """ Switch animation only when action changes """
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0  # Reset to the first frame
            self.image = self.images[self.image_index]
            self.time_elapsed = 0  # Reset animation timer

    def attack(self):
        """ Trigger attack animation """
        if not self.is_attacking:
            self.is_attacking = True
            self.set_action("Attack_1")

    def apply_gravity(self):
        """ Apply gravity to the character """
        screen_height = pygame.display.get_surface().get_height()  # Get current screen height
        ground_level = screen_height - 100  # Dynamic ground level

        self.velocity.y += self.gravity
        if self.rect.bottom >= ground_level:  # Check against dynamic ground level
            self.rect.bottom = ground_level
            self.is_jumping = False
            self.velocity.y = 0

    def update(self, keys, dt):
        """ Update character movement, jumping, and attacks """
        screen_height = pygame.display.get_surface().get_height()  # Get current screen height
        ground_level = screen_height - 100  # Dynamic ground level

        # Handle attack animation
        if self.is_attacking:
            self.time_elapsed += dt
            if self.time_elapsed >= self.animation_speed:
                self.time_elapsed = 0
                self.image_index += 1

                if self.image_index >= len(self.images):  # Attack animation ends
                    self.image_index = 0
                    self.is_attacking = False
                    self.set_action("Idle")
                else:
                    self.image = self.images[self.image_index]
            return  # Skip further updates if attacking

        # Reset horizontal velocity
        self.velocity.x = 0

        # Prioritize Jumping First
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity.y = self.jump_force
            self.is_jumping = True
            self.set_action("Jump")

        # Handle Movement if Not Jumping
        if keys[pygame.K_a]:  # Move left
            self.velocity.x = -self.speed
            self.facing_right = False  # ✅ Set facing direction
            if not self.is_jumping:
                self.set_action("Walk")
        elif keys[pygame.K_d]:  # Move right
            self.velocity.x = self.speed
            self.facing_right = True  # ✅ Set facing direction
            if not self.is_jumping:
                self.set_action("Walk")
        else:
            if not self.is_jumping:
                self.set_action("Idle")

        # Apply Gravity
        self.velocity.y += self.gravity

        # Update Position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Check If on the Ground
        if self.rect.bottom >= ground_level:  # Check against dynamic ground level
            self.rect.bottom = ground_level
            self.is_jumping = False
            self.velocity.y = 0

        # Update Animation Frames
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)

            # ✅ Apply Flipping if Facing Left
            if not self.facing_right:
                self.image = pygame.transform.flip(self.images[self.image_index], True, False)
            else:
                self.image = self.images[self.image_index]
