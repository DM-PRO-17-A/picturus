import cv2
import numpy as np

img = cv2.imread('img.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB);

print('3D list')
print(img)

print('')
print('3D list - First row')
print(img[0])

oned = img.reshape(-1)

print('')
print('1D list')
print(oned)
