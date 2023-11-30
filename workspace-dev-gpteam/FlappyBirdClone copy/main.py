import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_FLAP_POWER = 5
PIPE_SPEED = 4
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 200
GAME_SPEED_INCREASE = 0.4  # 40% increase
SPEED_INCREASE_INTERVAL = 5000  # in milliseconds

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# Set up the clock
clock = pygame.time.Clock()

# Load images
BIRD_IMAGE = pygame.Surface((30, 30))
BIRD_IMAGE.fill((255, 255, 0))
PIPE_IMAGE = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
PIPE_IMAGE.fill((0, 255, 0))

# Game variables
bird_pos = [50, SCREEN_HEIGHT // 2]
bird_vel = 0
bird_rect = BIRD_IMAGE.get_rect(center=bird_pos)
pipes = []
score = 0
game_speed = PIPE_SPEED
last_speed_increase = pygame.time.get_ticks()

# Main menu
def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        text = font.render('Click to Start', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.update()
        clock.tick(30)

# Game over
def game_over():
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        text = font.render('Game Over! Score: ' + str(score), True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        restart_text = font.render('Click to Restart', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

        pygame.display.update()
        clock.tick(30)

# Main game loop
def main():
    global bird_vel, bird_rect, pipes, score, game_speed, last_speed_increase

    main_menu()

    bird_vel = 0
    bird_rect = BIRD_IMAGE.get_rect(center=bird_pos)
    pipes.clear()
    score = 0
    game_speed = PIPE_SPEED
    last_speed_increase = pygame.time.get_ticks()

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_vel = -BIRD_FLAP_POWER

        # Bird physics
        bird_vel += GRAVITY
        bird_rect.centery += bird_vel

        # Pipe movement
        pipes = [(x - game_speed, y) for x, y in pipes]
        pipes = [(x, y) for x, y in pipes if x > -PIPE_WIDTH]

        # Add new pipes
        if not pipes or pipes[-1][0] < SCREEN_WIDTH - 300:
            pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
            pipes.append((SCREEN_WIDTH, pipe_height))

        # Check for collisions
        for x, y in pipes:
            pipe_rect_top = pygame.Rect(x, 0, PIPE_WIDTH, y)
            pipe_rect_bottom = pygame.Rect(x, y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - y - PIPE_GAP)
            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                game_over()
                return

        if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
            game_over()
            return

        # Increase game speed
        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase > SPEED_INCREASE_INTERVAL:
            game_speed *= (1 + GAME_SPEED_INCREASE)  # Increase by 40%
            last_speed_increase = current_time

        # Score
        for x, y in pipes:
            if bird_rect.centerx > x and bird_rect.centerx <= x + game_speed:
                score += 1

        # Drawing
        screen.fill((135, 206, 250))  # Sky blue background
        for x, y in pipes:
            screen.blit(PIPE_IMAGE, (x, y - PIPE_HEIGHT))
            screen.blit(PIPE_IMAGE, (x, y + PIPE_GAP))
        screen.blit(BIRD_IMAGE, bird_rect)

        # Display score
        font = pygame.font.SysFont(None, 32)
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()