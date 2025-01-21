import sys
import random
import os
import pygame

# Initialize pygame
pygame.init()

# For macOS, we need to handle the Python environment
if sys.platform == "darwin":  # This checks if we're on macOS
    os.environ['SDL_VIDEODRIVER'] = 'cocoa'

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floating Plank Survival")

# Path to background image
background_image_path = r"bg.jpg"

# Check if the background image exists
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
else:
    print("Background image not found, using a solid color instead.")
    background_image = pygame.Surface((WIDTH, HEIGHT))
    background_image.fill((0, 0, 255))  # Use blue as a fallback background
    
# Block properties (player)
block_width = 50
block_height = 50
x = WIDTH // 2 - block_width // 2  # Starting X (centered)
y = HEIGHT - block_height  # Initial Y position
velocity_y = 0  # Initial vertical velocity
gravity = 0.5
jump_strength = -15

# Water level properties
water_level = HEIGHT - 200  # Lower water level for a fair start
water_rise_speed = 0.05
water_rise_increase = 0.0005

# Adjust player's starting position
y = water_level - block_height - 150  # Start 150 pixels above the water level

# Plank properties
plank_width = 100
plank_height = 20
plank_speed = 2

# Game settings
is_jumping = False
score = 0
planks = []

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for frame rate
clock = pygame.time.Clock()

# Function to add a new plank
def add_plank():
    x_pos = random.randint(0, WIDTH - plank_width)
    y_pos = random.randint(int(water_level) - 150, int(water_level) - 50)
    plank_type = random.choice(['stable', 'unstable'])
    planks.append({'x': x_pos, 'y': y_pos, 'type': plank_type, 'time_on': 0})
    
# Update planks
def update_planks():
    for plank in planks[:]:
        plank['y'] += plank_speed
        if plank['y'] > HEIGHT:
            planks.remove(plank)
            
def start_screen():
    clock = pygame.time.Clock()
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 60)
    title_text = font.render("Floating Plank Survival", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title_text, (WIDTH // 4, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                
# Main game loop
def game_loop():
    global x, y, velocity_y, is_jumping, water_level, water_rise_speed, score
    running = True
    while running:
        screen.fill(BLUE)  # Fill the screen with blue before adding background
        
        # Draw the background image
        screen.blit(background_image, (0, 0))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            velocity_y = jump_strength
            is_jumping = True
            
        # Apply gravity
        velocity_y += gravity
        y += velocity_y
        
        # Prevent the player from falling through the ground
        if y > HEIGHT - block_height:
            y = HEIGHT - block_height
            is_jumping = False
            
        # Check collisions with planks
        on_plank = False
        for plank in planks:
            if (
                y + block_height <= plank['y'] + plank_height
                and y + block_height >= plank['y']
                and x + block_width > plank['x']
                and x < plank['x'] + plank_width
            ):
                if velocity_y > 0:  # Only land if falling
                    on_plank = True
                    y = plank['y'] - block_height
                    velocity_y = 0
                    is_jumping = False
                    if plank['type'] == 'unstable':
                        plank['time_on'] += 1
                        if plank['time_on'] > 60:  # Break unstable planks
                            planks.remove(plank)
                            
        if not on_plank and y + block_height < HEIGHT:
            is_jumping = True  # Player is falling if not on a plank or the ground
            
        # Check for game over
        if y + block_height >= int(water_level):
            running = False  # Player fell into the water
            
        # Move water level
        water_level -= water_rise_speed
        water_rise_speed += water_rise_increase
        
        # Add new planks
        if random.random() < 0.03:
            add_plank()
            
        # Draw planks
        for plank in planks:
            color = BROWN if plank['type'] == 'unstable' else GREEN
            pygame.draw.rect(screen, color, (int(plank['x']), int(plank['y']), plank_width, plank_height))
            
        # Draw player
        pygame.draw.rect(screen, RED, (int(x), int(y), block_width, block_height))
        
        # Display score
        score += 1
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score // 60}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Update screen
        pygame.display.flip()
        clock.tick(60)
        
    # Game over screen
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Your score: {score // 60}", True, RED)
    screen.fill(BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    try:
        print("Starting game...")
        start_screen()
        print("Start screen completed")
        game_loop()
        print("Game loop completed")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()