import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_FLAP_POWER = 5
OBSTACLE_SPEED = 5
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 500
OBSTACLE_GAP = 200
SPEED_INCREASE_INTERVAL = 5000  # in milliseconds
SPEED_INCREASE_FACTOR = 1.4

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# Load images
BIRD_IMAGE = pygame.Surface((30, 30))
BIRD_IMAGE.fill((255, 255, 0))
OBSTACLE_IMAGE = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
OBSTACLE_IMAGE.fill((0, 255, 0))

# Game variables
bird_pos = [50, SCREEN_HEIGHT // 2]
bird_vel = 0
obstacles = []
score = 0
high_score = 0
speed = OBSTACLE_SPEED
last_speed_increase = pygame.time.get_ticks()

# Main menu
def main_menu():
    global high_score
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)
        text = font.render('Flappy Bird Clone', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text, text_rect)

        start_button = font.render('Start Game', True, (255, 255, 255))
        start_button_rect = start_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(start_button, start_button_rect)

        high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(high_score_text, high_score_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False

# Game loop
def game_loop():
    global bird_pos, bird_vel, obstacles, score, high_score, speed, last_speed_increase
    clock = pygame.time.Clock()
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
        bird_pos[1] += bird_vel

        # Move obstacles
        obstacles = [(obs[0] - speed, obs[1]) for obs in obstacles if obs[0] > -OBSTACLE_WIDTH]

        # Add new obstacle
        if not obstacles or obstacles[-1][0] < SCREEN_WIDTH - 300:
            height = random.randint(100, SCREEN_HEIGHT - 100 - OBSTACLE_GAP)
            obstacles.append((SCREEN_WIDTH, height))

        # Check for collisions
        bird_rect = pygame.Rect(bird_pos[0], bird_pos[1], BIRD_IMAGE.get_width(), BIRD_IMAGE.get_height())
        for obs in obstacles:
            obs_rect_top = pygame.Rect(obs[0], 0, OBSTACLE_WIDTH, obs[1])
            obs_rect_bottom = pygame.Rect(obs[0], obs[1] + OBSTACLE_GAP, OBSTACLE_WIDTH, SCREEN_HEIGHT)
            if bird_rect.colliderect(obs_rect_top) or bird_rect.colliderect(obs_rect_bottom):
                running = False
            if bird_pos[1] > SCREEN_HEIGHT or bird_pos[1] < 0:
                running = False

        # Increase speed
        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase > SPEED_INCREASE_INTERVAL:
            speed *= SPEED_INCREASE_FACTOR
            last_speed_increase = current_time

        # Update score
        score += 1
        high_score = max(high_score, score)

        # Draw everything
        screen.fill((0, 0, 0))
        for obs in obstacles:
            screen.blit(OBSTACLE_IMAGE, (obs[0], 0))
            screen.blit(OBSTACLE_IMAGE, (obs[0], obs[1] + OBSTACLE_GAP))
        screen.blit(BIRD_IMAGE, bird_pos)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Draw speed
        speed_text = font.render(f'Speed: {speed:.1f}', True, (255, 255, 255))
        screen.blit(speed_text, (10, 50))

        pygame.display.flip()
        clock.tick(30)

    # Game over
    game_over()

# Game over screen
def game_over():
    global bird_pos, bird_vel, obstacles, score, speed, last_speed_increase
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)
        text = font.render('Game Over', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text, text_rect)

        restart_button = font.render('Restart', True, (255, 255, 255))
        restart_button_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_button, restart_button_rect)

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(score_text, score_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    bird_pos = [50, SCREEN_HEIGHT // 2]
                    bird_vel = 0
                    obstacles = []
                    score = 0
                    speed = OBSTACLE_SPEED
                    last_speed_increase = pygame.time.get_ticks()
                    running = False

    main_menu()

# Start the game
main_menu()
game_loop()