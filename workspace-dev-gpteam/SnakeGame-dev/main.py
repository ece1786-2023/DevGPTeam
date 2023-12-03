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
BLACK = (0, 0, 0)

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
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
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
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.score = 0
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (SNAKE_SIZE, SNAKE_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
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
        pygame.draw.rect(surface, BLACK, r, 1)

# Main game loop
def game_loop():
    snake = Snake()
    item = Item()

    while True:
        screen.fill(WHITE)
        snake.handle_keys()
        snake.move()
        if snake.get_head_position() == item.position:
            snake.length += 1
            snake.score += 1
            item.randomize_position()

        snake.draw(screen)
        item.draw(screen)

        # Check for collisions with walls
        if (snake.get_head_position()[0] >= SCREEN_WIDTH or snake.get_head_position()[0] < 0 or
                snake.get_head_position()[1] >= SCREEN_HEIGHT or snake.get_head_position()[1] < 0):
            snake.reset()

        # Display score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f'Score: {snake.score}', True, BLACK)
        screen.blit(score_text, (5, 5))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

# Run the game
game_loop()