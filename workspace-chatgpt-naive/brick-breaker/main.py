import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
WHITE = (255, 255, 255)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# Paddle
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x, ball_speed_y = 5 * random.choice((-1, 1)), 5 * random.choice((-1, 1))

# Bricks
bricks = []
for y in range(5):
    for x in range(10):
        bricks.append(pygame.Rect(x * (BRICK_WIDTH + 5) + 35, y * (BRICK_HEIGHT + 5) + 35, BRICK_WIDTH, BRICK_HEIGHT))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-10, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(10, 0)

    # Ball movement
    ball.move_ip(ball_speed_x, ball_speed_y)

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= SCREEN_HEIGHT:
        print("Game Over")
        running = False

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_speed_y *= -1
            bricks.remove(brick)
            break

    # Victory condition
    if not bricks:
        print("You Win!")
        running = False

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
