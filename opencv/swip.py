# Credit to https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/

import cv2
import imutils
import timeit
import ctypes

bridge = ctypes.cdll.LoadLibrary('./misc/test_queue.so')

cap = cv2.VideoCapture(0)

# Prod: Resolution and fps
w = 432
h = 240
fps = 5

ch = int(h * 0.75)
cw = int(w * 0.5)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)
cap.set(cv2.cv.CV_CAP_PROP_FPS, fps)

# Window width and height
(winW, winH) = (32, 32)


# it's weird man
def sliding_window(image, step_size, window_size):
    # slide a window across the image
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            # yield the current window
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])


# uhmmm
def pyramid(image, scale=1.5, min_size=(32, 32)):
    # yield the original image
    yield image

    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)

        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < min_size[1] or image.shape[1] < min_size[0]:
            break

        # yield the next image in the pyramid
        yield image

frame_count = 1

time_per_frame = timeit.default_timer()


# Normally this would just be while(True), but easier to time a set amount.
frame_cap = 100
while(frame_count < frame_cap):
    # Capture frame-by-frame

    time_per_read = timeit.default_timer()
    ret, frame = cap.read()
    time_per_read = timeit.default_timer() - time_per_read

    time_per_cvt = timeit.default_timer()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
    time_per_cvt = timeit.default_timer() - time_per_cvt

    # Prod: Crop
    time_per_crop = timeit.default_timer()
    frame = frame[0:ch, cw:w]
    time_per_crop = timeit.default_timer() - time_per_crop

    # Display the resulting frame
    time_per_show = timeit.default_timer()
    cv2.imshow('Capturing', frame)
    time_per_show = timeit.default_timer() - time_per_show

    time_per_wait = timeit.default_timer()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  
    time_per_wait = timeit.default_timer() - time_per_wait

    print('Frame {}'.format(frame_count))

    pyr_count = 0
    win_count = 0
    ign_count = 0
    # loop over the image pyramid
    for resized_frame in pyramid(frame, scale=1.5):
        print('Frame {}, level {}'.format(frame_count, pyr_count))
        # loop over the sliding window for each layer of the pyramid
        for (x, y, window) in sliding_window(resized_frame, step_size=16, window_size=(winW, winH)):

            print('Frame {}, level {}, window {}'.format(frame_count, pyr_count, win_count))

            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                print('Frame {}, level {}, window {}, ignore {}'.format(frame_count, pyr_count, win_count, ign_count))
                ign_count += 1
                continue

            # Handle the frame
            time_per_handle = timeit.default_timer()
            window_reshaped = window.reshape(-1)
            window_output = (ctypes.c_int * len(window_reshaped))(*window_reshaped) # This line is EXTREMELY slow
            bridge.iterate_input(window_output)
            time_per_handle = timeit.default_timer() - time_per_handle

            # Draw the window
            # cv2.rectangle(resized_frame, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
            # cv2.imshow("Preview", resized_frame)
            # cv2.waitKey(1)

            win_count += 1
        pyr_count += 1
    frame_count += 1
time_per_frame = (timeit.default_timer() - time_per_frame)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print('')
print('max: {}'.format(frame_cap / fps))
print('time: {}'.format(time_per_frame))
print('')
print('read: {}'.format(time_per_read))
print('cvt: {}'.format(time_per_cvt))
print('crop: {}'.format(time_per_crop))
print('show: {}'.format(time_per_show))
print('wait: {}'.format(time_per_wait))
print('handle: {}'.format(time_per_handle))
print('')
print('Max time per frame: {}'.format(1.0 / fps))
print('Time per frame: {}'.format(time_per_frame / frame_count))
print('Needs to be {} faster per frame.'.format((time_per_frame/frame_count)-(1.0/fps)))
