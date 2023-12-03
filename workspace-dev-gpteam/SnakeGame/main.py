import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SNAKE_SIZE = 20
ITEM_SIZE = 20
SNAKE_SPEED = 15

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * SNAKE_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * SNAKE_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        elif new[0] >= SCREEN_WIDTH or new[0] < 0 or new[1] >= SCREEN_HEIGHT or new[1] < 0:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.score = 0
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (SNAKE_SIZE, SNAKE_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.turn((1, 0))

# Item class
class Item:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - ITEM_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - ITEM_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (ITEM_SIZE, ITEM_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

def draw_score(surface, score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (5, 5))

def game_over(surface, score):
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    main()

def main():
    snake = Snake()
    item = Item()

    while True:
        screen.fill((0, 0, 0))
        snake.handle_keys()
        snake.move()
        if snake.get_head_position() == item.position:
            snake.length += 1
            snake.score += 1
            item.randomize_position()

        snake.draw(screen)
        item.draw(screen)
        draw_score(screen, snake.score)
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

        # Check for game over
        head_x, head_y = snake.get_head_position()
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            game_over(screen, snake.score)
            break

if __name__ == "__main__":
    main()