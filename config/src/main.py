import pm_gpt
import dev_gpt
import qa_gpt

def main():
    print("Welcome to Dev GPTeam!")
    initial_requirement = input("Please enter your initial software requirement: ")
    
    refined_requirement = pm_gpt.refine_requirements(initial_requirement)

    # tmp_requirement="""
    # Generate code for this requirement: create a brick Breaker game.

    # Requirement:
    # Brick Layout: The game must initialize with bricks arranged in a specific pattern (rows and columns) on the screen.
    # Paddle Control: Players should be able to control the horizontal movement of a paddle using keyboard, mouse, or touch inputs.
    # Ball Mechanics: A ball must bounce off walls, the paddle, and bricks, following proper physics for reflection angles.
    # Brick Collision: When the ball collides with a brick, the brick should disappear, and the player's score should increase.
    # Lives: The game should start with a predetermined number of lives. A life is lost when the ball passes the paddle and hits the bottom.
    # Scoring System: The game must have a scoring system where points are awarded for breaking bricks.
    # Game Over Condition: The game should end when either all bricks are broken (win) or the player loses all lives (lose).
    # User Interface: The game should display the current score, number of lives, and any relevant instructions or buttons (e.g., start, restart).
    # """

    # print(refined_requirement)
#     refined_requirement = """Classic Endless Brick Breaker Game
# ```
# # Requirements for the Classic Endless Brick Breaker Game

# 1. Implement an endless level design where new bricks are generated after the current set is cleared.
# 2. Start the game with a single layer of bricks and a paddle at the bottom of the screen.
# 3. Launch the ball from the center of the paddle after a short countdown or upon player action.
# 4. Award points for each brick broken, with a continuous score accumulation and high score tracking.
# 5. Provide the player with three lives, losing one each time the ball misses the paddle and hits the bottom.
# 6. End the game when all lives are lost.
# 7. Allow the player to control the paddle using mouse movement or keyboard arrow keys.
# 8. Ensure the ball bounces off the paddle, walls, and bricks, destroying bricks upon impact.
# 9. Incrementally increase difficulty by speeding up the ball or changing the brick layout as the game progresses.
# 10. Exclude power-ups, bonuses, and additional features to maintain a classic gameplay experience.
# ```"""
    generated_code = dev_gpt.generate_code(refined_requirement)
    #qa_gpt.validate_code(generated_code)

    print("Code generation completed!!!")

if __name__ == "__main__":
    main()
