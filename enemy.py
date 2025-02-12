import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.animations = {
            "Idle":    self.load_animation("Idle.png", 7),    # e.g., 6 frames
            "Walk":    self.load_animation("Walk.png", 8),
            "Attack":  self.load_animation("Attack_1.png", 7),
            "Hurt":    self.load_animation("Hurt.png", 3),
            "Death":   self.load_animation("Dead.png", 3),   # e.g., 4 frames
        }

        #
        # 2) BASIC ANIMATION SETUP
        #
        self.current_action = "Idle"
        self.images = self.animations[self.current_action]
        self.image_index = 0
        self.time_elapsed = 0
        self.animation_speed = 0.15  # seconds per frame

        # For flipping logic, keep an unflipped reference frame each update:
        self.original_frame = self.images[self.image_index]
        self.image = self.original_frame

        # Position
        self.rect = self.image.get_rect(topleft=position)

        #
        # 3) STATS & MOVEMENT
        #
        self.max_health = 3
        self.health = self.max_health

        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 0.5
        self.move_speed = 50  # example: 50 px/second

        # AI states and direction
        self.state = "idle"
        self.facing_right = True

        # Basic patrol parameters
        self.patrol_range = 200
        self.patrol_start_x = position[0]
        self.patrol_direction = 1  # 1 = right, -1 = left

        # Attack parameters
        self.attack_range = 60
        self.attack_cooldown = 1.0
        self.attack_timer = 0

    def load_animation(self, filename, frame_count):
        """
        Load frames from a sprite sheet in 'Asset/enemy/filename'.
        Each frame is equally wide. Adjust as needed for your folder layout.
        """
        path = os.path.join("Asset", "enemy", filename)
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []

        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames

    def set_action(self, action):
        """Switch to a new animation only if it's different from the current one."""
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0
            self.time_elapsed = 0

            # Update the 'original_frame' to the first frame of the new action
            self.original_frame = self.images[self.image_index]
            self.image = self.original_frame

    def apply_gravity(self):
        """Apply gravity until we hit the 'ground' (screen_height - 100)."""
        screen_height = pygame.display.get_surface().get_height()
        ground_level = screen_height - 100
        if self.rect.bottom < ground_level:
            self.velocity.y += self.gravity
        else:
            self.rect.bottom = ground_level
            self.velocity.y = 0

    def take_damage(self, amount):
        """Reduce health, switch to 'Hurt' or 'Death' animation/state."""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.state = "death"
            self.set_action("Death")
        else:
            self.state = "hurt"
            self.set_action("Hurt")

    def update_ai(self, dt, player):
        """
        Very simple AI flow:
          1) If we're 'death', do nothing (just animate).
          2) If 'hurt', wait for the animation to finish.
          3) Otherwise, decide if we should 'patrol', 'chase', or 'attack'.
        """
        # 1) Death
        if self.state == "death":
            return

        # 2) Hurt
        if self.state == "hurt":
            # We'll let the Hurt animation finish, then revert to idle or chase after one loop.
            return

        # 3) Patrol / Chase / Attack logic
        distance_to_player = player.rect.centerx - self.rect.centerx
        distance_abs = abs(distance_to_player)

        # Only update facing if in states that allow it
        if self.state in ("idle", "patrol", "chase"):
            # Use a small threshold so it won't spin at close range
            if distance_to_player > 5:
                self.facing_right = True
            elif distance_to_player < -5:
                self.facing_right = False

        # Attack range check
        if distance_abs < self.attack_range:
            # If we can attack again, do it
            if self.attack_timer <= 0:
                self.state = "attack"
                self.set_action("Attack")
                self.attack_timer = self.attack_cooldown
            else:
                # Otherwise idle if not attacking
                if self.state != "attack":
                    self.state = "idle"
                    self.set_action("Idle")
        elif distance_abs < 300:
            self.state = "chase"
            self.set_action("Walk")
        else:
            self.state = "patrol"
            self.set_action("Walk")

    def do_movement(self, dt):
        """Move the enemy according to its current state."""
        if self.state == "death":
            return

        if self.state == "chase":
            # Move toward the player
            direction = 1 if self.facing_right else -1
            self.velocity.x = direction * self.move_speed * dt
        elif self.state == "patrol":
            # Walk back and forth around the patrol start
            self.velocity.x = self.patrol_direction * self.move_speed * dt

            if abs(self.rect.x - self.patrol_start_x) > self.patrol_range:
                self.patrol_direction *= -1
        else:
            # idle, attack, hurt
            self.velocity.x = 0

        self.rect.x += self.velocity.x

    def process_attack_logic(self, player):
        """
        If in 'attack' state, define an attack hitbox in front of the enemy
        and check collision with the player's rect. If you have a player.take_damage(),
        call it here if collision occurs.
        """
        if self.state == "attack":
            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right - 10, self.rect.y, 40, self.rect.height)
            else:
                attack_rect = pygame.Rect(self.rect.left - 30, self.rect.y, 40, self.rect.height)

            if attack_rect.colliderect(player.rect):
                # e.g. player.take_damage(1)
                pass

    def update(self, dt, player=None):
        """
        Main update function:
          1) Gravity
          2) Decrement attack cooldown
          3) AI logic
          4) Movement
          5) Attack collision
          6) Animation updates
        """
        self.apply_gravity()

        if self.attack_timer > 0:
            self.attack_timer -= dt

        if player:
            self.update_ai(dt, player)
            self.do_movement(dt)
            self.process_attack_logic(player)

        #
        # 4) UPDATE ANIMATION
        #
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.original_frame = self.images[self.image_index]  # store unflipped frame

            # If we've just finished the Hurt or Attack animation, revert to idle
            if self.image_index == 0:
                if self.current_action == "Hurt" and self.state == "hurt":
                    self.state = "idle"
                    self.set_action("Idle")
                elif self.current_action == "Attack" and self.state == "attack":
                    self.state = "idle"
                    self.set_action("Idle")

            # If "death" animation reaches its last frame, remove this sprite
            # (Check if image_index is at last frame, or if you prefer after one full loop.)
            if self.current_action == "Death" and self.image_index == len(self.images) - 1:
                self.kill()

        #
        # 5) FLIP IF FACING LEFT
        #
        if self.facing_right:
            self.image = self.original_frame
        else:
            self.image = pygame.transform.flip(self.original_frame, True, False)
