import pygame, glob, random

# Initialize everything imported (otherwise things such as the font does not work)
pygame.init()

# Varibles to keep track of the time
clock = pygame.time.Clock()
passed_time = 0

# Initial Variables
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Side Scroller")

font = pygame.font.SysFont("impact", 20)
bigfont = pygame.font.SysFont("impact", 30)

high_score = 0
jump_success = False

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

def rating_func():
    global rating
    # Jump rating based on marker
    if crate_x - 85 < player_x:
        rating = "Perfect!"
    elif crate_x - 175 < player_x < crate_x - 85:
        rating = "Nice!"
    else:
        rating = ""

def show_rating():
    global jump_occured
    global rating
    global ratingdisplay
    global timer
    global score
    global fall_count
    if jump_occured:
        jump_occured = False
        if rating == "Perfect!" and fall_count == 0:
            score += 100
        if rating == "Nice!" and fall_count == 0:
            score += 50
        timer = 70
        if timer > 0:
            ratingdisplay = rating
# Game-screen function
## (Lots of necessary code is repeated from menu)
def game():

    #VARIABLES FOR THIS PAM ONLY
    fall_immune = False

    # Start by clearing the txt file (just in case)
    file = open("jumpfile.txt", "w")
    file.close()

    # Start timer
    global passed_time
    global clock
    start_time = pygame.time.get_ticks()

    # Load the menu image and stretch it to the window size
    image = pygame.image.load("assets\level1.png")
    image = pygame.transform.scale(image, (640, 480))

    # Keep track of the x-value of the background image
    bg_x = 0

    # Scroll speed
    scroll_speed = 1
    current_speed = scroll_speed

    # Sprite variables
    sprite_counter = 0
    sprite_delay = 0
    sprite_delay_amount = 0

    # Load the player running sprites and jumping sprites
    run_sprites = [pygame.image.load(img) for img in glob.glob("assets\Run\\*.png")]
    jump_sprites = [pygame.image.load(img) for img in glob.glob("assets\Jump\\*.png")]
    fall_sprites = [pygame.image.load(img) for img in glob.glob("assets\Fall\\*.png")]
    player = run_sprites[sprite_counter]

    # Keep track of the player's x and y-value
    global player_x
    player_x = 107
    player_y = 325

    # Keeps track of if the player is currently jumping
    global jump
    jump = 0

    # Keeps track of the player's jump, and when to return to the ground
    jump_count = 0
    jump_count_start = -12

    # Keeps track of the height of the jump
    jump_height = 8

    # Decreases the time of the jump
    jump_diff_add = 0.5

    # Jump occured
    global jump_occured
    jump_occured = False

    # Jump rating
    global rating
    global ratingdisplay
    global timer
    ratingdisplay = ""
    rating = ""
    display_rating = False
    timer = 0

    # Keeps track of if the player is currently falling
    global fall_count
    fall = 0
    fall_count = 0

    intro_text = True

    # Gravity
    gravity = 4

    # Score
    global score
    score = 0

    # Difficulty increase
    difficulty_increase = 0

    # Load crate image
    crate = pygame.image.load("assets\crate.png")

    # Scale crate image
    crate = pygame.transform.rotozoom(crate,0,0.8)

    # Keeps track of the crate's x-value and speed
    ## (Note that it starts slightly outside the window)
    global crate_x
    crate_x = 1500
    crate_speed = 5
    crate_speed_low = 5
    crate_speed_high = 7
    crate_spawn_low = 1000
    crate_spawn_high = 1100

    # Keeps track of the amount of crates - after 20, end the game
    crate_counter = 0

    # Load house
    house = pygame.image.load("assets\house.png")
    house = pygame.transform.rotozoom(house, 0, 0.1)
    house_rect = (0,0,0,0)
    goal_rect = (0,0,0,0)

    # Move house
    house_bgx = 900

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
                if jump != 1 and fall_count == 0:
                    sprite_counter = 0
            else:
                sprite_counter += 1
            sprite_delay = 0
        else:
            sprite_delay += 1

        # Change sprite based on if the player is jumping / falling or not
        if jump == 0 and fall_count == 0:
            player = run_sprites[sprite_counter]
            sprite_delay_amount = 3
        if jump == 1:
            player = jump_sprites[sprite_counter]
            sprite_delay_amount = 5
        if fall_count > 0:
            player = fall_sprites[sprite_counter]
            sprite_delay_amount = 5


        # Draw the player, scale the player down, blit it on the screen
        player = pygame.transform.rotozoom(player, 0, 0.2)
        player_rect = screen.blit(player, (50, player_y))
        player_hitbox = player_rect.inflate(-50, -10)
        player_hitbox = player_hitbox.move(3, 0)

        # Adjust hitbox if in the middle of jump
        if jump == 1:
            if fall == 0:
                player_hitbox = player_hitbox.move(-13,0)
        #pygame.draw.rect(screen, (255,0,0), (player_hitbox), 1)

        # If the player, for some reason, goes under the ground, put them back
        if player_y > 325:
            player_y = 325

        # If a jump is happening
        if jump == 1:
            jump_occured = True
            player_y += jump_count
            jump_count += jump_diff_add

            # If the player, for some reason, goes under the ground, put them back
            if player_y >= 325:
                player_y = 325
                jump = 0
        else:
            jump_count = jump_count_start
            show_rating()

        if fall == 1:
            current_speed = scroll_speed
            fall = 0
            if fall_count == 0:
                fall_count = 60

        if fall_count == 0:
            scroll_speed = current_speed

        if fall_count > 0:
            scroll_speed = scroll_speed / 1.1
            fall_count -= 1

        # Display crate
        crate_rect = screen.blit(crate,(crate_x,360))

        # Draw the markers before each crate
        red_mark = (crate_x - 300, 417, 300, 10)
        yellow_mark = (crate_x - 180, 417, 90, 10)
        green_mark = (crate_x - 90, 417, 90, 10)
        pygame.draw.rect(screen, (255, 0, 0), (red_mark), 0)
        pygame.draw.rect(screen, (255, 255, 0), (yellow_mark), 0)
        pygame.draw.rect(screen, (0, 255, 0), (green_mark), 0)


        # Make the crate move
        crate_x -= crate_speed

        # Remove Introtext
        if crate_x == 600:
            intro_text = False

        # Regenerate the crate with randomized stats when it disappears
        if crate_x <= -75:
            fall_immune = False
            if crate_counter < 19:
                # Increase difficulty based on current score
                if (crate_counter + 1) % 5 == 0 and crate_counter != 0:
                    print("Speed Increase!")
                    difficulty_increase = True

                if difficulty_increase:

                # As the game progresses, the crates move faster and spawn further apart
                    current_speed += 1
                    crate_speed_low += 1
                    crate_speed_high += 1
                    crate_spawn_low += 50
                    crate_spawn_high += 150
                    difficulty_increase = False

                crate_counter += 1
                crate_x = random.randint(crate_spawn_low, crate_spawn_high)
                if fall_count > 0:
                    crate_x += 500
                crate_speed = random.randint(crate_speed_low, crate_speed_high)

            else:
                house_rect = screen.blit(house, (house_bgx, 240))
                goal_rect = house_rect.inflate(-220,0)
                house_bgx -= 4



        # Write "Speed Up!" on speed up
        if (crate_counter) % 5 == 0 and crate_counter != 0:
            speedtext = font.render("SPEED UP!", 1, (0, 0, 0))
            screen.blit(speedtext, (270, 150))

        # Show tutorial text on start-up
        if intro_text:
            introtext = bigfont.render("Press SPACE to jump!", 1, (0, 0, 0))
            screen.blit(introtext, (175, 150))

        # Draw timer text in the corner at all times
        timertext = font.render("Time: " + str(passed_time / 1000), 1, (0, 0, 0))
        screen.blit(timertext, (20, 20))

        # Draw score
        scoretext = font.render("Score: " + str(score), 1, (0, 0, 0))
        screen.blit(scoretext, (20, 40))

        # Draw jump ratings
        if fall_count == 0:
            jumptext = font.render(str(ratingdisplay), 1, (0, 0, 0))
            screen.blit(jumptext, (80, 270))
        else:
            timer = 0

        # Draw dodges
        if fall_immune:
            immunetext = font.render("Dodged!", 1, (0, 0, 0))
            screen.blit(immunetext, (80, 250))

        # Fall on collision with crate
        if player_hitbox.colliderect(crate_rect):
            if fall_immune == False:
                if fall_count == 0:
                    if random.random() < .5:
                        print("Fall!")
                        fall = 1
                    else:
                        print("No fall!")
                        fall_immune = True

        f = open('jumpfile.txt', 'r+')
        contents = f.read()
        if player_x > crate_x - 300:
            if contents == '1':
                if jump == 0:
                    jump_count_start = -15
                    jump = 1
                    rating_func()
            if contents == '2':
                if jump == 0:
                    jump_count_start = -12
                    jump = 1
                    rating_func()
            if contents == '3':
                if jump == 0:
                    jump_count_start = -10
                    jump = 1
                    rating_func()
        f.truncate(0)
        f.close()

        if player_rect.colliderect(goal_rect):
            return

        # Keep track of time
        passed_time = pygame.time.get_ticks() - start_time
        clock.tick(60)

        # Rating timer
        if timer > 0:
            timer -= 1
        else:
            ratingdisplay = ""

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
                    if player_x > crate_x - 300:
                    # Jump only happens when the player is on the ground and not stumbling
                        if player_y == 325:
                            if fall_count == 0:
                                jump = 1
                                sprite_counter = 0
                                rating_func()

menu()



