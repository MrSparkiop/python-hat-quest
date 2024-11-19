import pygame

# Основен клас за героя
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Зелен цвят за героя
        self.rect = self.image.get_rect(center=(100, 300))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Основен клас за противници
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Червен цвят за противника
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += 2  # Движи се към играча
        elif self.rect.x > player.rect.x:
            self.rect.x -= 2
        if self.rect.y < player.rect.y:
            self.rect.y += 2
        elif self.rect.y > player.rect.y:
            self.rect.y -= 2

# Основен цикъл на играта
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = Player()
enemies = pygame.sprite.Group(Enemy(700, 300), Enemy(500, 200))
all_sprites = pygame.sprite.Group(player, *enemies)

running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновяване
    player.update(keys)
    enemies.update(player)

    # Рендериране
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
