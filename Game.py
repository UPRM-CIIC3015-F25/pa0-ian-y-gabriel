import pygame, sys, random

# Load images
Big_Boss = pygame.image.load("Big_Boss.png")
Big_Boss = pygame.transform.scale(Big_Boss, (100, 100))

how_wild = pygame.image.load("Wild_Hunt.png")
how_wild = pygame.transform.scale(how_wild, (400, 400))

mark = pygame.image.load("markiplier.png")
mark = pygame.transform.scale(mark, (200, 200))


def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, show_image, show_image2, show_image3, music

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # Completed task 5(Changed ball speed to 7)
    speed = 7
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # Completed task 2
            score += 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction

            # Increase speed by 10%
            ball_speed_x *= 1.1
            ball_speed_y *= 1.1

            #ball speed cap
            max_speed = 15
            ball_speed_x = max(-max_speed, min(ball_speed_x, max_speed))
            ball_speed_y = max(-max_speed, min(ball_speed_y, max_speed))

            if not is_muted:
                #Completed task 6
                pygame.init()
                pygame.mixer.init()
                sound_effect = pygame.mixer.Sound("hog-rider.wav")
                sound_effect.play()
                sound_effect.fadeout(2000)

            #if score = 10 show snake eater starts playing
            if score == 10:
                show_image = True
                pygame.init()
                pygame.mixer.init()
                sound_effect = pygame.mixer.Sound("snake-eater-outro.wav")
                sound_effect.play()

            # if score = 20 play "hello everybody my name is markiplier"
            if score == 20:
                show_image3 = True
                sound_effect = pygame.mixer.Sound(f"markiplier.wav")
                sound_effect.play()

            #when score = 30 play wild hunt laughing
            if score == 30:
                show_image2 = True
                pygame.init()
                pygame.mixer.init()
                sound_effect = pygame.mixer.Sound("wild_hunt_laugh_limbus.wav")
                sound_effect.play()
                sound_effect.fadeout(2000)





            # TODO Task 6: Add sound effects HERE
            #plays "hog rider" if ball hits paddle
            pygame.init()
            pygame.mixer.init()
            sound_effect = pygame.mixer.Sound(f"hog-rider.wav")
            sound_effect.play()
            sound_effect.fadeout(2000)


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart()  # Reset the game

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score
    pygame.init()
    pygame.mixer.init()
    sound_effect = pygame.mixer.Sound("bedman_announcer_mod_intro.wav")
    sound_effect.play()

def title_screen():
    """
    Displays the title screen with options to start the game or mute sound.
    """
    global game_state, is_muted

    while game_state == "title_screen":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if singleplayer_button.collidepoint(event.pos):
                    game_state = "playing"
                if mute_button.collidepoint(event.pos):
                    is_muted = not is_muted

        screen.fill(bg_color)

        # Title
        title_font = pygame.font.Font('freesansbold.ttf', 72)
        title_text = title_font.render("Pong", True, light_grey)
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(title_text, title_rect)

        # Name
        name_font = pygame.font.Font('freesansbold.ttf', 20)
        name_text = name_font.render("By: Gabriel & Ian", True, light_grey)
        name_rect = name_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
        screen.blit(name_text, name_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()

        # Singleplayer Button
        singleplayer_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 20, 200, 50)
        button_color = light_grey if singleplayer_button.collidepoint(mouse_pos) else 'gray'
        pygame.draw.rect(screen, button_color, singleplayer_button)
        button_text = basic_font.render("Singleplayer", True, bg_color)
        button_text_rect = button_text.get_rect(center=singleplayer_button.center)
        screen.blit(button_text, button_text_rect)

        # Mute Button
        mute_button_text_str = "Unmute" if is_muted else "Mute Sound"
        mute_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 90, 200, 50)
        mute_button_color = light_grey if mute_button.collidepoint(mouse_pos) else 'gray'
        pygame.draw.rect(screen, mute_button_color, mute_button)
        mute_button_text = basic_font.render(mute_button_text_str, True, bg_color)
        mute_button_text_rect = mute_button_text.get_rect(center=mute_button.center)
        screen.blit(mute_button_text, mute_button_text_rect)

        pygame.display.flip()
        clock.tick(60)

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Adding music
pygame.mixer.music.load('01. Through Patches of Violet.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('grey12')
light_grey = pygame.Color('grey83')
red = pygame.Color('red')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)

player_height = 15
player_width = 200 # task 1 done
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
game_state = "title_screen"
is_muted = False

# Score Text setup
score = 0
show_image = False
show_image2 = False
show_image3 = False
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score
start = False  # Indicates if the game has started

# Sound
sound_effect = pygame.mixer.Sound("hog-rider.wav")

# Main game loop
while True:
    if game_state == "title_screen":
        title_screen()

    elif game_state == "playing":
        # Event handling
        # Completed task 4
        name = "Gabriel & Ian"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed -= 6  # Move paddle left
                if event.key == pygame.K_RIGHT:
                    player_speed += 6  # Move paddle right
                if event.key == pygame.K_SPACE:
                    start = True  # Start the ball movement
                    show_image = False
                    show_image2 = False
                    show_image3 = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_speed += 6  # Stop moving left
                if event.key == pygame.K_RIGHT:
                    player_speed -= 6  # Stop moving right

        # Game Logic
        ball_movement()
        player_movement()



        # Visuals
        screen.fill(bg_color)  # Clear screen with background color
        pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
        # Completed task 3
        pygame.draw.ellipse(screen, red, ball)  # Draw ball
        player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
        screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

        #shows all the pngs (wild hunt, big boss, and markiplier)
        if show_image:
            screen.blit(Big_Boss, (screen_width // 2 - 50, screen_height // 2 - 50))

        if show_image3:
            mark_rect = mark.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(mark, mark_rect)

        if show_image2:
            how_wild_rect = how_wild.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(how_wild, how_wild_rect)


        # Update display
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second