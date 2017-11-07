# Open images
from PIL import Image
# For finding all files in a directory
from os import walk
from scipy import ndimage
from scipy import misc
#from scipy import spatial
import numpy as np
import math
from datetime import datetime
from time import time
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
S = time()
for (dirpath, dirnames, filenames) in walk(in_path):
    for filename in filenames: 
        if '.jpg' in filename:
            img = np.array(Image.open(in_path + filename))
            #s = time()
            #p = preprocessing(img, colors, radii, 3)
            p = preprocessing(img, colors, radii, 4)
            if p.shape == (2,2):
                continue
            #print time()-s
            misc.imsave(out_path+filename, p)
print "Total time: " + str(time()-S)
