import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15
WHITE = (255, 255, 255)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])

# Initialize paddles and ball
paddle1 = Paddle(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
paddle2 = Paddle(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Game variables
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)
running = True
clock = pygame.time.Clock()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move(-5)
    if keys[pygame.K_s]:
        paddle1.move(5)
    if keys[pygame.K_UP]:
        paddle2.move(-5)
    if keys[pygame.K_DOWN]:
        paddle2.move(5)

    # Move ball
    ball.move()

    # Check for collisions
    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.dx *= -1

    # Check for scoring
    if ball.rect.left <= 0:
        player2_score += 1
        ball.reset()
    if ball.rect.right >= SCREEN_WIDTH:
        player1_score += 1
        ball.reset()

    # Check for winning condition
    if player1_score == 10 or player2_score == 10:
        running = False

    # Draw everything
    screen.fill((0, 0, 0))
    paddle1.draw()
    paddle2.draw()
    ball.draw()

    # Display scores
    text = font.render(str(player1_score), True, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(player2_score), True, WHITE)
    screen.blit(text, (420, 10))

    # Update screen and wait
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
