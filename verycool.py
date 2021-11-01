import pygame
import random
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Initial Variables for Screen Size and Window Caption
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Side Scroller")


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

    # Load the player image
    ## (Did not work when the image was called boy.png? Maybe \b is a command or something idk)
    player = pygame.image.load("assets\player.png")

    # Scale the player down to fit the game
    player = pygame.transform.rotozoom(player,0,0.2)

    # Keep track of the player's y-value
    player_y = 325

    # Keeps track of if the player is currently jumping
    jump = 0

    # Keeps track of the player's jump, and when to return to the ground
    jump_count = 0

    # Keeps track of the height of the jump
    jump_height = 8

    momentum = True

    # Gravity
    gravity = 4

    # Load crate image
    crate = pygame.image.load("assets\crate.png")

    # Scale crate image
    crate = pygame.transform.rotozoom(crate,0,0.8)

    # Keeps track of the crate's x-value and speed
    ## (Note that it starts slightly outside the window)
    crate_x = 700
    crate_speed = 3







    # While the game is running...
    while True:

        # Draw 3 instances of the background image (allows scrolling)
        ## One to the left of the screen, one to the right, and one in the middle
        ### 640 is the length of the game screen
        screen.blit(image, (bg_x - 640, 0))
        screen.blit(image, (bg_x, 0))
        screen.blit(image, (bg_x + 640, 0))

        # Move background 1 pixel
        bg_x -= 1

        # Reset the background when the background has moved the length of the screen
        if bg_x <= -640:
            bg_x = 0

        # Draw the player on top of the background in a fixed spot
        ## (The .blit command returns a rectangle around the player, which we use for collisions)
        player_rect = screen.blit(player, (50, player_y))

        # Gravity needs to affect the player if they are in the air
        if player_y < 325:
            player_y += gravity

        # If a jump is happening, the player rises 4 pixels for 40 frames, then the jump ends
        if jump == 1:
            if momentum:
                player_y -= jump_height
            jump_count += 1
            if jump_count > 40:
                momentum = False
            if jump_count > 80:
                jump_count = 0
                jump = 0
                momentum = True


        # Display crate
        crate_rect = screen.blit(crate,(crate_x,360))

        # Make the crate move
        crate_x -= crate_speed

        # Regenerate the crate with randomized stats when it disappears
        if crate_x <= -75:
            crate_x = random.randint(700,800)
            crate_speed = random.randint(3,5)

        """
        # Return to menu on collision with crate
        if player_rect.colliderect(crate_rect):
            return
        """

        # Listen for messages from webcamtest


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
                        jump = 1
menu()

