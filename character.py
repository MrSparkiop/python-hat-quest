import pygame
import os

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Load animations
        self.animations = {
            "Attack_1": self.load_animation("Attack_1.png", 6),
            "Idle":     self.load_animation("Idle.png", 8),
            "Jump":     self.load_animation("Jump.png", 8),
            "Walk":     self.load_animation("Walk.png", 8),
            "Hurt":     self.load_animation("Hurt.png", 3),
            "Death":    self.load_animation("Dead.png", 3),
        }

        # Default animation
        self.current_action = "Idle"
        self.images = self.animations[self.current_action]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=position)

        # Animation timing
        self.animation_speed = 0.1
        self.time_elapsed = 0

        # Movement
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.5
        self.jump_force = -10
        self.is_jumping = False
        self.facing_right = True

        # Attacking
        self.is_attacking = False

        # Health
        self.max_health = 5
        self.health = self.max_health
        self.is_hurt = False
        self.is_dead = False

        # Knockdown logic
        self.knockdown_timer = 0
        self.saved_position = None  # To restore after knockdown

        # Respawn invulnerability
        self.respawn_invulnerability_timer = 0

    def load_animation(self, filename, frame_count):
        asset_folder = os.path.join("Asset", "character", filename)
        sprite_sheet = pygame.image.load(asset_folder).convert_alpha()
        frames = []
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def set_action(self, action):
        """Switch to a new animation if it's different from the current one."""
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.time_elapsed = 0

    def attack(self):
        if not self.is_attacking and not self.is_hurt and not self.is_dead:
            self.is_attacking = True
            self.set_action("Attack_1")

    def take_damage(self, damage):
        """ Take damage and briefly knock down the player. """
        if self.respawn_invulnerability_timer > 0 or self.is_hurt or self.is_dead:
            return

        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.set_action("Death")
        else:
            self.is_hurt = True
            self.set_action("Hurt")
            # Save current position
            self.saved_position = (self.rect.x, self.rect.y)
            # Force player onto the ground visually (assuming ground at y=560)
            # You can adjust this if your ground rect is at a different y
            self.rect.bottom = 560
            # Time to remain "knocked down"
            self.knockdown_timer = 1.0

    def apply_gravity(self):
        """ Simple gravity: just accelerate downward. """
        self.velocity.y += self.gravity

    def update(self, keys, dt):
        # If the player is dead, skip all logic except the death animation
        if self.is_dead:
            return

        # Handle respawn invulnerability blinking
        if self.respawn_invulnerability_timer > 0:
            self.respawn_invulnerability_timer -= dt
            if self.respawn_invulnerability_timer <= 0:
                self.respawn_invulnerability_timer = 0
                self.image.set_alpha(255)
            else:
                # Blink effect
                if int(self.respawn_invulnerability_timer * 10) % 2 == 0:
                    self.image.set_alpha(100)
                else:
                    self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        # If player is in hurt/knockdown state
        if self.is_hurt:
            # Update the Hurt animation frames
            self.time_elapsed += dt
            if self.time_elapsed >= self.animation_speed:
                self.time_elapsed = 0
                self.image_index += 1
                # If we've gone past the last Hurt frame, hold the last frame
                if self.image_index >= len(self.images):
                    self.image_index = len(self.images) - 1
                else:
                    self.image = self.images[self.image_index]

            # Count down knockdown time
            self.knockdown_timer -= dt
            if self.knockdown_timer <= 0:
                # Stand back up
                self.is_hurt = False
                self.set_action("Idle")
                # Restore the old position
                if self.saved_position:
                    self.rect.x, self.rect.y = self.saved_position
                self.saved_position = None

            return  # Skip normal movement if hurt

        # If attacking, play the Attack_1 animation
        if self.is_attacking:
            self.time_elapsed += dt
            if self.time_elapsed >= self.animation_speed:
                self.time_elapsed = 0
                self.image_index += 1
                if self.image_index >= len(self.images):
                    # Attack animation finished
                    self.image_index = 0
                    self.is_attacking = False
                    self.set_action("Idle")
                else:
                    self.image = self.images[self.image_index]
            return

        # Normal movement logic
        self.apply_gravity()
        self.velocity.x = 0

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity.y = self.jump_force
            self.is_jumping = True
            self.set_action("Jump")

        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
            self.facing_right = False
            if not self.is_jumping:
                self.set_action("Walk")
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.facing_right = True
            if not self.is_jumping:
                self.set_action("Walk")
        else:
            if not self.is_jumping:
                self.set_action("Idle")

        # Update position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Animation update for Idle/Walk/Jump
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)

            current_frame = self.images[self.image_index]
            # Flip if facing left
            if not self.facing_right:
                current_frame = pygame.transform.flip(current_frame, True, False)

            self.image = current_frame
