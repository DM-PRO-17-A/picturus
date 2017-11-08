# For finding all files in a directory
from scipy import ndimage
from scipy import misc
import numpy as np
import math
from numpy import linalg

# Euclidean distance between the color of a pixel and a specified color
def distance(pixel, color):
    return np.linalg.norm(pixel-color)

# Find pixels with color in a specified color range
def get_colored_region(image,colors,radii):
    X, Y, z = image.shape
    new_img = np.zeros((X,Y))
    for x in xrange(X):
        for y in xrange(Y):
            for i in xrange(len(colors)):
                if distance(image[x,y],colors[i]) < radii[i]:
                    new_img[x,y] = 1
    return new_img.astype(np.int)

# Find center of object
def get_center_of_mass(image):
    x, y = image.shape
    m = image.astype(np.float)
    m = m / max(np.sum(m),1)
    dx, dy = np.sum(m,1), np.sum(m,0)
    cx, cy = np.sum(dx * np.arange(x)), np.sum(dy * np.arange(y))
    return int(math.ceil(cx)), int(math.ceil(cy))

# Find size of object
def get_size(image):
    x, y = image.shape
    m = image.astype(np.int)
    sx = np.sum(m,1)
    sy = np.sum(m,0)
    w, h = max(sx), max(sy)
    size = int(math.ceil((w+h)/2))
    return size

def dilate(img, structure):
    x, y = structure.shape
    x, y = int((x-1)/2), int((y-1)/2)
    X, Y = img.shape
    R, C = X+(2*x), Y+(2*y)
    new_img = np.zeros((R, C))
    new_img[x:R-x, y:C-y] = img.astype(np.int)
    temp = new_img.copy()
    for c in xrange(y, C-y):
        for r in xrange(x, R-x):
            if img[r-x][c-y] == 1:
                new_img[(r-x):(r+x+1), (c-y):(c+y+1)] = new_img[(r-x):(r+x+1),(c-y):(c+y+1)]+structure
#                new_img[(r-x):(r+x+1), (c-y):(c+y+1)] += structure
    new_img = new_img[x:(R-x), y:(C-y)]
    return new_img.astype(np.bool_)

def dilation(image, structure, iterations=1):
    if iterations == 1:
        return dilate(image.astype(np.bool_),structure)
    else:
        result = dilate(image.astype(np.bool_),structure)
        for it in xrange(iterations-1):
            result = dilate(result, structure)
        return result

# Get coordinates of object
def get_coords(seg_img):
    struct = np.ones((3,3))
    #img = ndimage.binary_dilation(seg_img, struct, 3)
    img = dilation(seg_img, struct, 3).astype(np.int)
    img = ndimage.binary_fill_holes(img)
    structure1 = np.ones((5,5))
    res=ndimage.binary_hit_or_miss(img,structure1=structure1,origin1=0).astype(np.int)
    center = get_center_of_mass(res)
    dim = get_size(res)
    return [center[0]-dim,center[0]+dim,center[1]-dim,center[1]+dim]

def crop(image, coords):
    return image[coords[0]:coords[1],coords[2]:coords[3]]

def preprocessing(image, colors, radii, scale):
    x,y,z = image.shape
    img = misc.imresize(image, (int(x/scale), int(y/scale)))
    img = get_colored_region(img,colors,radii)
    cv2.imshow('thresh', img)
    if np.sum(img) > 30: # random
        coords = get_coords(img)
        try:
            coords = np.multiply(coords, scale)
            res = crop(image, coords)
            return misc.imresize(res, (32,32))
        except ValueError:
            return np.zeros((2,2))
    else: return np.zeros((2,2))

in_path = "pics/in/"
out_path = "pics/out/"

red = np.array([123,34,30])
#blue = np.array([25,50,110])
blue = np.array([21,42,95])
radii = [30, 45]
colors = [red, blue]


##### Ane's color magic ends here #####


import cv2
import timeit
import ctypes


# Load bridge to C++
bridge = ctypes.cdll.LoadLibrary('./misc/test_queue.so')

# Initialize video capture with camera at index
cap = cv2.VideoCapture(1)

# Counters for timers and filenames
frame_count = 0

# How will the window be handled?
frame_send = False
frame_save = False
frame_draw = False

# Resolution, fps, crop.
w = 432
h = 240
fps = 5
ch = int(h * 0.75)
cw = int(w * 0.5)

# Save initial image from framing and reference
if frame_save:
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
if frame_save:
    adjust_count = 0
    while adjust_count < 10:
        ret, img = cap.read()
        adjust_count += 1
    cv2.imwrite('./img/test/1_lowres.jpg'.format(frame_count), img)

time_per_frame = timeit.default_timer()

# Normally the loop would just be while(True), but it's easier to time a set amount.
frame_cap = 500

if frame_save:
    frame_cap = 1

while(frame_count < frame_cap):
    # Capture frame-by-frame

    time_per_read = timeit.default_timer()
    ret, frame = cap.read()
    time_per_read = timeit.default_timer() - time_per_read

    # TODO: Move cvtColor
    '''
    if not frame_save:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
    '''

    # Crop the frame
    frame = frame[0:ch, cw:w]

    if frame_save:
        cv2.imwrite('./img/test/2_cropped.jpg'.format(frame_count), frame)

    # Display the resulting frame
    cv2.imshow('Capturing', frame)

    time_per_wait = timeit.default_timer()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  
    time_per_wait = timeit.default_timer() - time_per_wait

    print('Frame {}'.format(frame_count))


    # Handle the frame
    time_per_handle = timeit.default_timer()

    #p = preprocessing(img, colors, radii, 3)
    p = preprocessing(frame, colors, radii, 3)

    if p.shape == (2,2):
        frame_count += 1
        continue
    cv2.imwrite('./img/test/f{}.jpg'.format(frame_count), p)

    print(p)

    time_per_handle = timeit.default_timer() - time_per_handle
    frame_count += 1
time_per_frame = (timeit.default_timer() - time_per_frame)



'''

# If we want to send the window as an array to our given C++ function.
if frame_send:
    frame_reshaped = window.reshape(-1)
    frame_output = (ctypes.c_int * len(frame_reshaped))(*frame_reshaped) # This line is EXTREMELY slow
    bridge.iterate_input(frame_output)

# If generating .jpg testdata, save every window as a file.
# Surprisingly gentle on performance.
if frame_save:
    cv2.imwrite('./img/test/f{}_p{}_w{}.jpg'.format(frame_count, pyr_count, win_count), window)

# Sometimes it can be helpful to see the windows visualized.
# Not a performance hit, but wildly distracting and glitchy
if frame_draw:
    cv2.rectangle(resized_frame, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
    cv2.imshow("Preview", resized_frame)
    cv2.waitKey(1)

'''

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print('')
print('max: {}'.format(frame_cap / fps))
print('time: {}'.format(time_per_frame))
print('')
print('read: {}'.format(time_per_read))
print('wait: {}'.format(time_per_wait))
print('handle: {}'.format(time_per_handle))
print('')
print('Max time per frame: {}'.format(1.0 / fps))
print('Time per frame: {}'.format(time_per_frame / frame_count))
print('Needs to be {} faster per frame.'.format((time_per_frame/frame_count)-(1.0/fps)))
