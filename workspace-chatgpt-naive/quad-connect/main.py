import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game
BOARD_SIZE = 15
CELL_SIZE = 40
WINDOW_WIDTH = WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gomoku Connect Four")

def draw_board(board):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if board[y // CELL_SIZE][x // CELL_SIZE] != '.':
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                color = BLACK if board[y // CELL_SIZE][x // CELL_SIZE] == 'B' else WHITE
                pygame.draw.circle(screen, color, center, CELL_SIZE // 2 - 5)

def check_winner(board, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == player:
                for dx, dy in directions:
                    count = 0
                    for step in range(4):
                        nx, ny = x + step * dx, y + step * dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == player:
                            count += 1
                    if count == 4:
                        return True
    return False

def main():
    board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    player_turn = 0
    running = True
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if board[row][col] == '.':
                    board[row][col] = 'B' if player_turn == 0 else 'W'
                    if check_winner(board, board[row][col]):
                        winner = 'Black' if player_turn == 0 else 'White'
                    player_turn = 1 - player_turn

        screen.fill(BLACK)
        draw_board(board)
        pygame.display.flip()

        if winner:
            print(f"{winner} wins!")
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
