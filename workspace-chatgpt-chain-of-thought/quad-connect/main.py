import tkinter as tk
from tkinter import messagebox

class GomokuGUI:
    def __init__(self, size=15):
        self.size = size
        self.root = tk.Tk()
        self.root.title("Gomoku")
        self.canvas_size = 600
        self.cell_size = self.canvas_size / self.size
        self.canvas = tk.Canvas(self.root, height=self.canvas_size, width=self.canvas_size, bg='white')
        self.canvas.pack()
        self.initialize_board()
        self.player_turn = 'X'
        self.canvas.bind("<Button-1>", self.handle_click)

    def initialize_board(self):
        for i in range(self.size):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.canvas_size)
            self.canvas.create_line(0, i * self.cell_size, self.canvas_size, i * self.cell_size)
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]

    def draw_piece(self, row, col, player):
        x0 = col * self.cell_size + self.cell_size / 4
        y0 = row * self.cell_size + self.cell_size / 4
        x1 = col * self.cell_size + 3 * self.cell_size / 4
        y1 = row * self.cell_size + 3 * self.cell_size / 4
        color = 'black' if player == 'X' else 'white'
        self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)

    def handle_click(self, event):
        row = int(event.y // self.cell_size)
        col = int(event.x // self.cell_size)
        if self.is_valid_move(row, col):
            self.place_piece(row, col, self.player_turn)
            if self.check_win(row, col):
                self.display_winner(f"Player {self.player_turn} wins!")
                self.canvas.unbind("<Button-1>")
            self.switch_player()

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == '.'

    def place_piece(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.draw_piece(row, col, player)

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # horizontal, vertical, diagonal down, diagonal up
        for dr, dc in directions:
            count = 0
            for i in range(-3, 4):  # Check 3 spaces in each direction
                r, c = row + dr*i, col + dc*i
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.player_turn:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def switch_player(self):
        self.player_turn = 'O' if self.player_turn == 'X' else 'X'

    def display_winner(self, message):
        messagebox.showinfo("Game Over", message)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = GomokuGUI()
    game.run()
