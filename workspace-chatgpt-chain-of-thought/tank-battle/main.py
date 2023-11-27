import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants for the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tank Battle Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tank class
class Tank(pygame.sprite.Sprite):
    def __init__(self, color, x, y, angle=0):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 5
        self.health = 100

    def update(self, action=None):
        if action == 'MOVE_FORWARD':
            self.rect.x += int(self.speed * math.cos(math.radians(self.angle)))
            self.rect.y += int(self.speed * math.sin(math.radians(self.angle)))
        elif action == 'MOVE_BACKWARD':
            self.rect.x -= int(self.speed * math.cos(math.radians(self.angle)))
            self.rect.y -= int(self.speed * math.sin(math.radians(self.angle)))
        elif action == 'ROTATE_LEFT':
            self.angle = (self.angle + 5) % 360
        elif action == 'ROTATE_RIGHT':
            self.angle = (self.angle - 5) % 360

        # Keep the tank on the screen
        self.rect.clamp_ip(screen.get_rect())

    def draw_barrel(self, screen):
        barrel_length = 30
        end_x = self.rect.centerx + int(barrel_length * math.cos(math.radians(self.angle)))
        end_y = self.rect.centery + int(barrel_length * math.sin(math.radians(self.angle)))
        pygame.draw.line(screen, WHITE, self.rect.center, (end_x, end_y), 2)

    def take_damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(10, 0).rotate(-angle)

    def update(self):
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        # Remove the bullet if it goes off-screen
        if not screen.get_rect().contains(self.rect):
            self.kill()

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

# Sprite groups
tanks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Create tanks
player_tank = Tank(GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
ai_tank = Tank(RED, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3)
tanks.add(player_tank, ai_tank)

# Create obstacles
obstacles.add(Obstacle(100, 100, 100, 50), Obstacle(400, 300, 200, 50), Obstacle(150, 450, 100, 50))

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_tank.update('MOVE_FORWARD')
    if keys[pygame.K_s]:
        player_tank.update('MOVE_BACKWARD')
    if keys[pygame.K_a]:
        player_tank.update('ROTATE_LEFT')
    if keys[pygame.K_d]:
        player_tank.update('ROTATE_RIGHT')
    if keys[pygame.K_SPACE]:
        bullets.add(Bullet(player_tank.rect.centerx, player_tank.rect.centery, player_tank.angle))

    # AI behavior and shooting
    # (AI behavior is simplified for demonstration purposes)
    ai_action = random.choice(['MOVE_FORWARD', 'MOVE_BACKWARD', 'ROTATE_LEFT', 'ROTATE_RIGHT'])
    ai_tank.update(ai_action)
    if random.random() < 0.1:
        bullets.add(Bullet(ai_tank.rect.centerx, ai_tank.rect.centery, ai_tank.angle))

    # Update game entities
    tanks.update()
    bullets.update()

    # Check for bullet collisions with tanks
    for bullet in bullets:
        hit_tanks = pygame.sprite.spritecollide(bullet, tanks, False)
        for hit_tank in hit_tanks:
            if hit_tank is not bullet.owner:
                hit_tank.take_damage(10)
                bullet.kill()

    # Check for tank collisions with obstacles
    for tank in tanks:
        if pygame.sprite.spritecollideany(tank, obstacles):
            tank.take_damage(5)

    # Drawing
    screen.fill(BLACK)
    obstacles.draw(screen)
    tanks.draw(screen)
    for tank in tanks:
        tank.draw_barrel(screen)
    bullets.draw(screen)

    pygame.display.flip()  # Update the display

    # Frame rate control
    pygame.time.Clock().tick(60)

# Quit the game
pygame.quit()
sys.exit()
