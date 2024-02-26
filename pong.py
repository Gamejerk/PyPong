import pygame
import sys
import AI_Opponent as ai

# Initialize Pygame
pygame.init()

# Sound effects
paddle_hit_sound = pygame.mixer.Sound('paddle_hit.wav')
wall_hit_sound = pygame.mixer.Sound('wall_hit.wav')
score_sound = pygame.mixer.Sound('score.wav')

# Font settings
menu_font = pygame.font.Font(None, 74)  # Use Pygame's default font for menu

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0) #Black
PADDLE_COLOR_PLAYER_1 = (0, 0, 255)  # Blue
PADDLE_COLOR_PLAYER_2 = (255, 0, 0)  # Red
BALL_COLOR = (255, 100, 100)

# Initialize scores
score_player_1 = 0
score_player_2 = 0

# Setup font for displaying scores
score_font = pygame.font.Font(None, 74)  # Use Pygame's default font

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PONG')

# Load the icon image
icon = pygame.image.load('icon.png')  # Make sure 'icon.png' is in your project directory
pygame.display.set_icon(icon)
tennis_ball_image = pygame.image.load('tennis_ball.png').convert_alpha()  # Load and convert the image with transparency

title_background_image = pygame.image.load('title_screen.png').convert()
title_background_image = pygame.transform.scale(title_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# Load paddle images
paddle1_image = pygame.image.load('paddle1.png').convert_alpha()
paddle1_image = pygame.transform.scale(paddle1_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

paddle2_image = pygame.image.load('paddle2.png').convert_alpha()
paddle2_image = pygame.transform.scale(paddle2_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball settings
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Paddle positions
paddle1_pos = [50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle2_pos = [SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]

# Ball position
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_vel = [BALL_SPEED_X, BALL_SPEED_Y]

# Create an instance of PongAI for player 2 (AI)
pong_ai = ai.PongAI(paddle2_pos, ball_pos, PADDLE_HEIGHT, PADDLE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, difficulty=1.0)

# Function to display the title screen and handle mode selection
def title_screen():
    pygame.mixer.music.load('title_screen_bgm.mp3')  # Replace 'title_screen_music.mp3' with your file
    pygame.mixer.music.play(-1)  # Play music indefinitely
    
    title_running = True
    selected_mode = 1  # 1 for '1 Player', 2 for '2 Players'
    while title_running:
        screen.blit(title_background_image, (0, 0))  # Draw the background image

        # Render text
        one_player_text = menu_font.render("1 Player", True, (255, 255, 255))
        two_player_text = menu_font.render("2 Players", True, (255, 255, 255))
        
        # Calculate positions for the text
        one_player_text_pos = (SCREEN_WIDTH // 2 - one_player_text.get_width() // 2, 250)
        two_player_text_pos = (SCREEN_WIDTH // 2 - two_player_text.get_width() // 2+12, 310)
        
        # Display the options
        screen.blit(one_player_text, one_player_text_pos)
        screen.blit(two_player_text, two_player_text_pos)

        # Calculate and draw the tennis ball as an indicator
        indicator_offset = -25  # Offset to the left of the selected item
        if selected_mode == 1:
            indicator_pos = (one_player_text_pos[0] + indicator_offset, one_player_text_pos[1]+12)
        else:
            indicator_pos = (two_player_text_pos[0] + indicator_offset, two_player_text_pos[1]+12)
        
        # Drawing the tennis ball image as an indicator
        screen.blit(tennis_ball_image, indicator_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_mode = 2
                elif event.key == pygame.K_UP:
                    selected_mode = 1
                elif event.key == pygame.K_RETURN:
                    title_running = False
                    pygame.mixer.music.stop()  # Stop the title screen music
                    return selected_mode
            
                
                
                     
# Call title screen and get selected mode
mode = title_screen()

# Load and play background music
pygame.mixer.music.load('bgm.mp3')  # Make sure 'background_music.mp3' is in your project directory
pygame.mixer.music.play(-1)  # Play music indefinitely

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move paddle 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_pos[1] > 0:
        paddle1_pos[1] -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1_pos[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle1_pos[1] += PADDLE_SPEED

    # Move paddle 2 based on mode
    if mode == 1:  # AI Control for single-player mode
        pong_ai.update()
    elif mode == 2:  # Player Control for two-player mode
        if keys[pygame.K_UP] and paddle2_pos[1] > 0:
            paddle2_pos[1] -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle2_pos[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle2_pos[1] += PADDLE_SPEED


    # Move ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Collision with top and bottom
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= SCREEN_HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        wall_hit_sound.play()

    # Collision with paddles
    if ball_pos[0] <= (paddle1_pos[0] + PADDLE_WIDTH + BALL_RADIUS) and paddle1_pos[1] < ball_pos[1] < paddle1_pos[1] + PADDLE_HEIGHT:
        ball_vel[0] = -ball_vel[0]
        paddle_hit_sound.play()
    if ball_pos[0] >= (paddle2_pos[0] - BALL_RADIUS) and paddle2_pos[1] < ball_pos[1] < paddle2_pos[1] + PADDLE_HEIGHT:
        ball_vel[0] = -ball_vel[0]
        paddle_hit_sound.play()


    # Reset ball and update score if it goes off screen
    if ball_pos[0] < 0:
        score_player_2 += 1  # Increment score for Player 2
        ball_pos[0] = SCREEN_WIDTH // 2
        ball_pos[1] = SCREEN_HEIGHT // 2
        ball_vel[0] = BALL_SPEED_X
        ball_vel[1] = BALL_SPEED_Y
        score_sound.play()

    elif ball_pos[0] > SCREEN_WIDTH:
        score_player_1 += 1  # Increment score for Player 1
        ball_pos[0] = SCREEN_WIDTH // 2
        ball_pos[1] = SCREEN_HEIGHT // 2
        ball_vel[0] = -BALL_SPEED_X
        ball_vel[1] = BALL_SPEED_Y
        score_sound.play()

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    # Draw paddle 1 using its scaled image
    screen.blit(paddle1_image, paddle1_pos)
    # Draw paddle 2 using its scaled image
    screen.blit(paddle2_image, paddle2_pos)
   
    #pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_RADIUS)
    # Calculate the top-left corner of the tennis ball image for blitting
    tennis_ball_rect = tennis_ball_image.get_rect(center=(ball_pos[0], ball_pos[1]))

    # Drawing the tennis ball image instead of a circle
    screen.blit(tennis_ball_image, tennis_ball_rect)

    # Display scores
    score_text_player_1 = score_font.render(str(score_player_1), True, (255, 255, 255))  # White color
    score_text_player_2 = score_font.render(str(score_player_2), True, (255, 255, 255))  # White color
    screen.blit(score_text_player_1, (80, 300))  # Position for Player 1's score
    screen.blit(score_text_player_2, (SCREEN_WIDTH - 100, 300))  # Position for Player 2's score

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
