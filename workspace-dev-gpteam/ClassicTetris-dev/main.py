import pygame
import random
import time

# Define the size of the grid
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Define the size of the window
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Define colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Define the shapes of the Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

# Define the colors of the Tetriminos
SHAPES_COLORS = [
    (0, 255, 255),  # Cyan
    (128, 0, 128),  # Purple
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (255, 165, 0)   # Orange
]

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Classic Tetris')

# Define the font for displaying the score
font = pygame.font.Font(None, 36)

# Define the Tetrimino class
class Tetrimino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# Define the game class
class TetrisGame:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.start_time = time.time()
        self.speed = 1

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = SHAPES_COLORS[SHAPES.index(shape)]
        return Tetrimino(shape, color)

    def collide(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell and (x + offset_x < 0 or x + offset_x >= GRID_WIDTH or y + offset_y >= GRID_HEIGHT or self.grid[y + offset_y][x + offset_x]):
                    return True
        return False

    def freeze(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.current_piece.y][x + self.current_piece.x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if self.collide(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [index for index, row in enumerate(self.grid) if all(row)]
        for index in lines_to_clear:
            del self.grid[index]
            self.grid.insert(0, [0] * GRID_WIDTH)
        self.score += len(lines_to_clear) ** 2

    def move_current_piece(self, dx, dy):
        if not self.collide(self.current_piece.shape, self.current_piece.x + dx, self.current_piece.y + dy):
            self.current_piece.move(dx, dy)

    def rotate_current_piece(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.collide(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
            self.current_piece.shape = original_shape

    def drop_current_piece(self):
        while not self.collide(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1):
            self.current_piece.move(0, 1)
        self.freeze()

    def update(self):
        if time.time() - self.start_time > 10:
            self.speed += 0.1
            self.start_time = time.time()
        if not self.collide(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1):
            self.current_piece.move(0, self.speed)
        else:
            self.freeze()

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x]
                if color:
                    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GREY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_current_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + x) * CELL_SIZE, (self.current_piece.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_next_piece(self):
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece.color, ((GRID_WIDTH + 1 + x) * CELL_SIZE, (1 + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_score(self):
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH - 200, 10))

    def draw_game_over(self):
        game_over_text = font.render('GAME OVER', True, WHITE)
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - game_over_text.get_height() // 2))

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_current_piece()
        self.draw_next_piece()
        self.draw_score()
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = TetrisGame()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_current_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_current_piece(1, 0)
                elif event.key == pygame.K_UP:
                    game.rotate_current_piece()
                elif event.key == pygame.K_DOWN:
                    game.move_current_piece(0, 1)
                elif event.key == pygame.K_SPACE:
                    game.drop_current_piece()

        game.update()
        game.draw()

        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()