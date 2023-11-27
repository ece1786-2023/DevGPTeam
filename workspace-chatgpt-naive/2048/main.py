import random

def initialize_game():
    board = [[0]*4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            board[row][col] = 2 if random.random() < 0.9 else 4
            break

def print_board(board):
    for row in board:
        print("\t".join(map(str, row)))
    print()

def compress(board):
    new_board = [[0]*4 for _ in range(4)]
    for i in range(4):
        position = 0
        for j in range(4):
            if board[i][j] != 0:
                new_board[i][position] = board[i][j]
                position += 1
    return new_board

def merge(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j+1] = 0
    return board

def reverse(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[i][3-j])
    return new_board

def transpose(board):
    new_board = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_board[i][j] = board[j][i]
    return new_board

def move_left(board):
    board = compress(board)
    board = merge(board)
    board = compress(board)
    return board

def move_right(board):
    board = reverse(board)
    board = move_left(board)
    board = reverse(board)
    return board

def move_up(board):
    board = transpose(board)
    board = move_left(board)
    board = transpose(board)
    return board

def move_down(board):
    board = transpose(board)
    board = move_right(board)
    board = transpose(board)
    return board

def check_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if j < 3 and board[i][j] == board[i][j+1]:
                return False
            if i < 3 and board[i][j] == board[i+1][j]:
                return False
    return True

def main():
    board = initialize_game()
    print_board(board)
    game_over = False

    while not game_over:
        move = input("Enter your move (W/A/S/D): ").upper()
        if move == 'W':
            board = move_up(board)
            add_new_tile(board)
        elif move == 'A':
            board = move_left(board)
            add_new_tile(board)
        elif move == 'S':
            board = move_down(board)
            add_new_tile(board)
        elif move == 'D':
            board = move_right(board)
            add_new_tile(board)
        else:
            print("Invalid move. Please enter W, A, S, or D.")
            continue

        print_board(board)

        if check_game_over(board):
            print("Game Over!")
            game_over = True

if __name__ == "__main__":
    main()
