import pygame
import sys

# Constants
BOARD_SIZE = 15
SQUARE_SIZE = 40
BOARD_WIDTH = BOARD_SIZE * SQUARE_SIZE
BOARD_HEIGHT = BOARD_SIZE * SQUARE_SIZE
WINDOW_WIDTH = BOARD_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
FONT_COLOR = (50, 50, 50)
PLAYER_ONE = 1
PLAYER_TWO = 2

# Initialize Pygame
pygame.init()

# Set up the display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quad Connect")

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = PLAYER_ONE
game_over = False
winner = None

def draw_board():
    window.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(window, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.line(window, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100), ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE + 100))
            pygame.draw.line(window, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100), (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE + 100))
            if board[row][col] == PLAYER_ONE:
                pygame.draw.circle(window, BLACK, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2 + 100)), int(SQUARE_SIZE / 2 - 5))
            elif board[row][col] == PLAYER_TWO:
                pygame.draw.circle(window, WHITE, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2 + 100)), int(SQUARE_SIZE / 2 - 5))

def draw_menu():
    title_text = font.render("Quad Connect", True, FONT_COLOR)
    start_text = font.render("Start New Game", True, FONT_COLOR)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, 50))
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    window.blit(title_text, title_rect)
    window.blit(start_text, start_rect)

def check_win(player):
    # Horizontal check
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True
    # Vertical check
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True
    # Positive diagonal check
    for row in range(BOARD_SIZE - 3):
        for col in range(BOARD_SIZE - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
    # Negative diagonal check
    for row in range(3, BOARD_SIZE):
        for col in range(BOARD_SIZE - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True
    return False

def check_draw():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return False
    return True

def restart_game():
    global board, current_player, game_over, winner
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = PLAYER_ONE
    game_over = False
    winner = None

def main():
    global current_player, game_over, winner
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = pygame.mouse.get_pos()
                col = mouseX // SQUARE_SIZE
                row = (mouseY - 100) // SQUARE_SIZE
                if board[row][col] == 0:
                    board[row][col] = current_player
                    if check_win(current_player):
                        game_over = True
                        winner = current_player
                    elif check_draw():
                        game_over = True
                        winner = None
                    current_player = PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()

        draw_board()
        if game_over:
            if winner is not None:
                win_text = font.render(f"Player {winner} wins!", True, FONT_COLOR)
            else:
                win_text = font.render("It's a draw!", True, FONT_COLOR)
            win_rect = win_text.get_rect(center=(WINDOW_WIDTH / 2, 50))
            window.blit(win_text, win_rect)
        else:
            turn_text = font.render(f"Player {current_player}'s turn", True, FONT_COLOR)
            turn_rect = turn_text.get_rect(center=(WINDOW_WIDTH / 2, 50))
            window.blit(turn_text, turn_rect)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()