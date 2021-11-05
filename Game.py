import pygame, glob, random, socket, sys

# Initialize everything imported (otherwise things such as the font does not work)
pygame.init()

# Initial Variables
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Side Scroller")

font = pygame.font.SysFont("comicsansms", 20)
bigfont = pygame.font.SysFont("comicsansms", 30)

high_score = 0

def jumpy():
    global jump
    jump = 1

# Menu Function
def menu():

    # Load the menu image and stretch it to the window size
    image = pygame.image.load("assets\menu.png")
    image = pygame.transform.scale(image, (640, 480))

    # While the game is running...
    while True:

        # Show the menu image
        screen.blit(image,(0,0))

        # Update display
        pygame.display.update()

        # Built-in function that keeps track of specific events unique to pygame
        for event in pygame.event.get():

            # Window close event
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

            # Mouse-down event (runs once per mouse-click)
            if event.type == pygame.MOUSEBUTTONDOWN:

                # If the mouse is within a specific range (0 = X, 1 = Y), start game
                if event.pos[0] in range(300, 325) and event.pos[1] in range(200,228):
                    print(f"PLAY!")

                    # Run the game
                    game()


# Game-screen function
## (Lots of necessary code is repeated from menu)
def game():
    # Load the menu image and stretch it to the window size
    image = pygame.image.load("assets\level1.png")
    image = pygame.transform.scale(image, (640, 480))

    # Keep track of the x-value of the background image
    bg_x = 0

    # Scroll speed
    scroll_speed = 1

    # Sprite variables
    sprite_counter = 0
    sprite_delay = 0
    sprite_delay_amount = 0

    # Load the player running sprites and jumping sprites
    run_sprites = [pygame.image.load(img) for img in glob.glob("assets\Run\\*.png")]
    jump_sprites = [pygame.image.load(img) for img in glob.glob("assets\Jump\\*.png")]
    player = run_sprites[sprite_counter]

    # Keep track of the player's y-value
    player_y = 325

    # Keeps track of if the player is currently jumping
    global jump
    jump = 0

    # Keeps track of incoming jump-commands from middleman
    middleman = 0

    # Keeps track of the player's jump, and when to return to the ground
    jump_count = 0
    jump_count_start = -15

    # Keeps track of the height of the jump
    jump_height = 8

    # Decreases the time of the jump
    jump_diff_add = 0.5

    intro_text = True

    # Gravity
    gravity = 4

    # Score
    global score
    global high_score
    score = 0

    # Difficulty increase
    difficulty_increase = 0

    # Load crate image
    crate = pygame.image.load("assets\crate.png")

    # Scale crate image
    crate = pygame.transform.rotozoom(crate,0,0.8)

    # Keeps track of the crate's x-value and speed
    ## (Note that it starts slightly outside the window)
    crate_x = 1500
    crate_speed = 5
    crate_speed_low = 5
    crate_speed_high = 7
    crate_spawn_low = 700
    crate_spawn_high = 800

    # While the game is running...
    while True:

        # Draw 3 instances of the background image (allows scrolling)
        ## One to the left of the screen, one to the right, and one in the middle
        ### 640 is the length of the game screen
        screen.blit(image, (bg_x - 640, 0))
        screen.blit(image, (bg_x, 0))
        screen.blit(image, (bg_x + 640, 0))

        # Move background 1 pixel
        bg_x -= scroll_speed

        # Reset the background when the background has moved the length of the screen
        if bg_x <= -640:
            bg_x = 0

        # Draw the player on top of the background in a fixed spot
        ## (The .blit command returns a rectangle around the player, which we use for collisions)

        # Update the player sprite
        if sprite_delay >= sprite_delay_amount:
            if sprite_counter == 7:
                if jump == 0:
                    sprite_counter = 0
            else:
                sprite_counter += 1
            sprite_delay = 0
        else:
            sprite_delay += 1

        # Draw the player, scale the player down, blit it on the screen
        if jump == 0:
            player = run_sprites[sprite_counter]
            sprite_delay_amount = 3
        if jump == 1:
            player = jump_sprites[sprite_counter]
            sprite_delay_amount = 5
        player = pygame.transform.rotozoom(player, 0, 0.2)
        player_rect = screen.blit(player, (50, player_y))
        pygame.draw.rect(screen, (255,0,0), (player_rect), 1)

        # If the player, for some reason, goes under the ground, put them back
        if player_y > 325:
            player_y = 325

        # If a jump is happening
        if jump == 1:
            player_y += jump_count
            jump_count += jump_diff_add

            # If the player, for some reason, goes under the ground, put them back
            if player_y >= 325:
                player_y = 325
                jump = 0
        else:
            jump_count = jump_count_start



        # Display crate
        crate_rect = screen.blit(crate,(crate_x,360))
        pygame.draw.rect(screen, (0, 0, 255), (crate_rect), 1)

        # Make the crate move
        crate_x -= crate_speed

        # Remove Introtext
        if crate_x == 600:
            intro_text = False

        # Regenerate the crate with randomized stats when it disappears
        if crate_x <= -75:

            # Increase difficulty based on current score
            if (score + 1) % 5 == 0 and score != 0:
                print("Speed Increase!")
                difficulty_increase = True

            if difficulty_increase:

            # As the game progresses, the crates move faster and spawn further apart
                scroll_speed += 1
                crate_speed_low += 1
                crate_speed_high += 1
                crate_spawn_low += 50
                crate_spawn_high += 150
                difficulty_increase = False

            score += 1
            if score > high_score:
                high_score = score
            crate_x = random.randint(crate_spawn_low,crate_spawn_high)
            crate_speed = random.randint(crate_speed_low,crate_speed_high)

        # Write "Speed Up!" on speed up
        if (score) % 5 == 0 and score != 0:
            speedtext = font.render("SPEED UP!", 1, (0, 0, 0))
            screen.blit(speedtext, (270, 150))

        if intro_text:
            introtext = bigfont.render("Press SPACE to jump!", 1, (0, 0, 0))
            screen.blit(introtext, (175, 150))

        # Return to menu on collision with crate
        if player_rect.colliderect(crate_rect):
            return


        # Show score in the corner of the screen
        scoretext = font.render("Score = " + str(score), 1, (0, 0, 0))
        screen.blit(scoretext, (5, 10))

        high_scoretext = font.render("High-Score = " + str(high_score), 1, (0, 0, 0))
        screen.blit(high_scoretext, (5, 40))


        # Update display
        pygame.display.update()

        # Built-in function that keeps track of specific events unique to pygame
        for event in pygame.event.get():

            # Window close event
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

            # Key-down event (runs once per key-press)
            if event.type == pygame.KEYDOWN:

                # Jump when SPACE is pressed
                if event.key == pygame.K_SPACE:

                    # Jump only happens when the player is on the ground
                    if player_y == 325:
                        print("jump")
                        jumpy()
                        sprite_counter = 0
menu()
