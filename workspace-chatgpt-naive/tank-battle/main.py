import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TANK_WIDTH, TANK_HEIGHT = 40, 20
TANK_BARREL_WIDTH, TANK_BARREL_HEIGHT = 40, 5
BULLET_RADIUS = 5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tank Battle Game')

# Clock to control the frame rate
clock = pygame.time.Clock()

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.health = 100
        self.rect = pygame.Rect(x, y, TANK_WIDTH, TANK_HEIGHT)
        self.barrel_angle = 0  # Angle in degrees, 0 is to the right
        self.speed = 2
        self.rotation_speed = 2  # Degrees per frame
    
    def draw(self):
        # Draw the tank body
        pygame.draw.rect(screen, self.color, self.rect)
        # Calculate the end point of the barrel with the current angle
        end_x = self.rect.centerx + math.cos(math.radians(self.barrel_angle)) * TANK_BARREL_WIDTH
        end_y = self.rect.centery - math.sin(math.radians(self.barrel_angle)) * TANK_BARREL_WIDTH
        # Draw the tank barrel
        pygame.draw.line(screen, GREY, self.rect.center, (end_x, end_y), TANK_BARREL_HEIGHT)
    
    def move(self, forward=True):
        # Move the tank forward or backward
        direction = 1 if forward else -1
        delta_x = self.speed * math.cos(math.radians(self.barrel_angle)) * direction
        delta_y = self.speed * math.sin(math.radians(self.barrel_angle)) * direction
        self.rect.x += delta_x
        self.rect.y -= delta_y  # Pygame's y-axis is inverted

    def rotate_barrel(self, left=True):
        # Rotate the barrel left or right
        if left:
            self.barrel_angle = (self.barrel_angle - self.rotation_speed) % 360
        else:
            self.barrel_angle = (self.barrel_angle + self.rotation_speed) % 360

class Bullet:
    def __init__(self, x, y, angle, velocity):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = velocity
        self.rect = pygame.Rect(x - BULLET_RADIUS, y - BULLET_RADIUS, BULLET_RADIUS * 2, BULLET_RADIUS * 2)
    
    def move(self):
        self.x += self.velocity * math.cos(math.radians(self.angle))
        self.y -= self.velocity * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, BULLET_RADIUS)

# Game variables
player_tank = Tank(50, SCREEN_HEIGHT // 2, GREEN)
enemy_tank = Tank(SCREEN_WIDTH - TANK_WIDTH - 50, SCREEN_HEIGHT // 2, RED)
bullets = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Player fires a bullet
                bullet = Bullet(
                    player_tank.rect.centerx,
                    player_tank.rect.centery,
                    player_tank.barrel_angle,
                    velocity=10
                )
                bullets.append(bullet)

    # Enemy fires back at random intervals
    if random.randint(0, 120) == 1:
        enemy_bullet = Bullet(
            enemy_tank.rect.centerx,
            enemy_tank.rect.centery,
            180,  # Assuming the enemy always faces left
            velocity=10
        )
        bullets.append(enemy_bullet)

    # Movement keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_tank.rotate_barrel(left=True)
    if keys[pygame.K_d]:
        player_tank.rotate_barrel(left=False)
    if keys[pygame.K_w]:
        player_tank.move(forward=True)
    if keys[pygame.K_s]:
        player_tank.move(forward=False)

    # Move and draw bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH or bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT:
            bullets.remove(bullet)
        elif player_tank.rect.colliderect(bullet.rect):
            player_tank.health -= 10
            bullets.remove(bullet)
        elif enemy_tank.rect.colliderect(bullet.rect):
            enemy_tank.health -= 10
            bullets.remove(bullet)

    # Check for game over
    if player_tank.health <= 0:
        print("Game Over! Enemy wins!")
        running = False
    elif enemy_tank.health <= 0:
        print("Game Over! You win!")
        running = False

    # Drawing everything
    screen.fill(BLACK)
    player_tank.draw()
    enemy_tank.draw()
    for bullet in bullets:
        bullet.draw()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
