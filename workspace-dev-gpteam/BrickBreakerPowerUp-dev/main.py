import pygame
import random
import time

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BRICK_WIDTH, BRICK_HEIGHT = 75, 30
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_SIZE = 15
BALL_SPEED = 5
PADDLE_SPEED = 7
GREEN_BRICK = 1
RED_BRICK = 2
BRICKS_PER_ROW = SCREEN_WIDTH // BRICK_WIDTH
BRICK_ROWS = 5
POWER_UP_TIME = 10

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker with Power-Up')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game variables
score = 0
lives = 3
ball_speed_x = BALL_SPEED
ball_speed_y = -BALL_SPEED
power_up_active = False
power_up_start_time = 0

# Paddle
paddle = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball
ball = pygame.Rect((SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))

# Bricks
bricks = []
for y in range(BRICK_ROWS):
    for x in range(BRICKS_PER_ROW):
        brick_type = GREEN_BRICK if random.random() > 0.2 else RED_BRICK
        color = GREEN if brick_type == GREEN_BRICK else RED
        bricks.append({'rect': pygame.Rect(x * BRICK_WIDTH, y * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT), 'color': color, 'type': brick_type})

# Main loop
running = True
game_active = False
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True

    # Game logic
    if game_active:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        # Ball movement
        ball.move_ip(ball_speed_x, ball_speed_y)

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y
        if ball.bottom >= SCREEN_HEIGHT:
            lives -= 1
            ball = pygame.Rect((SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))
            ball_speed_y = -BALL_SPEED
            if lives == 0:
                game_active = False

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick['rect']):
                ball_speed_y = -ball_speed_y
                bricks.remove(brick)
                score += 10
                if brick['type'] == RED_BRICK:
                    power_up_active = True
                    power_up_start_time = time.time()
                    ball = pygame.Rect(ball.left, ball.top, BALL_SIZE * 2, BALL_SIZE * 2)
                    ball_speed_x, ball_speed_y = ball_speed_x * 1.5, ball_speed_y * 1.5

        # Power-up duration
        if power_up_active and time.time() - power_up_start_time > POWER_UP_TIME:
            power_up_active = False
            ball = pygame.Rect(ball.left, ball.top, BALL_SIZE, BALL_SIZE)
            ball_speed_x, ball_speed_y = BALL_SPEED, -BALL_SPEED

        # Draw ball
        pygame.draw.ellipse(screen, RED if power_up_active else BLUE, ball)

        # Draw paddle
        pygame.draw.rect(screen, WHITE, paddle)

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, brick['color'], brick['rect'])

        # Draw score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        screen.blit(score_text, (5, 5))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 5, 5))

    else:
        # Main menu
        font = pygame.font.Font(None, 74)
        title_text = font.render('Brick Breaker', True, WHITE)
        instruction_text = font.render('Press SPACE to start', True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()