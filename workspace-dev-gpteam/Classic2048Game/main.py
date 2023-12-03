import tkinter as tk
import random
import numpy as np

class Game2048:
    def __init__(self, root):
        self.root = root
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.tile_colors = {
            0: "#9e948a",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        self.init_ui()
        self.start_game()

    def init_ui(self):
        self.root.title('2048 Game')
        self.root.resizable(False, False)
        self.board_frame = tk.Frame(self.root, bg='azure3')
        self.board_frame.grid()
        self.tiles = {}
        for i in range(4):
            for j in range(4):
                tile = tk.Label(self.board_frame, text='', bg=self.tile_colors[0], font=('Helvetica', 22, 'bold'), width=4, height=2)
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[(i, j)] = tile
        self.score_label = tk.Label(self.root, text=f'Score: {self.score}', font=('Helvetica', 18, 'bold'))
        self.score_label.grid()
        self.root.bind('<Up>', self.up)
        self.root.bind('<Down>', self.down)
        self.root.bind('<Left>', self.left)
        self.root.bind('<Right>', self.right)
        self.root.bind('<r>', self.restart_game)

    def start_game(self):
        self.place_random_tile()
        self.place_random_tile()
        self.update_ui()

    def place_random_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = random.choice([2, 4])

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                self.tiles[(i, j)].config(text=str(value) if value > 0 else '', bg=self.tile_colors[value])
        self.score_label.config(text=f'Score: {self.score}')

    def compress(self, grid):
        new_grid = np.zeros((4, 4), dtype=int)
        for i in range(4):
            pos = 0
            for j in range(4):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    pos += 1
        return new_grid

    def merge(self, grid):
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    grid[i][j + 1] = 0
                    self.score += grid[i][j]
        return grid

    def reverse(self, grid):
        new_grid = []
        for i in range(4):
            new_grid.append([])
            for j in range(4):
                new_grid[i].append(grid[i][3 - j])
        return np.array(new_grid)

    def transpose(self, grid):
        return np.transpose(grid)

    def move(self, direction):
        if direction == 'up':
            self.grid = self.transpose(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.transpose(self.grid)
        elif direction == 'down':
            self.grid = self.transpose(self.grid)
            self.grid = self.reverse(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.reverse(self.grid)
            self.grid = self.transpose(self.grid)
        elif direction == 'left':
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
        elif direction == 'right':
            self.grid = self.reverse(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.merge(self.grid)
            self.grid = self.compress(self.grid)
            self.grid = self.reverse(self.grid)
        self.place_random_tile()
        self.update_ui()
        if self.is_game_over():
            self.game_over()

    def up(self, event):
        self.move('up')

    def down(self, event):
        self.move('down')

    def left(self, event):
        self.move('left')

    def right(self, event):
        self.move('right')

    def restart_game(self, event):
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.start_game()

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def game_over(self):
        game_over_frame = tk.Frame(self.root, borderwidth=2, relief='raised')
        game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(game_over_frame, text='Game Over!', font=('Helvetica', 18, 'bold')).pack()
        tk.Button(game_over_frame, text='Restart', command=lambda: [game_over_frame.destroy(), self.restart_game(None)]).pack()

if __name__ == '__main__':
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()