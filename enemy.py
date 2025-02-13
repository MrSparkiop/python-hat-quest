import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.animations = {
            "Idle":   self.load_animation("Idle.png", 7),
            "Walk":   self.load_animation("Walk.png", 8),
            "Attack": self.load_animation("Attack_1.png", 7),
            "Hurt":   self.load_animation("Hurt.png", 3),
            "Death":  self.load_animation("Dead.png", 3),
        }

        self.current_action = "Idle"
        self.images = self.animations[self.current_action]
        self.image_index = 0
        self.time_elapsed = 0
        self.animation_speed = 0.15

        self.original_frame = self.images[self.image_index]
        self.image = self.original_frame

        # Position
        self.rect = self.image.get_rect(topleft=position)

        # Health & States
        self.max_health = 3
        self.health = self.max_health
        self.is_hurt = False
        self.is_dead = False
        self.hurt_timer = 0

        # Movement & AI
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 0.5
        self.move_speed = 50
        self.state = "idle"
        self.facing_right = True
        self.patrol_range = 200
        self.patrol_start_x = position[0]
        self.patrol_direction = 1

        # Attack
        self.attack_range = 60
        self.attack_cooldown = 1.0
        self.attack_timer = 0

    def load_animation(self, filename, frame_count):
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
        """ Switch to a new animation only if it's different from the current one. """
        if action != self.current_action:
            self.current_action = action
            self.images = self.animations[action]
            self.image_index = 0
            self.time_elapsed = 0
            self.original_frame = self.images[self.image_index]
            self.image = self.original_frame

    def apply_gravity(self):
        """ Let the main loop or platform collision handle final snap to ground if needed. """
        self.velocity.y += self.gravity

    def take_damage(self, damage):
        """ Enemy takes damage and plays Hurt or Death animation. """
        if self.is_hurt or self.is_dead:
            return

        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.set_action("Death")
            self.image_index = 0
        else:
            self.is_hurt = True
            self.set_action("Hurt")
            self.hurt_timer = 0.5

    def draw_health_bar(self, screen):
        """ Draw a health bar above the enemy """
        if self.health > 0:
            bar_width = 50
            bar_height = 5
            health_ratio = max(self.health / self.max_health, 0)
            health_length = int(bar_width * health_ratio)

            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 10

            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_length, bar_height))

    def update_ai(self, dt, player):
        """ Enemy behavior: patrol, chase, or attack. """
        if self.is_dead:
            return

        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False
                self.state = "idle"
                self.set_action("Idle")
            return

        distance_to_player = player.rect.centerx - self.rect.centerx
        distance_abs = abs(distance_to_player)

        # Determine facing direction
        if distance_to_player > 5:
            self.facing_right = True
        elif distance_to_player < -5:
            self.facing_right = False

        # Attack if in range
        if distance_abs < self.attack_range:
            if self.attack_timer <= 0:
                self.state = "attack"
                self.set_action("Attack")
                self.attack_timer = self.attack_cooldown
            else:
                if self.state != "attack":
                    self.state = "idle"
                    self.set_action("Idle")
        elif distance_abs < 300:
            # chase
            self.state = "chase"
            self.set_action("Walk")
        else:
            # patrol
            self.state = "patrol"
            self.set_action("Walk")

    def do_movement(self, dt):
        """ Move enemy according to AI state. """
        if self.is_dead:
            return

        if self.state == "chase":
            direction = 1 if self.facing_right else -1
            self.velocity.x = direction * self.move_speed * dt
        elif self.state == "patrol":
            self.velocity.x = self.patrol_direction * self.move_speed * dt
            if abs(self.rect.x - self.patrol_start_x) > self.patrol_range:
                self.patrol_direction *= -1
        else:
            self.velocity.x = 0

        self.rect.x += self.velocity.x

    def process_attack_logic(self, player):
        """ Attack player if in range (and not invulnerable). """
        if self.state == "attack" and player.health > 0 and player.respawn_invulnerability_timer <= 0:
            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right - 10, self.rect.y, 40, self.rect.height)
            else:
                attack_rect = pygame.Rect(self.rect.left - 30, self.rect.y, 40, self.rect.height)

            if attack_rect.colliderect(player.rect):
                player.take_damage(1)

    def update(self, dt, player=None):
        """ Main update: gravity, AI, movement, attacking, animations. """
        self.apply_gravity()

        if self.attack_timer > 0:
            self.attack_timer -= dt

        if player:
            self.update_ai(dt, player)
            self.do_movement(dt)
            self.process_attack_logic(player)

        # Animate
        self.time_elapsed += dt
        if self.time_elapsed >= self.animation_speed:
            self.time_elapsed = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.original_frame = self.images[self.image_index]

            # If finishing an animation
            if self.image_index == 0:
                # End of Hurt?
                if self.current_action == "Hurt" and self.is_hurt:
                    self.is_hurt = False
                    self.state = "idle"
                    self.set_action("Idle")
                # End of Attack?
                elif self.current_action == "Attack" and self.state == "attack":
                    self.state = "idle"
                    self.set_action("Idle")

            # If Death animation finishes, remove sprite
            if self.current_action == "Death" and self.image_index == len(self.images) - 1:
                self.kill()

        # Flip image if facing left
        if self.facing_right:
            self.image = self.original_frame
        else:
            self.image = pygame.transform.flip(self.original_frame, True, False)
