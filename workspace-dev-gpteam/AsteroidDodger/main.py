import pygame
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
ASTEROID_SIZE = 50
SHIELD_POWERUP_SIZE = 30
PLAYER_COLOR = (0, 255, 0)
ASTEROID_COLOR = (255, 0, 0)
SHIELD_POWERUP_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
FONT_NAME = pygame.font.match_font('arial')

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Asteroid Dodger')

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        self.y = SCREEN_HEIGHT - PLAYER_SIZE * 2
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.color = PLAYER_COLOR
        self.shield = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Boundary check
        self.x = max(self.x, 0)
        self.x = min(self.x, SCREEN_WIDTH - self.width)
        self.y = max(self.y, 0)
        self.y = min(self.y, SCREEN_HEIGHT - self.height)

# Asteroid class
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE)
        self.y = -ASTEROID_SIZE
        self.width = ASTEROID_SIZE
        self.height = ASTEROID_SIZE
        self.color = ASTEROID_COLOR
        self.speed = random.randint(2, 5)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

# ShieldPowerUp class
class ShieldPowerUp:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - SHIELD_POWERUP_SIZE)
        self.y = -SHIELD_POWERUP_SIZE
        self.width = SHIELD_POWERUP_SIZE
        self.height = SHIELD_POWERUP_SIZE
        self.color = SHIELD_POWERUP_COLOR

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += 3

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.asteroids = []
        self.shield_powerups = []
        self.score = 0
        self.high_score = 0
        self.start_time = time.time()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(0, -5)
            if keys[pygame.K_s]:
                self.player.move(0, 5)
            if keys[pygame.K_a]:
                self.player.move(-5, 0)
            if keys[pygame.K_d]:
                self.player.move(5, 0)

            # Spawn asteroids
            if random.randint(1, 20) == 1:
                self.asteroids.append(Asteroid())

            # Spawn shield power-ups
            if random.randint(1, 100) == 1:
                self.shield_powerups.append(ShieldPowerUp())

            # Move and draw asteroids
            for asteroid in self.asteroids[:]:
                asteroid.move()
                asteroid.draw()
                if asteroid.y > SCREEN_HEIGHT:
                    self.asteroids.remove(asteroid)
                    self.score += 1

            # Move and draw shield power-ups
            for powerup in self.shield_powerups[:]:
                powerup.move()
                powerup.draw()
                if powerup.y > SCREEN_HEIGHT:
                    self.shield_powerups.remove(powerup)

            # Check for collisions
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            for asteroid in self.asteroids[:]:
                asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
                if player_rect.colliderect(asteroid_rect):
                    if self.player.shield:
                        self.player.shield = False
                        self.asteroids.remove(asteroid)
                    else:
                        running = False
                        self.display_final_score()
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        self.reset_game()

            for powerup in self.shield_powerups[:]:
                powerup_rect = pygame.Rect(powerup.x, powerup.y, powerup.width, powerup.height)
                if player_rect.colliderect(powerup_rect):
                    self.player.shield = True
                    self.shield_powerups.remove(powerup)
                    self.score += 5

            # Draw player
            self.player.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

            # Update score based on survival time
            self.score += (time.time() - self.start_time) // 1
            self.start_time = time.time()

            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score

            # Display score
            self.display_score()

        pygame.quit()

    def display_score(self):
        font = pygame.font.Font(FONT_NAME, 36)
        score_text = font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def display_final_score(self):
        font = pygame.font.Font(FONT_NAME, 48)
        final_score_text = font.render(f'Final Score: {int(self.score)}', True, (255, 255, 255))
        high_score_text = font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - final_score_text.get_height() // 2))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + high_score_text.get_height()))

    def reset_game(self):
        self.player = Player()
        self.asteroids = []
        self.shield_powerups = []
        self.score = 0
        self.start_time = time.time()
        self.run()

# Main function
def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()