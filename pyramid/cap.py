import numpy as np
import cv2

cap = cv2.VideoCapture(1)

w = 432
h = 240

ch = int(h * 0.75)
cw = int(w * 0.5)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 432)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 5)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Crop the frame
    cropped_frame = frame[0:ch, cw:w]

    # Our operations on the frame come here
    gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)


    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()