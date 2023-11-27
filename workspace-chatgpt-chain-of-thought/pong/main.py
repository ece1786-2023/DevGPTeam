import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
FONT_SIZE = 30
WINNING_SCORE = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Paddle and Ball Setup
paddle1 = pygame.Rect(10, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(SCREEN_WIDTH - 10 - PADDLE_WIDTH, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect((SCREEN_WIDTH - BALL_SIZE) // 2, (SCREEN_HEIGHT - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)

# Movement variables
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y
paddle_speed = PADDLE_SPEED

# Score variables
score1 = 0
score2 = 0

# Font for text
font = pygame.font.Font(None, FONT_SIZE)

# Game loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pause feature
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        # Paddle Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.y -= paddle_speed if paddle1.y > 0 else 0
        if keys[pygame.K_s]:
            paddle1.y += paddle_speed if paddle1.y < SCREEN_HEIGHT - PADDLE_HEIGHT else 0
        if keys[pygame.K_UP]:
            paddle2.y -= paddle_speed if paddle2.y > 0 else 0
        if keys[pygame.K_DOWN]:
            paddle2.y += paddle_speed if paddle2.y < SCREEN_HEIGHT - PADDLE_HEIGHT else 0

        # Ball Movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball Collision with top and bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1

        # Ball Collision with paddles
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_speed_x *= -1

        # Score Update
        if ball.left <= 0:
            score2 += 1
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x *= -1

        if ball.right >= SCREEN_WIDTH:
            score1 += 1
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x *= -1

        # Check for winning score
        if score1 >= WINNING_SCORE or score2 >= WINNING_SCORE:
            winner = "Player 1" if score1 > score2 else "Player 2"
            text = font.render(f'{winner} wins!', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds
            score1, score2 = 0, 0  # Reset scores
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Reset ball position

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        score_text = font.render(f'{score1}  {score2}', True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 frames per second

pygame.quit()
