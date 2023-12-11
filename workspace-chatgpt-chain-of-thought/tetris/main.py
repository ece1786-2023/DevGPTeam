import pygame
import random

# Initialize Pygame
pygame.init()

# Game Variables
screen_width, screen_height = 300, 600
grid_size = 30
grid_width, grid_height = screen_width // grid_size, screen_height // grid_size
game_speed = 500  # Milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (128, 0, 128)   # Purple
]

# Tetromino Shapes
TETROMINOES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Setup the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

def draw_grid(surface, grid):
    for i in range(grid_width):
        for j in range(grid_height):
            pygame.draw.rect(surface, BLACK, (i*grid_size, j*grid_size, grid_size, grid_size), 1)

def draw_tetromino(surface, shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, COLORS[TETROMINOES.index(shape)], 
                                 (x*grid_size + j*grid_size, y*grid_size + i*grid_size, grid_size, grid_size))

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def valid_space(shape, grid, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell and (x + j < 0 or x + j >= grid_width or y + i >= grid_height or grid[y + i][x + j]):
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(TETROMINOES)
        self.color = COLORS[TETROMINOES.index(self.shape)]

    def move(self, dx, dy, grid):
        new_x = self.x + dx
        new_y = self.y + dy
        if valid_space(self.shape, grid, new_x, new_y):
            self.x = new_x
            self.y = new_y

    def rotate(self, grid):
        new_shape = rotate(self.shape)
        if valid_space(new_shape, grid, self.x, self.y):
            self.shape = new_shape

def create_grid(locked_positions={}):
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for y in range(grid_height):
        for x in range(grid_width):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_window(surface, grid):
    surface.fill(WHITE)
    draw_grid(surface, grid)
    pygame.display.update()

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Tetromino(5, 0)
    clock = pygame.time.Clock()

    while run:
        grid = create_grid(locked_positions)
        fall_time = 0

        fall_speed = game_speed
        clock.tick()
        fall_time += clock.get_rawtime()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0, grid)
                if event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0, grid)
                if event.key == pygame.K_DOWN:
                    current_piece.move(0, 1, grid)
                if event.key == pygame.K_UP:
                    current_piece.rotate(grid)

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.move(0, 1, grid)
            if not valid_space(current_piece.shape, grid, current_piece.x, current_piece.y):
                change_piece = True

        draw_window(screen, grid)
        draw_tetromino(screen, current_piece.shape, current_piece.x, current_piece.y)
        pygame.display.update()

        if change_piece:
            for pos in format_shape(current_piece):
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = Tetromino(5, 0)
            change_piece = False

            if check_lost(locked_positions):
                run = False

    pygame.quit()

main()
