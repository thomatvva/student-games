import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Stickman Jump")

# Colors
LIGHT_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
DARK_BLUE = (0, 0, 205)
BLACK = (0, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Game variables
stickman = pygame.Rect(WIDTH // 2, HEIGHT - 60, 20, 40)
stickman_dx = 0
stickman_dy = 0
grounded = False
double_jump_used = False
can_jump = True
camera_y = 0
water_level = HEIGHT
score = 0
rocks = [pygame.Rect(380, 550, 100, 20), 
         pygame.Rect(300, 450, 120, 20), 
         pygame.Rect(500, 350, 100, 20)]

# Fonts
font = pygame.font.Font(None, 36)

def reset_game():
    global stickman, stickman_dx, stickman_dy, grounded, double_jump_used
    global can_jump, camera_y, water_level, score, rocks
    
    stickman = pygame.Rect(WIDTH // 2, HEIGHT - 60, 20, 40)
    stickman_dx = 0
    stickman_dy = 0
    grounded = False
    double_jump_used = False
    can_jump = True
    camera_y = 0
    water_level = HEIGHT
    score = 0
    rocks = [pygame.Rect(380, 550, 100, 20),
             pygame.Rect(300, 450, 120, 20),
             pygame.Rect(500, 350, 100, 20)]

def draw_background():
    screen.fill(LIGHT_BLUE)

def draw_water():
    water_y = water_level - camera_y
    pygame.draw.rect(screen, BLUE, (0, water_y, WIDTH, HEIGHT - water_y))
    pygame.draw.rect(screen, DARK_BLUE, (0, water_y + 20, WIDTH, 10))

def draw_rock(rock):
    adjusted_rock = pygame.Rect(rock.x, rock.y - camera_y, rock.width, rock.height)
    pygame.draw.rect(screen, BROWN, adjusted_rock)
    pygame.draw.rect(screen, GREEN, (adjusted_rock.x, adjusted_rock.y, adjusted_rock.width, adjusted_rock.height // 4))

def draw_stickman():
    adjusted_stickman = pygame.Rect(stickman.x, stickman.y - camera_y, stickman.width, stickman.height)
    pygame.draw.rect(screen, BLACK, adjusted_stickman)

def handle_jump(jump_pressed):
    global stickman_dy, double_jump_used, can_jump, grounded
    
    if jump_pressed:  # Removed the can_jump check to make it more responsive
        if grounded:
            stickman_dy = -12
            grounded = False  # Set grounded to False immediately
        elif not double_jump_used and stickman_dy > -6:  # Allow double jump when falling or near peak of first jump
            stickman_dy = -12
            double_jump_used = True

def update_stickman():
    global stickman_dx, stickman_dy, grounded, double_jump_used, camera_y

    stickman_dy += 0.5  # Gravity
    stickman.x += stickman_dx
    stickman.y += stickman_dy

    # Screen boundaries
    if stickman.x < 0:
        stickman.x = 0
    if stickman.x + stickman.width > WIDTH:
        stickman.x = WIDTH - stickman.width

    # Platform collision
    grounded = False
    for rock in rocks:
        if stickman.colliderect(rock) and stickman_dy >= 0:
            grounded = True
            double_jump_used = False
            stickman_dy = 0
            stickman.y = rock.y - stickman.height

    # Camera follow
    target_camera_y = stickman.y - HEIGHT // 2
    camera_y += (target_camera_y - camera_y) * 0.1

    # Horizontal movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        stickman_dx = -5
    elif keys[pygame.K_RIGHT]:
        stickman_dx = 5
    else:
        stickman_dx = 0

    # Handle jumping
    handle_jump(keys[pygame.K_UP])

def update_water():
    global water_level
    water_level = camera_y + HEIGHT + 100
    if stickman.y + stickman.height > water_level:
        return True
    return False

def add_new_rock():
    global rocks
    if not rocks:  # If rocks list is empty, add initial rocks
        rocks = [pygame.Rect(380, 550, 100, 20),
                pygame.Rect(300, 450, 120, 20),
                pygame.Rect(500, 350, 100, 20)]
        return
        
    last_rock = rocks[-1]
    new_x = random.randint(50, WIDTH - 150)
    new_y = last_rock.y - random.randint(100, 120)  # Distance between platforms
    rocks.append(pygame.Rect(new_x, new_y, random.randint(80, 120), 20))

def check_and_generate_rocks():
    global rocks
    # Get the highest rock (the one with smallest y value)
    if rocks:
        highest_rock_y = min(rock.y for rock in rocks)
        # If highest rock is within camera view, generate more rocks
        if highest_rock_y > camera_y - HEIGHT:
            add_new_rock()
    else:
        add_new_rock()

def clean_old_rocks():
    global rocks
    # Keep rocks that are not too far below the camera
    rocks = [rock for rock in rocks if rock.y > camera_y - HEIGHT * 2 and rock.y < camera_y + HEIGHT * 2]

def update_score():
    global score
    score = max(score, int(abs(camera_y) // 10))

def game_over():
    waiting = True
    while waiting:
        screen.fill(LIGHT_BLUE)
        game_over_text = font.render("Game Over! Press R to Restart or Q to Quit", True, BLACK)
        score_text = font.render(f"Your score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return True
                if event.key == pygame.K_q:
                    return False
        
        clock.tick(FPS)

def game_loop():
    global rocks
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_background()
        draw_water()
        for rock in rocks:
            draw_rock(rock)
        draw_stickman()

        update_stickman()
        if update_water():  # Game over if True
            if not game_over():
                running = False
                
        clean_old_rocks()
        check_and_generate_rocks()  # New function to check and generate rocks

        update_score()

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    game_loop()