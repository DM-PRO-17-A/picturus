import numpy as np
import cv2

cap = cv2.VideoCapture(1)

prod = False

if prod:
    w = 432
    h = 240
    fps = 5

    ch = int(h * 0.75)
    cw = int(w * 0.5)

    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.cv.CV_CAP_PROP_FPS, fps)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if prod:
        # Crop the frame
        frame = frame[0:ch, cw:w]


    # Display the resulting frame
    cv2.imshow('Capturing', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()