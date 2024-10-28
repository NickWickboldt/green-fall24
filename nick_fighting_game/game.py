import pygame

# Initialize pygame
pygame.init()

# Set up display
window_width, window_height = 1000, 700
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Move the Square")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

bullets = [] #array

# Define the player's starting position and size
player_size = 50
player_x, player_y = window_width // 2, window_height // 2
player_speed = 7

# Set up the game clock
clock = pygame.time.Clock()



# Main game loop
running = True
while running:
    left = False
    right = False
    up = False
    down = False
    holding_gun = False
    shoot_bullet = False
    # Limit the frame rate to 60 FPS
    clock.tick(60)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current state of all keys
    keys = pygame.key.get_pressed()

    # Update player position based on WASD keys
    if keys[pygame.K_w]:  # Move up
        player_y -= player_speed
    if keys[pygame.K_s]:  # Move down
        player_y += player_speed
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed

    if keys[pygame.K_UP]:
        up = True
    if keys[pygame.K_DOWN]:
        down = True
    if keys[pygame.K_LEFT]:
        left = True
    if keys[pygame.K_RIGHT]:
        right = True

    if keys[pygame.K_SPACE]:
        holding_gun = True
    
    if keys[pygame.K_RCTRL]:
        shoot_bullet = True

    # Prevent the player from going off the screen
    player_x = max(0, min(window_width - player_size, player_x))
    player_y = max(0, min(window_height - player_size, player_y))

    # Fill the window with a blank grid (white background)
    win.fill(WHITE)

    if holding_gun:
        pygame.draw.rect(win, (0,0,255), (player_x + 20, player_y - 30, 10, 30))
        if shoot_bullet:
            pygame.draw.circle(win, (0,0,0), (player_x + 20, player_y - 30), 10)
            bullets.append((player_x + 20, player_y - 30)) # (x,y) ~ tuple

    for bullet in bullets:
        pygame.draw.circle(win, (0,0,0), (bullet[0], bullet[1]), 10)
    

    # Draw the player (a black square)
    pygame.draw.rect(win, BLACK, (player_x, player_y, player_size, player_size))

    if left:
        pygame.draw.rect(win, (255, 0, 0), (player_x - 10, player_y - 10, 10, 70))
    elif right:
        pygame.draw.rect(win, (255, 0, 0), (player_x + 50, player_y - 10, 10, 70))
    elif up:
        pygame.draw.rect(win, (255, 0, 0), (player_x - 10, player_y - 10, 70, 10))
    elif down:
        pygame.draw.rect(win, (255, 0, 0), (player_x - 10, player_y + 50, 70, 10))
    else:
        pygame.draw.rect(win, (255, 0, 0), (player_x + 10, player_y + 10, 30, 30))


    # Update the display
    pygame.display.flip()

# Quit pygame when the loop ends
pygame.quit()
