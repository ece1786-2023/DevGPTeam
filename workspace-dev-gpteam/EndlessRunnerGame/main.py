import pygame
import random
import sys
from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
ASTEROID_SIZE = 50
GRAVITY = 0.5
FLAP_STRENGTH = -10
ASTEROID_SPAWN_TIME = 5000  # milliseconds
ASTEROID_INCREASE_TIME = 5000  # milliseconds for increasing asteroid count
INITIAL_ASTEROID_COUNT = 3

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Endless Asteroid Runner')

# Load fonts
font = pygame.font.Font(None, 36)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.game_over()

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def game_over(self):
        pygame.event.post(pygame.event.Event(QUIT))

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed_range=(1, 5)):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_SIZE, ASTEROID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(random.choice([0, SCREEN_WIDTH]), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(*speed_range)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.asteroids = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.last_asteroid_spawn = pygame.time.get_ticks()
        self.asteroid_spawn_time = ASTEROID_SPAWN_TIME
        self.asteroid_speed_range = (1, 5)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        asteroid_count = INITIAL_ASTEROID_COUNT
        last_asteroid_increase = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.flap()

            # Spawn asteroids
            current_time = pygame.time.get_ticks()
            if current_time - self.last_asteroid_spawn > self.asteroid_spawn_time:
                self.last_asteroid_spawn = current_time
                for _ in range(asteroid_count):
                    new_asteroid = Asteroid(self.asteroid_speed_range)
                    self.asteroids.add(new_asteroid)
                    self.all_sprites.add(new_asteroid)

            # Increase asteroid count every 5 seconds
            if current_time - last_asteroid_increase > ASTEROID_INCREASE_TIME:
                last_asteroid_increase = current_time
                asteroid_count += 1

            # Update
            self.all_sprites.update()

            # Check for collisions
            if pygame.sprite.spritecollide(self.player, self.asteroids, False):
                running = False

            # Draw everything
            screen.fill(BLACK)
            self.all_sprites.draw(screen)

            # Display score
            score_text = font.render(f'Score: {self.score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

            # Increase score
            self.score += 1

            # Cap the frame rate
            clock.tick(60)

        pygame.quit()
        sys.exit()

# Main menu
def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    menu = False

        screen.fill(BLACK)
        title_text = font.render('Endless Asteroid Runner', True, WHITE)
        instruction_text = font.render('Press SPACE to start', True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2))
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

# Start the game
main_menu()
game = Game()
game.run()