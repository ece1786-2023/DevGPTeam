import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define some constants
SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 20
WIDTH = HEIGHT = TILE_SIZE * SIZE + TILE_MARGIN * (SIZE + 1)
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    # ... add colors for more tiles if needed
}
FONT = pygame.font.SysFont("Arial", 48)
SCORE_FONT = pygame.font.SysFont("Arial", 36)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

def init_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board

def add_tile(board):
    empty_tiles = [(x, y) for x in range(SIZE) for y in range(SIZE) if board[x][y] == 0]
    if empty_tiles:
        x, y = random.choice(empty_tiles)
        board[x][y] = random.choice([2, 4])

def draw_board(screen, board, score):
    screen.fill(BACKGROUND_COLOR)
    for x in range(SIZE):
        for y in range(SIZE):
            value = board[x][y]
            tile_color = TILE_COLORS.get(value, (204, 192, 179))
            pygame.draw.rect(screen, tile_color,
                             (y * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                              x * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                              TILE_SIZE, TILE_SIZE))
            if value:
                text_surface = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(
                    y * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN + TILE_SIZE / 2,
                    x * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN + TILE_SIZE / 2))
                screen.blit(text_surface, text_rect)
    # Display the score
    text_surface = SCORE_FONT.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text_surface, (TILE_MARGIN, HEIGHT - TILE_MARGIN - 30))
    pygame.display.flip()

def compress(board):
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for x in range(SIZE):
        position = 0
        for y in range(SIZE):
            if board[x][y] != 0:
                new_board[x][position] = board[x][y]
                position += 1
    return new_board

def merge(board, score):
    for x in range(SIZE):
        for y in range(SIZE - 1):
            if board[x][y] == board[x][y + 1] and board[x][y] != 0:
                board[x][y] *= 2
                board[x][y + 1] = 0
                score += board[x][y]  # Increase the score with the new tile's value
    return board, score

def reverse(board):
    new_board = []
    for x in range(SIZE):
        new_board.append([])
        for y in range(SIZE):
            new_board[x].append(board[x][SIZE - y - 1])
    return new_board

def transpose(board):
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for x in range(SIZE):
        for y in range(SIZE):
            new_board[x][y] = board[y][x]
    return new_board

def move_left(board):
    board = compress(board)
    board = merge(board)
    board = compress(board)
    return board

def move_right(board):
    board = reverse(board)
    board = compress(board)
    board = merge(board)
    board = compress(board)
    board = reverse(board)
    return board

def move_up(board):
    board = transpose(board)
    board = compress(board)
    board = merge(board)
    board = compress(board)
    board = transpose(board)
    return board

def move_down(board):
    board = transpose(board)
    board = reverse(board)
    board = compress(board)
    board = merge(board)
    board = compress(board)
    board = reverse(board)
    board = transpose(board)
    return board

def can_move(board):
    for x in range(SIZE):
        for y in range(SIZE):
            if board[x][y] == 0:
                return True
            if y < SIZE - 1 and board[x][y] == board[x][y + 1]:
                return True
            if x < SIZE - 1 and board[x][y] == board[x + 1][y]:
                return True
    return False

def main():
    board = init_board()
    score = 0
    while True:
        draw_board(SCREEN, board, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                valid_move = False
                if event.key == pygame.K_LEFT:
                    old_board = [row[:] for row in board]
                    board, score = merge(compress(board), score)
                    valid_move = board != old_board
                elif event.key == pygame.K_RIGHT:
                    old_board = [row[:] for row in board]
                    board = reverse(board)
                    board, score = merge(compress(board), score)
                    board = reverse(board)
                    valid_move = board != old_board
                elif event.key == pygame.K_UP:
                    old_board = [row[:] for row in board]
                    board = transpose(board)
                    board, score = merge(compress(board), score)
                    board = transpose(board)
                    valid_move = board != old_board
                elif event.key == pygame.K_DOWN:
                    old_board = [row[:] for row in board]
                    board = transpose(board)
                    board = reverse(board)
                    board, score = merge(compress(board), score)
                    board = reverse(board)
                    board = transpose(board)
                    valid_move = board != old_board
                
                if valid_move:
                    add_tile(board)
                
                if not can_move(board):
                    # If no moves are possible, display game over message and break loop
                    draw_board(SCREEN, board, score)
                    text_surface = SCORE_FONT.render('Game Over!', True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    SCREEN.blit(text_surface, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    return  # End the game

if __name__ == '__main__':
    main()
