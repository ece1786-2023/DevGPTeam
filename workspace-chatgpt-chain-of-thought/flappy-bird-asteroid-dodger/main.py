import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BIRD_START_POS = (150, SCREEN_HEIGHT // 2)
GRAVITY = 0.5
FLAP_STRENGTH = -10
ASTEROID_FREQUENCY = 90 # Lower is more frequent
ASTEROID_SPEED = 5

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Asteroid Navigator")

# Load images and sounds here
# bird_img = pygame.image.load('path_to_bird_image.png')
# asteroid_img = pygame.image.load('path_to_asteroid_image.png')
# ... etc.

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = bird_img
        self.image = pygame.Surface((50, 50))  # Temporary square bird
        self.image.fill((255, 200, 0))  # Temporary color
        self.rect = self.image.get_rect(center=BIRD_START_POS)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Prevent bird from going off screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def flap(self):
        self.velocity = FLAP_STRENGTH

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = asteroid_img
        self.image = pygame.Surface((60, 60))  # Temporary square asteroid
        self.image.fill((140, 140, 140))  # Temporary color
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)))

    def update(self):
        self.rect.x -= ASTEROID_SPEED
        if self.rect.right < 0:
            self.kill()  # Remove asteroid if it's off the screen

# Game loop
def game_loop():
    bird = Bird()
    asteroids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(bird, asteroids)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Add asteroids
        if random.randint(1, ASTEROID_FREQUENCY) == 1:
            asteroid = Asteroid()
            asteroids.add(asteroid)
            all_sprites.add(asteroid)

        # Update
        all_sprites.update()

        # Collision check
        if pygame.sprite.spritecollideany(bird, asteroids):
            running = False  # End game on collision

        # Draw everything
        screen.fill((0, 0, 0))  # Fill screen with black (space)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

game_loop()
