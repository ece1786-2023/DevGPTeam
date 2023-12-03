import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
BALL_SPEED_INCREMENT = 0.5
PADDLE_SPEED = 10
FONT_SIZE = 32
WINNING_SCORE = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Initialize clock
clock = pygame.time.Clock()

# Initialize font
font = pygame.font.Font(None, FONT_SIZE)

# Game states
running = True
paused = False

# Game variables
left_score = 0
right_score = 0
ball_speed_x = BALL_SPEED_INCREMENT * random.choice((1, -1))
ball_speed_y = BALL_SPEED_INCREMENT * random.choice((1, -1))
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
left_paddle_pos = [0, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
right_paddle_pos = [SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]

def reset_ball():
    global ball_pos, ball_speed_x, ball_speed_y
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    ball_speed_x = BALL_SPEED_INCREMENT * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_INCREMENT * random.choice((1, -1))

def draw_startup_screen():
    screen.fill(BLACK)
    title_text = font.render('Pong', True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(title_text, title_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (*left_paddle_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (*right_paddle_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (*ball_pos, BALL_SIZE, BALL_SIZE))
    left_score_text = font.render(str(left_score), True, WHITE)
    right_score_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (SCREEN_WIDTH // 4, FONT_SIZE))
    screen.blit(right_score_text, (3 * SCREEN_WIDTH // 4, FONT_SIZE))
    pygame.display.flip()

def move_paddles(keys):
    if keys[pygame.K_w] and left_paddle_pos[1] > 0:
        left_paddle_pos[1] -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_pos[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
        left_paddle_pos[1] += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle_pos[1] > 0:
        right_paddle_pos[1] -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_pos[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
        right_paddle_pos[1] += PADDLE_SPEED

def move_ball():
    global ball_speed_x, ball_speed_y, left_score, right_score, running
    ball_pos[0] += ball_speed_x
    ball_pos[1] += ball_speed_y

    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    if ball_pos[0] <= PADDLE_WIDTH and left_paddle_pos[1] < ball_pos[1] < left_paddle_pos[1] + PADDLE_HEIGHT:
        ball_speed_x *= -1
        ball_speed_x += BALL_SPEED_INCREMENT if ball_speed_x > 0 else -BALL_SPEED_INCREMENT
        ball_speed_y += BALL_SPEED_INCREMENT if ball_speed_y > 0 else -BALL_SPEED_INCREMENT
    elif ball_pos[0] >= SCREEN_WIDTH - PADDLE_WIDTH and right_paddle_pos[1] < ball_pos[1] < right_paddle_pos[1] + PADDLE_HEIGHT:
        ball_speed_x *= -1
        ball_speed_x += BALL_SPEED_INCREMENT if ball_speed_x > 0 else -BALL_SPEED_INCREMENT
        ball_speed_y += BALL_SPEED_INCREMENT if ball_speed_y > 0 else -BALL_SPEED_INCREMENT
    elif ball_pos[0] < 0:
        right_score += 1
        reset_ball()
    elif ball_pos[0] > SCREEN_WIDTH:
        left_score += 1
        reset_ball()

    if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
        running = False

def display_winner():
    winner_text = font.render(f'Player {"Left" if left_score > right_score else "Right"} wins!', True, WHITE)
    winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(winner_text, winner_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    global paused, running

    draw_startup_screen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            move_paddles(keys)
            move_ball()
            draw_game()

        clock.tick(60)

    display_winner()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()