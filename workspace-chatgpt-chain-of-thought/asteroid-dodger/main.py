import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodger")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Player (spaceship)
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

# Asteroid
asteroid_size = 50
asteroid_pos = [random.randint(0, WIDTH - asteroid_size), 0]
asteroid_list = [asteroid_pos]

# Game speed
speed = 10

# Clock
clock = pygame.time.Clock()

# Game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += 5

    # Update asteroid position
    if asteroid_pos[1] >= 0 and asteroid_pos[1] < HEIGHT:
        asteroid_pos[1] += speed
    else:
        asteroid_pos = [random.randint(0, WIDTH - asteroid_size), 0]

    # Collision detection
    if player_pos[1] < asteroid_pos[1] + asteroid_size and \
       player_pos[1] + player_size > asteroid_pos[1] and \
       player_pos[0] < asteroid_pos[0] + asteroid_size and \
       player_pos[0] + player_size > asteroid_pos[0]:
        game_over = True

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, GRAY, (asteroid_pos[0], asteroid_pos[1], asteroid_size, asteroid_size))
    pygame.display.update()

    # Control game speed
    clock.tick(30)

# Quit game
pygame.quit()
