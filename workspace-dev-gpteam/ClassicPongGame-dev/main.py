import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
BALL_SPEED_INCREMENT = 0.5
PADDLE_SPEED = 10
FPS = 60
WINNING_SCORE = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Set up the clock
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        # Keep the paddle within the screen bounds
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
        self.speed_x = random.choice((-5, 5))
        self.speed_y = random.choice((-5, 5))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off the top and bottom edges
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def increase_speed(self):
        if self.speed_x < 0:
            self.speed_x -= BALL_SPEED_INCREMENT
        else:
            self.speed_x += BALL_SPEED_INCREMENT

        if self.speed_y < 0:
            self.speed_y -= BALL_SPEED_INCREMENT
        else:
            self.speed_y += BALL_SPEED_INCREMENT

# Game class
class Game:
    def __init__(self):
        self.left_paddle = Paddle(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.left_score = 0
        self.right_score = 0
        self.paused = False

    def reset_ball(self):
        self.ball = Ball()

    def draw(self):
        screen.fill(BLACK)
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.ball.draw()

        # Draw the scores
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.left_score), 1, WHITE)
        screen.blit(text, (250, 10))
        text = font.render(str(self.right_score), 1, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 250, 10))

    def handle_collision(self):
        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x *= -1
            self.ball.increase_speed()

    def check_score(self):
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.reset_ball()
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.left_score += 1
            self.reset_ball()

    def check_win(self):
        if self.left_score >= WINNING_SCORE:
            return 'Left Player Wins!'
        elif self.right_score >= WINNING_SCORE:
            return 'Right Player Wins!'
        return None

    def display_winner(self, winner_text):
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render(winner_text, 1, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.left_paddle.move(up=True)
            if keys[pygame.K_s]:
                self.left_paddle.move(up=False)
            if keys[pygame.K_UP]:
                self.right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(up=False)
            if keys[pygame.K_SPACE]:
                self.paused = not self.paused

            if not self.paused:
                self.ball.move()
                self.handle_collision()
                self.check_score()
                winner = self.check_win()
                if winner:
                    self.display_winner(winner)
                    self.__init__()  # Restart the game

            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()