# For sliding window image pyramid, credit to https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/

import cv2
import imutils
import timeit
import ctypes
import time


# Load bridge to C++
bridge = ctypes.cdll.LoadLibrary('./misc/test_queue.so')


# Initialize video capture with camera at index
cap = cv2.VideoCapture(1)


# Counters for timers and filenames
frame_count = 0


# How will the window be handled?
window_send = False
window_save = False
window_draw = False


# Resolution, fps, crop.
w = 432
h = 240
fps = 5

ch = int(h * 0.75)
cw = int(w * 0.5)


# Save initial image from framing and reference
if window_save:
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 960)
    adjust_count = 0
    while adjust_count < 10:
        ret, img = cap.read()
        adjust_count += 1
    cv2.imwrite('./img/test/0_full.jpg'.format(frame_count), img)


# Set resolution and fps
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)
cap.set(cv2.cv.CV_CAP_PROP_FPS, fps)


# Save image post-resolution set
if window_save:
    adjust_count = 0
    while adjust_count < 10:
        ret, img = cap.read()
        adjust_count += 1
    cv2.imwrite('./img/test/1_lowres.jpg'.format(frame_count), img)


# Sliding window width and height
(winW, winH) = (32, 32)


# Helper function for sliding window over a given frame
def sliding_window(image, step_size, window_size):
    # slide a window across the image
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            # yield the current window
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])


# Wrapping helper function for image pyramid
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


time_per_frame = timeit.default_timer()


# Normally the loop would just be while(True), but it's easier to time a set amount.
frame_cap = 500

if window_save:
    frame_cap = 1

while(frame_count < frame_cap):
    # Capture frame-by-frame

    time_per_read = timeit.default_timer()
    ret, frame = cap.read()
    time_per_read = timeit.default_timer() - time_per_read

    time_per_cvt = timeit.default_timer()
    if not window_save:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
    time_per_cvt = timeit.default_timer() - time_per_cvt

    # Crop the frame
    time_per_crop = timeit.default_timer()
    frame = frame[0:ch, cw:w]
    time_per_crop = timeit.default_timer() - time_per_crop

    if window_save:
        cv2.imwrite('./img/test/2_cropped.jpg'.format(frame_count), frame)

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
    for resized_frame in pyramid(frame, scale=1.25):
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

            # If we want to send the window as an array to our given C++ function.
            if window_send:
                window_reshaped = window.reshape(-1)
                window_output = (ctypes.c_int * len(window_reshaped))(*window_reshaped) # This line is EXTREMELY slow
                bridge.iterate_input(window_output)

            # If generating .jpg testdata, save every window as a file.
            # Surprisingly gentle on performance.
            if window_save:
                cv2.imwrite('./img/test/f{}_p{}_w{}.jpg'.format(frame_count, pyr_count, win_count), window)

            # Sometimes it can be helpful to see the windows visualized.
            # Not a performance hit, but wildly distracting and glitchy
            if window_draw:
                cv2.rectangle(resized_frame, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
                cv2.imshow("Preview", resized_frame)
                cv2.waitKey(1)

            time_per_handle = timeit.default_timer() - time_per_handle

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
