import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
BRICK_WIDTH, BRICK_HEIGHT = 60, 30
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
SPECIAL_EFFECT_TIME = 5  # Seconds
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Green Brick Breaker")

# Paddle
paddle = pygame.Rect(SCREEN_WIDTH//2 - PADDLE_WIDTH//2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_RADIUS, SCREEN_HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
ball_speed_x = 3 * random.choice((1, -1))
ball_speed_y = 3 * random.choice((1, -1))

# Bricks
bricks = []
for y in range(5):
    for x in range(10):
        brick = pygame.Rect(x * (BRICK_WIDTH + 10) + 20, y * (BRICK_HEIGHT + 10) + 20, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append((brick, RED if random.random() > 0.7 else GREEN))

# Special effect variables
special_effect_active = False
effect_start_time = None

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(5, 0)

    # Ball movement
    ball.move_ip(ball_speed_x, ball_speed_y)

    # Collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= SCREEN_HEIGHT:
        print("Game Over")
        running = False

    # Collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # Collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick[0]):
            ball_speed_y *= -1
            if brick[1] == RED:
                special_effect_active = True
                effect_start_time = time.time()
            bricks.remove(brick)

    # Special effect
    if special_effect_active:
        if time.time() - effect_start_time > SPECIAL_EFFECT_TIME:
            special_effect_active = False
        else:
            pygame.draw.rect(screen, RED, ball)  # Red and larger ball
            continue

    # Draw elements
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, GREEN if not special_effect_active else RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, brick[1], brick[0])

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
