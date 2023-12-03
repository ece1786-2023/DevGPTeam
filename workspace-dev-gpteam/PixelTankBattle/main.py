import pygame
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_SIZE = 40
TURRET_LENGTH = 25
PROJECTILE_RADIUS = 4
OBSTACLE_SIZE = 40
POWER_UP_SIZE = 30
ENEMY_TANK_COUNT = 2
MAZE_ROWS = 10
MAZE_COLS = 15
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pixel Tank Battle')
clock = pygame.time.Clock()

# Game variables
player_position = [100, 100]  # Changed to list to allow item assignment
player_angle = 0
player_turret_angle = 0
player_speed = 2
player_rotation_speed = 2
projectiles = []
enemies = []
obstacles = []
power_ups = []
score = 0
game_over = False
power_up_active = False
power_up_type = None
power_up_timer = 0

# Functions
def draw_tank(position, angle, turret_angle, color):
    # Draw tank body
    tank_rect = pygame.Rect(0, 0, TANK_SIZE, TANK_SIZE)
    tank_rect.center = position
    pygame.draw.rect(screen, color, tank_rect)

    # Draw turret
    end_x = position[0] + math.cos(math.radians(turret_angle)) * TURRET_LENGTH
    end_y = position[1] + math.sin(math.radians(turret_angle)) * TURRET_LENGTH
    pygame.draw.line(screen, color, position, (end_x, end_y), 4)

def move_tank(position, angle, speed):
    new_x = position[0] + math.cos(math.radians(angle)) * speed
    new_y = position[1] + math.sin(math.radians(angle)) * speed
    return [new_x, new_y]  # Changed to list to allow item assignment

def rotate_tank(angle, rotation_speed, direction):
    return angle + (rotation_speed * direction)

def fire_projectile(position, angle):
    end_x = position[0] + math.cos(math.radians(angle)) * (TURRET_LENGTH + PROJECTILE_RADIUS)
    end_y = position[1] + math.sin(math.radians(angle)) * (TURRET_LENGTH + PROJECTILE_RADIUS)
    projectiles.append({'position': [end_x, end_y], 'angle': angle})  # Changed to list to allow item assignment

def draw_projectiles():
    for projectile in projectiles:
        pygame.draw.circle(screen, RED, projectile['position'], PROJECTILE_RADIUS)

def move_projectiles():
    for projectile in projectiles:
        new_x = projectile['position'][0] + math.cos(math.radians(projectile['angle'])) * 5
        new_y = projectile['position'][1] + math.sin(math.radians(projectile['angle'])) * 5
        projectile['position'] = [new_x, new_y]  # Changed to list to allow item assignment

def generate_maze():
    for row in range(MAZE_ROWS):
        for col in range(MAZE_COLS):
            if random.choice([True, False]):
                obstacles.append(pygame.Rect(col * OBSTACLE_SIZE, row * OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE))

def draw_maze():
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, obstacle)

def spawn_enemies():
    while len(enemies) < ENEMY_TANK_COUNT:
        x = random.randint(0, SCREEN_WIDTH - TANK_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - TANK_SIZE)
        enemy_rect = pygame.Rect(x, y, TANK_SIZE, TANK_SIZE)
        if not any(enemy_rect.colliderect(obstacle) for obstacle in obstacles):
            enemies.append({'position': [x, y], 'angle': 0, 'turret_angle': random.randint(0, 360)})  # Changed to list to allow item assignment

def draw_enemies():
    for enemy in enemies:
        draw_tank(enemy['position'], enemy['angle'], enemy['turret_angle'], BLUE)

def spawn_power_up():
    valid_position = False
    while not valid_position:
        x = random.randint(0, SCREEN_WIDTH - POWER_UP_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - POWER_UP_SIZE)
        power_up_rect = pygame.Rect(x, y, POWER_UP_SIZE, POWER_UP_SIZE)
        if not any(power_up_rect.colliderect(obstacle) for obstacle in obstacles):
            valid_position = True
            power_ups.append({'position': [x, y], 'type': random.choice(['speed', 'shield', 'power'])})  # Changed to list to allow item assignment

def draw_power_ups():
    for power_up in power_ups:
        if power_up['type'] == 'speed':
            color = YELLOW
        elif power_up['type'] == 'shield':
            color = WHITE
        else:  # 'power'
            color = RED
        pygame.draw.rect(screen, color, pygame.Rect(power_up['position'][0], power_up['position'][1], POWER_UP_SIZE, POWER_UP_SIZE))

def check_collisions():
    global game_over, score, power_up_active, power_up_type, power_up_timer
    player_rect = pygame.Rect(player_position[0] - TANK_SIZE / 2, player_position[1] - TANK_SIZE / 2, TANK_SIZE, TANK_SIZE)
    
    # Check projectile collisions with obstacles
    for projectile in projectiles[:]:
        projectile_rect = pygame.Rect(projectile['position'][0] - PROJECTILE_RADIUS, projectile['position'][1] - PROJECTILE_RADIUS, PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2)
        for obstacle in obstacles[:]:
            if projectile_rect.colliderect(obstacle):
                obstacles.remove(obstacle)
                projectiles.remove(projectile)
                break
    
    # Check projectile collisions with enemies
    for projectile in projectiles[:]:
        projectile_rect = pygame.Rect(projectile['position'][0] - PROJECTILE_RADIUS, projectile['position'][1] - PROJECTILE_RADIUS, PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy['position'][0] - TANK_SIZE / 2, enemy['position'][1] - TANK_SIZE / 2, TANK_SIZE, TANK_SIZE)
            if projectile_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                score += 100
                if len(enemies) == ENEMY_TANK_COUNT - 1:
                    spawn_power_up()
                break
    
    # Check player collisions with power-ups
    for power_up in power_ups[:]:
        power_up_rect = pygame.Rect(power_up['position'][0], power_up['position'][1], POWER_UP_SIZE, POWER_UP_SIZE)
        if player_rect.colliderect(power_up_rect):
            power_up_active = True
            power_up_type = power_up['type']
            power_up_timer = pygame.time.get_ticks()
            power_ups.remove(power_up)
    
    # Check player collisions with enemies
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy['position'][0] - TANK_SIZE / 2, enemy['position'][1] - TANK_SIZE / 2, TANK_SIZE, TANK_SIZE)
        if player_rect.colliderect(enemy_rect):
            game_over = True
    
    # Check if game is over
    if len(enemies) == 0:
        game_over = True

def apply_power_up():
    global player_speed, power_up_active, power_up_timer
    if power_up_active:
        current_time = pygame.time.get_ticks()
        if power_up_type == 'speed' and current_time - power_up_timer < 5000:
            player_speed = 4
        elif power_up_type == 'shield' and current_time - power_up_timer < 5000:
            # Implement shield effect
            pass
        elif power_up_type == 'power' and current_time - power_up_timer < 5000:
            # Implement power shot effect
            pass
        else:
            power_up_active = False
            player_speed = 2

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
        
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render('Welcome to Pixel Tank Battle!', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(text, text_rect)
        
        instructions = font.render('Use arrow keys to move, space to fire.', True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(instructions, instructions_rect)
        
        start_msg = font.render('Press Enter to start', True, WHITE)
        start_msg_rect = start_msg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(start_msg, start_msg_rect)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    global player_position, player_angle, player_turret_angle, game_over, score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle = rotate_tank(player_angle, player_rotation_speed, -1)
        if keys[pygame.K_RIGHT]:
            player_angle = rotate_tank(player_angle, player_rotation_speed, 1)
        if keys[pygame.K_UP]:
            player_position = move_tank(player_position, player_angle, player_speed)
        if keys[pygame.K_DOWN]:
            player_position = move_tank(player_position, player_angle, -player_speed)
        if keys[pygame.K_a]:
            player_turret_angle -= 5
        if keys[pygame.K_d]:
            player_turret_angle += 5
        if keys[pygame.K_SPACE]:
            fire_projectile(player_position, player_turret_angle)
        
        screen.fill(BLACK)
        draw_maze()
        draw_power_ups()
        draw_tank(player_position, player_angle, player_turret_angle, GREEN)
        draw_enemies()
        move_projectiles()
        draw_projectiles()
        check_collisions()
        apply_power_up()
        
        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over', True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    quit()

# Main execution
if __name__ == '__main__':
    game_intro()
    generate_maze()
    spawn_enemies()
    game_loop()