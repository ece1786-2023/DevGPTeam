import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
screen_width, screen_height = 800, 600
bird_x, bird_y = 100, 300
bird_width, bird_height = 30, 30
bird_vel_y = 0
gravity = 0.5
flap_strength = -10
game_over = False
score = 0

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Pixel Bird")

# Bird color
bird_color = (255, 255, 0)  # Yellow

# Asteroid settings
asteroid_width, asteroid_height = 80, random.randint(150, 450)
asteroid_x = screen_width
asteroid_vel_x = -5
asteroid_gap = 200
asteroid_color = (169, 169, 169)  # Grey

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_vel_y = flap_strength

    # Bird movement
    bird_vel_y += gravity
    bird_y += bird_vel_y

    # Asteroid movement
    asteroid_x += asteroid_vel_x
    if asteroid_x < -asteroid_width:
        asteroid_x = screen_width
        asteroid_height = random.randint(150, 450)
        score += 1

    # Collision detection
    if bird_y > screen_height - bird_height or bird_y < 0:
        game_over = True
    if asteroid_x < bird_x < asteroid_x + asteroid_width and (bird_y < asteroid_height or bird_y > asteroid_height + asteroid_gap):
        game_over = True

    # Drawing
    pygame.draw.rect(screen, bird_color, (bird_x, bird_y, bird_width, bird_height))  # Bird
    pygame.draw.rect(screen, asteroid_color, (asteroid_x, 0, asteroid_width, asteroid_height))  # Top asteroid
    pygame.draw.rect(screen, asteroid_color, (asteroid_x, asteroid_height + asteroid_gap, asteroid_width, screen_height))  # Bottom asteroid

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit the game
pygame.quit()
