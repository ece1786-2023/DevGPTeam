import pygame
import random

# Initialize Pygame
pygame.init()

# Game Variables
screen_width = 400
screen_height = 600
bird_y = screen_height // 2
bird_x = 50
bird_move = 0
gravity = 0.25
game_active = True
score = 0
high_score = 0

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# Colors
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
BLUE = (135, 206, 235)

# Pipe settings
pipe_height = [200, 300, 400]
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_gap = 150
pipe_width = 70

def draw_bird(bird_y):
    pygame.draw.ellipse(screen, YELLOW, (bird_x, bird_y, 35, 25))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pygame.Rect(screen_width, random_pipe_pos, pipe_width, screen_height - random_pipe_pos)
    top_pipe = pygame.Rect(screen_width, 0, pipe_width, random_pipe_pos - pipe_gap)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes):
    bird_rect = pygame.Rect(bird_x, bird_y, 35, 25)
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= screen_height:
        return False

    return True

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def score_display(game_active):
    if game_active:
        score_surface = font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(200, 50))
        screen.blit(score_surface, score_rect)
    else:
        high_score_surface = font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(200, 50))
        screen.blit(high_score_surface, high_score_rect)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            bird_move = 0
            bird_move -= 6
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.fill(BLUE)  # Background color

    if game_active:
        # Bird
        bird_move += gravity
        bird_y += bird_move
        draw_bird(bird_y)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display(game_active)
    else:
        high_score = update_score(score, high_score)
        score_display(game_active)

    pygame.display.update()
    clock.tick(120)
