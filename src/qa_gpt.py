import json
import os
import utilities

QA_GPT_SYSTEM_CONTEXT2="""Your role is a professional quality assurance engineer for Python and Pygame mini-games. You will be provided with a list of requirements and some codes. you need to review the code for gameplay functionality, correct display and graphics, and then generate the complete final code in this structured format:
 <FILE_START>
GENERATED_FILE_NAME
```python
# your code here
```
<FILE_END>.
"""

QA_GPT_SYSTEM_CONTEXT="""NOTICE
Role: You are a professional quality assurance engineer; the main goal is to write PEP8 compliant, elegant, modular, easy to read and maintain Python 3.9 code. Output format strictly follow "Format example".

Write code with triple quoto, based on the following list and context.

1. You may output more than one file, but please use '<FILE_START>' and '<FILE_END>' tags to seperete them.
2. You code must be able to be run on end-to-end
3. Replace 'GENERATED_FILE_NAME' with file name you propose.
4. Please assume user will run the program by running  'python -m unittest -v test_xxxxx.py'
5. The total number line of code generated should be less than 500
6. Attention1: ALWAYS SET A DEFAULT VALUE, ALWAYS USE EXPLICIT VARIABLE.
7. IMPORTANT: Please implement complete code snippets.

Format Example:
-----
<FILE_START>
GENERATED_FILE_NAME
```python
# your code here
```
<FILE_END>
<FILE_START>
GENERATED_FILE_NAME
```python
# your code here
```
<FILE_END>
-----"""

input="""Generate code for this requirement: create a brick Breaker game.

    Requirement:
    Brick Layout: The game must initialize with bricks arranged in a specific pattern (rows and columns) on the screen.
    Paddle Control: Players should be able to control the horizontal movement of a paddle using keyboard, mouse, or touch inputs.
    Ball Mechanics: A ball must bounce off walls, the paddle, and bricks, following proper physics for reflection angles.
    Brick Collision: When the ball collides with a brick, the brick should disappear, and the player's score should increase.
    Lives: The game should start with a predetermined number of lives. A life is lost when the ball passes the paddle and hits the bottom.
    Scoring System: The game must have a scoring system where points are awarded for breaking bricks.
    Game Over Condition: The game should end when either all bricks are broken (win) or the player loses all lives (lose).
    User Interface: The game should display the current score, number of lives, and any relevant instructions or buttons (e.g., start, restart).
    

Additional requirement:
1. IMPORTANT: Put your generated project folder name between '<PROJECT_NAME_START>' and '<PROJECT_NAME_END>' tags.
2. Output format strictly follow "Format example" in your context or instruction.

<PROJECT_NAME_START>brick_breaker_game<PROJECT_NAME_END>
<FILE_START>
main.py
```python
import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

# initialize pygame
pygame.init()

# set up the game window
window_width = 800
window_height = 600
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Brick Breaker")

# colors
black = (0, 0, 0)
white = (255, 255, 255)

# game variables
score = 0
lives = 3
game_over = False

# create objects
paddle = Paddle(window_width, window_height)
ball = Ball(window_width, window_height)
bricks = pygame.sprite.Group()
brick_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
for row in range(len(brick_layout)):
    for col in range(len(brick_layout[row])):
        if brick_layout[row][col] == 1:
            brick = Brick(100 + col * 90, 50 + row * 40)
            bricks.add(brick)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # move the paddle
        keys = pygame.key.get_pressed()
        paddle.move(keys)

        # move the ball
        ball.move()

        # check for ball collision with paddle
        if pygame.sprite.collide_rect(ball, paddle):
            ball.bounce()

        # check for ball collision with bricks
        brick_collision_list = pygame.sprite.spritecollide(ball, bricks, True)
        if brick_collision_list:
            score += len(brick_collision_list)
            ball.bounce()

        # check for ball passing the paddle
        if ball.rect.top > window_height:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                ball.reset()

        # check for win condition
        if len(bricks) == 0:
            game_over = True

    # draw everything
    game_window.fill(black)
    paddle.draw(game_window)
    ball.draw(game_window)
    bricks.draw(game_window)

    # display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    game_window.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, white)
    game_window.blit(lives_text, (window_width - 100, 10))

    if game_over:
        if len(bricks) == 0:
            game_over_text = font.render("You Win!", True, white)
        else:
            game_over_text = font.render("Game Over", True, white)
        game_window.blit(game_over_text, (window_width // 2 - 100, window_height // 2))

    pygame.display.update()

pygame.quit()
```
<FILE_END>
<FILE_START>
paddle.py
```python
import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_height - 30)
        self.window_width = window_width

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < self.window_width:
            self.rect.x += 5

    def draw(self, game_window):
        game_window.blit(self.image, self.rect)
```
<FILE_END>
<FILE_START>
ball.py
```python
import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_height // 2)
        self.window_width = window_width
        self.window_height = window_height
        self.speed_x = 3
        self.speed_y = 3

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= self.window_width:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def bounce(self):
        self.speed_y = -self.speed_y

    def reset(self):
        self.rect.center = (self.window_width // 2, self.window_height // 2)
        self.speed_x = 3
        self.speed_y = 3

    def draw(self, game_window):
        game_window.blit(self.image, self.rect)
```
<FILE_END>
<FILE_START>
brick.py
```python
import pygame

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
```
<FILE_END>
Code generation completed!!!

above are the requirement and source code, try you best to generate some unit test case file for each file
"""


import os

def parse_code(code_string):
    # Get the directory of the main.py file
    main_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Extract project name between the new tags
    project_start_tag = "<PROJECT_NAME_START>"
    project_end_tag = "<PROJECT_NAME_END>"
    project_name_start = code_string.find(project_start_tag) + len(project_start_tag)
    project_name_end = code_string.find(project_end_tag)
    project_name = code_string[project_name_start:project_name_end].strip()

    # Define the workspace path relative to the main.py file
    project_workspace_path = os.path.join(main_file_dir, f'../workspace/{project_name}')

    # Ensure the project workspace directory exists
    os.makedirs(project_workspace_path, exist_ok=True)

    # Split the string by the file start delimiter
    file_sections = code_string.split("<FILE_START>")

    for file_section in file_sections[1:]:  # Skip the first split as it's before the first FILE_START
        # Further split by the file end delimiter
        parts = file_section.split("<FILE_END>")
        file_content = parts[0].strip()  # The file content (filename + code)

        # Split each file content into filename and code
        filename_and_code = file_content.split("```python\n", 1)
        filename = filename_and_code[0].strip()
        code = filename_and_code[1].strip("```\n").strip()

        # Write the code to a file in the project workspace directory
        file_path = os.path.join(project_workspace_path, filename)
        with open(file_path, 'w') as file:
            file.write(code)


# src/qa_gpt.py
def validate_code(generated_code):
    # In a real application, here you'd validate code using a GPT model.
    print("Validating code...\n")

    response = utilities.call_openai_api_DEV(QA_GPT_SYSTEM_CONTEXT, input, 0.1, 0.1)
    code_string = response.choices[0].message.content
    
    print(response.choices[0].message.content)
    parse_code(code_string)


    print("No issues found in the generated code.\n")

def code_review(requirement, generated_code):
    print("Reveiwing code...\n")
    req_and_code = "Requirement:\n" + requirement + "Code to review:\n" + generated_code
    messages = [
        {"role": "system", "content": QA_GPT_SYSTEM_CONTEXT2},
        {"role": "user", "content": req_and_code}
    ]
    response = utilities.call_openai_api_QA(messages, model="gpt-4-1106-preview")
    return response

if __name__ == "__main__":
    test_req = """# Flappy Bird-style arcade game for desktop
```
1. Implement bird character with gravity-affected flight mechanics.
2. Create a continuous scroll of green pipe obstacles with variable heights and gaps.
3. Increment score by one each time the bird successfully passes through a set of pipes.
4. Use spacebar key press to control the bird's flapping and ascending motion.
5. Detect collisions between the bird and pipes or ground to trigger game over.
6. Start the game upon the first spacebar press after the game is launched.
7. Display the current score during gameplay and final score upon game over.
8. Allow the player to restart the game by pressing the spacebar after a game over screen is displayed.
```"""
    test_code = """import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_FLAP_POWER = 5
PIPE_SPEED = -3
PIPE_WIDTH = 70
PIPE_HEIGHT_DIFF = 150
PIPE_GAP = 200
BIRD_START_X = 50
BIRD_START_Y = 300

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(BIRD_START_X, BIRD_START_Y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = -BIRD_FLAP_POWER

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, y_change):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        if position == 'top':
            self.rect.bottomleft = (SCREEN_WIDTH, y_change - PIPE_GAP // 2)
        else:
            self.rect.topleft = (SCREEN_WIDTH, y_change + PIPE_GAP // 2)

    def update(self):
        self.rect.x += PIPE_SPEED

# Game class
class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.score = 0
        self.game_active = False

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not self.game_active:
                        self.game_active = True
                        self.pipes.empty()
                        self.bird.rect.center = (BIRD_START_X, BIRD_START_Y)
                        self.bird.velocity = 0
                        self.score = 0
                    self.bird.flap()

            if self.game_active:
                self.all_sprites.update()
                self.manage_pipes()
                self.check_collisions()
                self.update_score()

            self.draw()

            clock.tick(60)

    def manage_pipes(self):
        for pipe in self.pipes:
            if pipe.rect.right < 0:
                self.pipes.remove(pipe)
        if not self.pipes or self.pipes.sprites()[-1].rect.centerx < SCREEN_WIDTH // 2:
            y_change = random.randint(PIPE_HEIGHT_DIFF, SCREEN_HEIGHT - PIPE_HEIGHT_DIFF)
            top_pipe = Pipe('top', y_change)
            bottom_pipe = Pipe('bottom', y_change)
            self.pipes.add(top_pipe, bottom_pipe)
            self.all_sprites.add(top_pipe, bottom_pipe)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or \
           self.bird.rect.top <= 0 or \
           self.bird.rect.bottom >= SCREEN_HEIGHT:

    def update_score(self):
        for pipe in self.pipes:
            if pipe.rect.centerx < self.bird.rect.left and not pipe.passed:
                pipe.passed = True
                self.score += 1

    def draw(self):
        screen.fill((135, 206, 235))  # Light blue color for the sky
        self.all_sprites.draw(screen)
        self.draw_score()

    def draw_score(self):
            score_surface = pygame.font.Font(None, 36).render(str(self.score), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        else:
            game_over_surface = pygame.font.Font(None, 48).render(f'Game Over! Score: {self.score}', True, (255, 255, 255))
            screen.blit(game_over_surface, game_over_rect)

    game = Game()
    game.run()
"""
    response = code_review(test_req, test_code)
    print(response)