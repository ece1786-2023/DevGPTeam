import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_ROWS = 6
BOARD_COLS = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
PLAYER_1_COLOR = (255, 0, 0)  # Red
PLAYER_2_COLOR = (0, 0, 255)  # Blue
BG_COLOR = (30, 30, 30)
BOARD_COLOR = (0, 50, 50)
FONT_COLOR = (255, 255, 255)
GAME_TITLE = "Quad Connect"
FONT_NAME = "arial"

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# Font setup
font = pygame.font.SysFont(FONT_NAME, 72)
small_font = pygame.font.SysFont(FONT_NAME, 48)  # For player turn indicator

# Game variables
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
game_over = False
turn = 0

# Main menu button
start_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2, 300, 50)


def draw_board():
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS):
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BG_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, PLAYER_1_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), SCREEN_HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, PLAYER_2_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), SCREEN_HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def draw_main_menu():
    screen.fill(BG_COLOR)
    title_text = font.render(GAME_TITLE, True, FONT_COLOR)
    start_text = small_font.render("Start New Game", True, FONT_COLOR)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    start_rect = start_text.get_rect(center=start_button.center)
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, PLAYER_1_COLOR, start_button)  # Highlight the start button
    screen.blit(start_text, start_rect)
    pygame.display.update()


def restart_game():
    global board, game_over, turn
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    turn = 0
    draw_board()


def check_win(player):
    # Horizontal check
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    # Vertical check
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Positive diagonal check
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Negative diagonal check
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

    return False


def draw_winner(winner):
    screen.fill(BG_COLOR)
    if winner == 0:
        text = font.render("It's a draw!", True, FONT_COLOR)
    else:
        text = font.render(f"Player {winner} wins!", True, FONT_COLOR)
    rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(3000)
    restart_game()


def draw_turn_indicator(current_turn):
    turn_text = small_font.render(f"Player {current_turn + 1}'s turn", True, FONT_COLOR)
    turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
    pygame.draw.rect(screen, BG_COLOR, turn_rect.inflate(20, 10))  # Background for the text
    screen.blit(turn_text, turn_rect)
    pygame.display.update()


def main_menu():
    draw_main_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main_game_loop()


def main_game_loop():
    global turn, game_over
    draw_board()
    while not game_over:
        draw_turn_indicator(turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                col = int(x_pos // SQUARE_SIZE)

                if board[BOARD_ROWS - 1][col] == 0:
                    for r in range(BOARD_ROWS):
                        if board[r][col] == 0:
                            board[r][col] = turn + 1
                            if check_win(turn + 1):
                                game_over = True
                                draw_winner(turn + 1)
                            turn += 1
                            turn = turn % 2
                            break

                draw_board()

                # Check for draw
                if all(board[BOARD_ROWS - 1][col] != 0 for col in range(BOARD_COLS)) and not game_over:
                    game_over = True
                    draw_winner(0)

if __name__ == "__main__":
    main_menu()