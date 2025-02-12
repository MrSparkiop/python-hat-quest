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
            "Hurt": self.load_animation("Hurt.png", 3),  # ✅ Hurt animation
            "Death": self.load_animation("Dead.png", 3),  # ✅ Death animation
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
        self.is_attacking = False
        self.facing_right = True

        # ✅ Health System
        self.max_health = 5
        self.health = self.max_health
        self.is_hurt = False
        self.is_dead = False  #

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
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.time_elapsed = 0  # Reset animation timer

    def attack(self):
        """ Trigger attack animation """
        if not self.is_attacking:
            self.is_attacking = True
            self.set_action("Attack_1")

    def take_damage(self, damage):
        """ Reduce health and trigger hurt animation before dying """
        if self.is_hurt or self.is_dead:
            return  # Ignore if already hurt or dead

        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.set_action("Death")
        else:
            self.is_hurt = True
            self.set_action("Hurt")

            # ✅ Add invulnerability for a short time
            self.hurt_timer = 1.0  # 0.5 seconds of invulnerability

    def apply_gravity(self):
        """ Apply gravity to the character """
        screen_height = pygame.display.get_surface().get_height()
        ground_level = screen_height - 100

        self.velocity.y += self.gravity
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.is_jumping = False
            self.velocity.y = 0

    def update(self, keys, dt):
        """ Update character movement, jumping, and attacks """
        screen_height = pygame.display.get_surface().get_height()
        ground_level = screen_height - 100

        # ✅ Handle Invulnerability Timer
        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False  # End hurt state

        # ✅ Prevent movement if dead
        if self.is_dead:
            return

        # ✅ Handle Hurt Animation
        if self.is_hurt:
            self.time_elapsed += dt
            if self.time_elapsed >= self.animation_speed:
                self.time_elapsed = 0
                self.image_index += 1

                if self.image_index >= len(self.images):  # Hurt animation ends
                    self.image_index = 0
                    self.is_hurt = False  # ✅ Only reset after animation finishes
                    self.set_action("Idle")
                else:
                    self.image = self.images[self.image_index]

            return  # ✅ Prevents overriding hurt state with movement

        # ✅ Handle Attack Animation
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

            return  # Skip movement while attacking

        # ✅ Apply Gravity
        self.apply_gravity()

        # Reset horizontal velocity
        self.velocity.x = 0

        # Prioritize Jumping
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity.y = self.jump_force
            self.is_jumping = True
            self.set_action("Jump")

        # Handle Movement (Only if not attacking or hurt)
        if keys[pygame.K_a]:  # Move left
            self.velocity.x = -self.speed
            self.facing_right = False
            if not self.is_jumping:
                self.set_action("Walk")
        elif keys[pygame.K_d]:  # Move right
            self.velocity.x = self.speed
            self.facing_right = True
            if not self.is_jumping:
                self.set_action("Walk")
        else:
            if not self.is_jumping:
                self.set_action("Idle")

        # ✅ Update Position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Check If on the Ground
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.is_jumping = False
            self.velocity.y = 0

        # ✅ Update Animation Frames
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)

            # ✅ Flip Image Based on Facing Direction
            if not self.facing_right:
                self.image = pygame.transform.flip(self.images[self.image_index], True, False)
            else:
                self.image = self.images[self.image_index]
