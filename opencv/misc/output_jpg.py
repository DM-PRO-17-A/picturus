# Simple script to capture a single frame for testing purposes

import cv2

cap = cv2.VideoCapture(1)

w = 432
h = 240
fps = 5

ch = int(h * 0.75)
cw = int(w * 0.5)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)
cap.set(cv2.cv.CV_CAP_PROP_FPS, fps)

while(True):
    ret, frame = cap.read()
    frame = frame[0:ch, cw:w]
    cv2.imshow('Press q to save image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('../img/out.jpg', frame)
        break

cap.release()
cv2.destroyAllWindows()
