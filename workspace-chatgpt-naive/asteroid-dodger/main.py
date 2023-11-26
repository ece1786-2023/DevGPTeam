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

# Player variables
player_size = 50
player_pos = [WIDTH//2, HEIGHT-2*player_size]
player_speed = 10

# Enemy variables
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
enemy_speed = 10

clock = pygame.time.Clock()

# Game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    screen.fill(BLACK)

    # Update enemy position
    if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
        enemy_pos[1] += enemy_speed
    else:
        enemy_pos[1] = 0
        enemy_pos[0] = random.randint(0, WIDTH-enemy_size)

    # Collision detection
    if player_pos[1] < enemy_pos[1] + enemy_size and player_pos[1] + player_size > enemy_pos[1]:
        if player_pos[0] < enemy_pos[0] + enemy_size and player_pos[0] + player_size > enemy_pos[0]:
            game_over = True

    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, WHITE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
