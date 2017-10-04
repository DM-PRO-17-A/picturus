from PIL import Image
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import numpy as np

img = Image.open("pics/50.jpg")
img = img.convert("L")
img = np.asarray(img)
plt.imshow(img, cmap='gray')
plt.show();
