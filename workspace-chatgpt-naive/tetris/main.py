import pygame
import random

# Pygame Initialization
pygame.init()

# Set up the display
WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan I
    (0, 0, 255),    # Blue J
    (255, 165, 0),  # Orange L
    (255, 255, 0),  # Yellow O
    (0, 255, 0),    # Green S
    (255, 0, 0),    # Red Z
    (128, 0, 128)   # Purple T
]

# Tetromino shapes
TETROMINOS = [
    [[1, 1, 1, 1]], # I
    [[1, 0, 0],     # J
     [1, 1, 1]],
    [[0, 0, 1],     # L
     [1, 1, 1]],
    [[1, 1],        # O
     [1, 1]],
    [[0, 1, 1],     # S
     [1, 1, 0]],
    [[1, 1, 0],     # Z
     [0, 1, 1]],
    [[0, 1, 0],     # T
     [1, 1, 1]]
]

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state

    # Draw everything
    pygame.display.flip()

pygame.quit()
