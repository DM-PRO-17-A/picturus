import cv2
import numpy as np

img = cv2.imread('../img/out.jpg')
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
print(oned.tolist())

f = open('vector.txt', 'w')
f.write(' '.join(str(v) for v in oned.tolist()))
