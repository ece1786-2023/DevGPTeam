import pygame
import time
from random import choice

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BRICK_WIDTH, BRICK_HEIGHT = 60, 30
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_SIZE = 15
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
SPECIAL_EFFECT_DURATION = 5  # seconds

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Python Green Brick Breaker')

# Bricks
def create_bricks():
    bricks = []
    for y in range(5):
        for x in range(10):
            brick_color = choice([RED, GREEN])
            brick = pygame.Rect(x * (BRICK_WIDTH + 5) + 35, y * (BRICK_HEIGHT + 5) + 35, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append((brick, brick_color))
    return bricks

bricks = create_bricks()

# Paddle
paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect((SCREEN_WIDTH - BALL_SIZE) // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 3
ball_speed_y = 3

def draw_objects():
    screen.fill((0, 0, 0))
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, GREEN, ball)
    pygame.display.flip()

def move_ball():
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    # Collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1

    # Collision with bricks
    for brick, color in bricks[:]:
        if ball.colliderect(brick):
            if color == RED:
                pygame.draw.ellipse(screen, RED, ball.inflate(BALL_SIZE, BALL_SIZE))  # Double size and change color
                pygame.display.flip()
                time.sleep(SPECIAL_EFFECT_DURATION)  # Wait for 5 seconds
                pygame.draw.ellipse(screen, GREEN, ball)  # Revert to original size and color
            bricks.remove((brick, color))
            ball_speed_y *= -1
            break

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 5
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.x += 5

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_ball()
    move_paddle()
    draw_objects()

    clock.tick(60)

pygame.quit()
