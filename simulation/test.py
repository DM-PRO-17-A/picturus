from PIL import Image
from matplotlib.pyplot import imshow
import numpy as np

img = Image.open("pics/50.jpg")
img = img.convert("L")
img = np.asarray(img)
% matplotlib inline
plt.show(img, cmap='gray')
