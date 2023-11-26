import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
screen_width = 400
screen_height = 600
bird_x = 50
bird_y = 300
bird_width = 40
bird_height = 40
bird_gravity = 0.5
bird_jump = -10
bird_velocity = 0
ground_height = screen_height - 70
pipe_width = 70
pipe_height = random.randint(150, 450)
pipe_x = screen_width - 50
pipe_gap = 200
scroll_speed = 2.5
score = 0

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # Bird
    bird_y += bird_velocity
    bird_velocity += bird_gravity
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    pygame.draw.rect(screen, YELLOW, bird_rect)

    # Pipes
    pipe_x -= scroll_speed
    upper_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    lower_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap)
    pygame.draw.rect(screen, GREEN, upper_pipe)
    pygame.draw.rect(screen, GREEN, lower_pipe)

    # Scoring
    if pipe_x < bird_x and not upper_pipe.colliderect(bird_rect) and not lower_pipe.colliderect(bird_rect):
        score += 1
        print("Score:", score)
        pipe_x = screen_width
        pipe_height = random.randint(150, 450)

    # Collision detection
    if bird_rect.colliderect(upper_pipe) or bird_rect.colliderect(lower_pipe) or bird_y > ground_height:
        running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                bird_velocity = bird_jump

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
