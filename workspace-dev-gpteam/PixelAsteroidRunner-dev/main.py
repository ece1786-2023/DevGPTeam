import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
ASTEROID_SIZE = 50
GRAVITY = 0.5
JUMP_STRENGTH = 10
ASTEROID_SPAWN_RATE = 1500  # in milliseconds
GAME_FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pixel Asteroid Runner')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.move_ip(0, self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((ASTEROID_SIZE, ASTEROID_SIZE))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Main menu
def main_menu():
    title_font = pygame.font.Font(None, 54)
    title_text = title_font.render('Pixel Asteroid Runner', True, WHITE)
    play_button = GAME_FONT.render('Play', True, WHITE)
    play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(play_button, play_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        pygame.display.flip()

# Game loop
def game():
    player = Player()
    asteroids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    score = 0
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, ASTEROID_SPAWN_RATE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                new_asteroid = Asteroid()
                asteroids.add(new_asteroid)
                all_sprites.add(new_asteroid)
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                player.jump()

        all_sprites.update()

        if pygame.sprite.spritecollideany(player, asteroids):
            running = False

        screen.fill(BLACK)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        score += 1
        score_text = GAME_FONT.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    return score

# Post-game screen
def game_over(score):
    game_over_text = GAME_FONT.render('Game Over', True, WHITE)
    score_text = GAME_FONT.render(f'Final Score: {score}', True, WHITE)
    restart_text = GAME_FONT.render('Click to Restart', True, WHITE)

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 1.5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                running = False

        pygame.display.flip()

# Main function
def main():
    main_menu()
    score = game()
    game_over(score)
    main()

if __name__ == '__main__':
    main()