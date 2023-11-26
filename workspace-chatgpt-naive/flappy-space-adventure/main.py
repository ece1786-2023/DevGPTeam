import pygame
import random

# Initialize Pygame
pygame.init()

# Game Variables
screen_width = 800
screen_height = 600
bird_x = 100
bird_y = screen_height // 2
bird_speed = 0
gravity = 0.5
flap_power = -10
game_over = False
score = 0

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Space Adventure')

# Load bird image
bird_img = pygame.Surface((50, 50))
bird_img.fill((255, 200, 0))  # A simple square to represent the bird

# Function to draw the bird
def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

# Function to create asteroids
def create_asteroid():
    height = random.randint(100, 400)
    width = random.randint(20, 70)
    x = screen_width
    y = random.randint(0, screen_height - height)
    return pygame.Rect(x, y, width, height)

# Function to draw asteroids
def draw_asteroids(asteroids):
    for asteroid in asteroids:
        pygame.draw.rect(screen, (169, 169, 169), asteroid)

# Asteroids List
asteroids = [create_asteroid() for _ in range(5)]

# Main game loop
clock = pygame.time.Clock()
while not game_over:
    screen.fill((0, 0, 0))  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = flap_power

    # Bird physics
    bird_speed += gravity
    bird_y += bird_speed

    # Asteroid movement
    for asteroid in asteroids:
        asteroid.x -= 5  # Move asteroid left
        if asteroid.x < -asteroid.width:  # If asteroid is off-screen, reset it
            asteroids.remove(asteroid)
            asteroids.append(create_asteroid())
            score += 1

    # Collision detection
    bird_rect = pygame.Rect(bird_x, bird_y, bird_img.get_width(), bird_img.get_height())
    for asteroid in asteroids:
        if bird_rect.colliderect(asteroid):
            game_over = True

    # Drawing
    draw_bird()
    draw_asteroids(asteroids)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()  # Update the display
    clock.tick(30)  # Frame rate

pygame.quit()
