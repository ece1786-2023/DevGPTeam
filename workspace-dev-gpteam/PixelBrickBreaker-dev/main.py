import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_ROWS = 6
BRICK_COLUMNS = 10
BRICK_SPACING = 5
LIVES = 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PixelBreaker")

# Set up the font
font = pygame.font.Font(None, 36)

# Game variables
score = 0
lives = LIVES
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = -4
paddle_speed = 0
power_up_active = False
power_up_timer = 0

# Paddle
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, paddle.y - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    brick_color = GREEN if row % 2 == 0 else RED
    for column in range(BRICK_COLUMNS):
        brick = pygame.Rect(column * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING,
                            row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_SPACING + 50,
                            BRICK_WIDTH,
                            BRICK_HEIGHT)
        bricks.append((brick, brick_color))

# Main menu
def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("PixelBreaker", True, WHITE)
        start_text = font.render("Press SPACE to start", True, WHITE)
        quit_text = font.render("Press ESC to quit", True, WHITE)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Game over screen
def game_over():
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        quit_text = font.render("Press ESC to quit", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(final_score_text, final_score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Reset game
def reset_game():
    global score, lives, ball_speed_x, ball_speed_y, paddle, ball, bricks, power_up_active, power_up_timer
    score = 0
    lives = LIVES
    ball_speed_x = 4 * random.choice((1, -1))
    ball_speed_y = -4
    paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, paddle.y - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    bricks = []
    for row in range(BRICK_ROWS):
        brick_color = GREEN if row % 2 == 0 else RED
        for column in range(BRICK_COLUMNS):
            brick = pygame.Rect(column * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING,
                                row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_SPACING + 50,
                                BRICK_WIDTH,
                                BRICK_HEIGHT)
            bricks.append((brick, brick_color))
    power_up_active = False
    power_up_timer = 0

# Main game loop
def main_game():
    global score, lives, ball_speed_x, ball_speed_y, paddle_speed, power_up_active, power_up_timer

    clock = pygame.time.Clock()
    running = True
    ball_launched = False

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    paddle_speed = -6
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    paddle_speed = 6
                if event.key == pygame.K_SPACE:
                    if not ball_launched:
                        ball_launched = True
                    else:
                        # Pause functionality
                        paused = True
                        while paused:
                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_SPACE:
                                    paused = False
                                if pause_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    paddle_speed = 0

        # Paddle movement
        paddle.x += paddle_speed
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > SCREEN_WIDTH:
            paddle.right = SCREEN_WIDTH

        # Ball movement
        if ball_launched:
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_speed_x *= -1
            if ball.top <= 0:
                ball_speed_y *= -1
            if ball.bottom >= SCREEN_HEIGHT:
                lives -= 1
                ball_launched = False
                ball.center = (SCREEN_WIDTH // 2, paddle.y - BALL_RADIUS * 2)
                ball_speed_x = 4 * random.choice((1, -1))
                ball_speed_y = -4
                if lives == 0:
                    game_over()
                    running = False

            # Ball collision with paddle
            if ball.colliderect(paddle) and ball_speed_y > 0:
                ball_speed_y *= -1
                offset = (ball.centerx - paddle.centerx) / (paddle.width / 2)
                ball_speed_x += offset * 2

            # Ball collision with bricks
            for brick, color in bricks[:]:
                if ball.colliderect(brick):
                    if color == GREEN:
                        score += 5
                    elif color == RED:
                        score += 10
                        power_up_active = True
                        power_up_timer = pygame.time.get_ticks()
                        ball_speed_x *= 1.5
                        ball_speed_y *= 1.5
                        ball.color = DARK_RED
                    bricks.remove((brick, color))
                    ball_speed_y *= -1
                    break

        # Power-up logic
        if power_up_active:
            current_time = pygame.time.get_ticks()
            if current_time - power_up_timer > 10000:
                power_up_active = False
                paddle.width = PADDLE_WIDTH
                ball.color = BLUE
                ball_speed_x /= 1.5
                ball_speed_y /= 1.5
            else:
                paddle.width = PADDLE_WIDTH * 2

        # Draw everything
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, ball.color, ball)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # Draw the score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (5, 5))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 5, 5))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# Start the game
main_menu()
main_game()