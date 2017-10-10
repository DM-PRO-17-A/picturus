# USAGE
# python pyramid.py --image images/rubberducky.jpg
#Credit to https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/

import argparse
import cv2
import imutils
import timeit
import uuid
from datetime import datetime

start_time = timeit.default_timer()


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


def sliding_window(image, step_size, window_size):
    # slide a window across the image
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            # yield the current window
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image and define the window width and height
image = cv2.imread(args["image"])
(winW, winH) = (128, 128)

# loop over the image pyramid
for resized in pyramid(image, scale=1.5):
    counter = 0
    # loop over the sliding window for each layer of the pyramid
    for (x, y, window) in sliding_window(resized, step_size=16, window_size=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        counter += 1
        unique_filename = str(datetime.now())
        clone = window.copy()
        #path = '/home/embrik/Datamaskinprosjekt/picturus/pyramid/test_images'
        cv2.imwrite('./test_images/' + unique_filename + 'test' + str(counter) + '.jpg', clone)

        # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
        # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
        # WINDOW

        # since we do not have a classifier, we'll just draw the window
        # clone = resized.copy()
        # cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        # cv2.imshow("Window", clone)
        # cv2.waitKey(1)


print(timeit.default_timer() - start_time)
