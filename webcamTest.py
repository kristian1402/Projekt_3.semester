import cv2, numpy, socket

# Easy access to green color values, not actually used
green_1_test = (78, 0, 246), (94, 12, 255)
green_2_test = (70, 79, 146), (85, 255, 255)

# Define a video capture object
vid = cv2.VideoCapture(0)

# Varibles that store the X and Y coordinate of the yellow center circle
cX = 0
cY = 0

# Stores the last 5 center coordinates
cList = []

# Delay counter
delay = 0

# Jump counter
jumpNumber = 0

# Jump type
jumpType = 0

# Jump Check
jumpCheck = False

while (True):
    # Capture the video frame by frame
    ret, frame = vid.read()

    # If there isn't a frame, stop
    if frame is None:
        break

    # Convert the frame to HSV and run the green-color threshold
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (35, 58, 81), (93, 164, 255))

    # We want to flip the normal frame and the threshold frame to mimic a webcam - feels more natural
    frame_flip = cv2.flip(frame, 1)
    frame_threshold_flip = cv2.flip(frame_threshold, 1)
    blur = cv2.GaussianBlur(frame_threshold_flip, (7, 7), cv2.BORDER_DEFAULT)

    # Display the resulting frame + the center circle

    cv2.circle(frame_flip, (cX, cY), 7, (0, 255, 255), -1)
    #cv2.rectangle(frame_threshold_flip, (0, 80), (1000, 85), (255, 0, 0), 0)
    cv2.imshow('adjusted frame', blur)

    # Finds the contours around the largest cluster of pixels - should be the green glove
    contours, hierarchy = cv2.findContours(frame_threshold_flip, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if numpy.all(hierarchy) != None:

        # Draws the contours
        contours = max(contours, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(frame_flip, [contours], -1, (255, 255, 0), 2)

        #Find average position of contours
        M = cv2.moments(contours)

        # Avoiding a division by 0 error
        if int(M["m00"]) != 0:

            # Define center position of the largest cluster of pixels
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

        # Puts the Y-coordinate into the list
        cList.append(cY)

        # The last 5 frame's y-coordinates are put into a list, any older are popped out
        if (len(cList) > 5):
            cList.pop(0)
        # The delay variable ensures that the same gesture doesn't get recognized multiple times
        if (delay == 0):

            # Avoids out-of-bounds errors in the beginning
            if(len(cList) == 5):

                # If the current frame is 120 pixels above the frame 10 frames previously...
                if(cList[0] - 150 > cList[4]):
                    jumpType = 1

                    # Perform jump action, and set the delay
                    with open('jumpfile.txt', 'w') as f:
                        f.writelines(str(jumpType))
                    f.close
                    print(f"Jump #{jumpNumber}")
                    jumpNumber += 1
                    delay = 5
                    print(cList[4] - cList[0])

                elif(cList[0] - 120 > cList[4]):
                    jumpType = 2

                    # Perform jump action, and set the delay
                    with open('jumpfile.txt', 'w') as f:
                        f.writelines(str(jumpType))
                    f.close
                    print(f"Jump #{jumpNumber}")
                    jumpNumber += 1
                    delay = 5
                    print(cList[4] - cList[0])

                elif (cList[0] - 75 > cList[4]):
                    jumpType = 3

                    # Perform jump action, and set the delay
                    with open('jumpfile.txt', 'w') as f:
                        f.writelines(str(jumpType))
                    f.close
                    print(f"Jump #{jumpNumber}")
                    jumpNumber += 1
                    delay = 5
                    print(cList[4] - cList[0])


                    # Send jump action to server


        else:
            # The delay makes it so the program waits 5 frames before accepting more input
            delay -= 1

    # Show image
    cv2.imshow("contours", frame_flip)


    # Old code that printed if the hand was inside a rectangle
    """
    #for contours in contours:
        x, y, _, _ = cv2.boundingRect(contours)
        if x < 150 and y < 100:
            print("In range")
    """

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()