import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 60
PIPE_HEIGHT = 500
PIPE_GAP = 160
GRAVITY = 0.25
FLAP_STRENGTH = -5
GAME_SPEED = 2
FONT_NAME = 'arial'
FONT_SIZE = 32
BACKGROUND_COLOR = (255, 255, 0)
BIRD_COLOR = (255, 0, 0)
PIPE_COLOR = (0, 128, 0)
TEXT_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Pixel Bird')

# Load font
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Game variables
clock = pygame.time.Clock()
score = 0
game_speed = GAME_SPEED
running = True
game_active = False
bird_movement = 0
bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
pipes = []

def draw_floor():
    pygame.draw.rect(screen, PIPE_COLOR, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

def create_pipe():
    pipe_pos = random.choice([300, 400, 500])
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_pos, PIPE_WIDTH, PIPE_HEIGHT)
    top_pipe = pygame.Rect(SCREEN_WIDTH, pipe_pos - PIPE_GAP - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= game_speed
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            pygame.draw.rect(screen, PIPE_COLOR, pipe)
        else:
            flip_pipe = pygame.transform.flip(pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT)), False, True)
            screen.blit(flip_pipe, pipe.topleft)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT - 100:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
    new_bird.fill(BIRD_COLOR)
    return new_bird

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = font.render(str(int(score)), True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = font.render(f'Score: {int(score)}', True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(f'Press Enter to Restart', True, TEXT_COLOR)
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(high_score_surface, high_score_rect)

def game_over_screen():
    screen.fill(BACKGROUND_COLOR)
    score_display('game_over')
    pygame.display.update()
    wait_for_restart()

def wait_for_restart():
    global game_active, score, pipes, bird_movement, bird_rect
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                score = 0
                pipes.clear()
                bird_rect.center = (50, SCREEN_HEIGHT // 2)
                bird_movement = 0
                restart = True

def main_game():
    global game_active, game_speed, score, bird_movement, pipes

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement += FLAP_STRENGTH
                if event.key == pygame.K_RETURN and not game_active:
                    game_active = True
                    score = 0
                    pipes.clear()
                    bird_rect.center = (50, SCREEN_HEIGHT // 2)
                    bird_movement = 0

        screen.fill(BACKGROUND_COLOR)
        if game_active:
            # Bird
            bird_movement += GRAVITY
            rotated_bird = rotate_bird(bird_animation())
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)

            # Pipes
            if len(pipes) == 0 or pipes[-1].centerx < SCREEN_WIDTH - 300:
                pipes.extend(create_pipe())
            pipes = move_pipes(pipes)
            draw_pipes(pipes)

            # Check collision
            game_active = check_collision(pipes)

            # Score
            score += 0.01
            score_display('main_game')
            game_speed += 0.001
        else:
            game_over_screen()

        # Floor
        draw_floor()

        pygame.display.update()
        clock.tick(120)

if __name__ == '__main__':
    main_game()