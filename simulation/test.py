from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import imshow
import numpy as np

img = Image.open("pics/50.jpg")
img = img.convert("L")
img = np.asarray(img)
# % matplotlib inline
plt.imshow(img, cmap='gray')
plt.show()

# from QNN.layers import *
# import pickle

# qnn = pickle.load(open("mnist-w1a1.pickle", "rb"))
# qnn

