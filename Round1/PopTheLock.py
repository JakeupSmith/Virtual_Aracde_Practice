import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop the Lock")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
outer_radius = 300
inner_radius = 200
line_length = outer_radius - inner_radius
angle = 0
speed = 1
target_angle = random.randint(0, 360)
score = 50
running = True
clockwise = True

# Previous target position
previous_target_angle = target_angle

def draw_lock():
    pygame.draw.circle(screen, PURPLE, (WIDTH // 2, HEIGHT // 2), outer_radius, 10)
    pygame.draw.circle(screen, PURPLE, (WIDTH // 2, HEIGHT // 2), inner_radius, 10)
    for i in range(40):
        theta = i * 9
        x = WIDTH // 2 + math.cos(math.radians(theta)) * outer_radius
        y = HEIGHT // 2 + math.sin(math.radians(theta)) * outer_radius
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 10)

def draw_center():
    pygame.draw.circle(screen, GREEN, (WIDTH // 2, HEIGHT // 2), 200)
    
    # Render the score in the center
    font_score = pygame.font.Font(None, 300)
    text_score = font_score.render(str(score), True, WHITE)
    y_offset = -20
    screen.blit(text_score, (WIDTH // 2 - text_score.get_width() // 2, HEIGHT // 2 - text_score.get_height() // 2 + y_offset))
    
    # Render the "TO GO!" text below the score
    font_text = pygame.font.Font(None, 60)
    text = font_text.render("TO GO!", True, WHITE)
    y_offset2 = 175
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text_score.get_height() // 2 + y_offset2))

def draw_target():
    target_x = WIDTH // 2 + math.cos(math.radians(target_angle)) * ((inner_radius + outer_radius) // 2)
    target_y = HEIGHT // 2 + math.sin(math.radians(target_angle)) * ((inner_radius + outer_radius) // 2)
    pygame.draw.circle(screen, YELLOW, (int(target_x), int(target_y)), 25)
    pygame.draw.circle(screen, RED, (int(target_x), int(target_y)), 25, 3)

def display_win_message():
    font_win = pygame.font.Font(None, 100)
    text_win = font_win.render("YOU WIN!", True, GREEN)
    screen.blit(text_win, (WIDTH // 2 - text_win.get_width() // 2, HEIGHT // 2 - text_win.get_height() // 2))

def generate_new_target():
    global target_angle
    while True:
        new_target_angle = random.randint(0, 360)
        if abs(new_target_angle - previous_target_angle) >= 5:
            target_angle = new_target_angle
            break

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and score > 0:
                if abs(angle - target_angle) < 10:
                    score -= 1
                    speed += 0.2
                    previous_target_angle = target_angle
                    generate_new_target()
                    clockwise = not clockwise  # Change direction
                else:
                    running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw lock and center
    draw_lock()
    draw_center()

    if score == 0:
        display_win_message()
    else:
        # Update angle
        if clockwise:
            angle = (angle + speed) % 360
        else:
            angle = (angle - speed) % 360

        # Draw the rotating line
        inner_x = WIDTH // 2 + math.cos(math.radians(angle)) * inner_radius
        inner_y = HEIGHT // 2 + math.sin(math.radians(angle)) * inner_radius
        outer_x = WIDTH // 2 + math.cos(math.radians(angle)) * outer_radius
        outer_y = HEIGHT // 2 + math.sin(math.radians(angle)) * outer_radius
        pygame.draw.line(screen, RED, (inner_x, inner_y), (outer_x, outer_y), 10)

        # Draw the target
        draw_target()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
