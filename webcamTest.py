import cv2
import numpy

# define a video capture object
vid = cv2.VideoCapture(0)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    if frame is None:
        break
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (70, 1, 1), (80, 255, 255))

    frame_flip = cv2.flip(frame, 1)
    frame_threshold_flip = cv2.flip(frame_threshold, 1)

    # Display the resulting frame
    cv2.imshow('adjusted frame', frame_threshold_flip)

    contours, hierarchy = cv2.findContours(frame_threshold_flip, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv2.contourArea(x))
    cv2.drawContours(frame_flip, [contours], -1, (255, 255, 0), 2)
    cv2.imshow("contours", frame_flip)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()