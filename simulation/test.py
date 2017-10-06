from PIL import Image
import matplotlib
from IPython.display import display
from gtsrb import *

qnn = pickle.load(open("gtsrb-w1a1.pickle", "rb"))


#img = prepare_gtsrb(Image.open("pics/50.jpg"))
#img2 = prepare_gtsrb(Image.open("pics/left.jpg"))
#img3 = prepare_gtsrb(Image.open("pics/right.jpg"))
#img4 = prepare_gtsrb(Image.open("pics/stop.jpg"))
img5 = prepare_gtsrb(Image.open("test_pics/stoptest2.jpg"))
img6 = prepare_gtsrb(Image.open("test_pics/stoptest3.jpg"))

#gtsrb_predict(img)
#gtsrb_predict(img2)
#gtsrb_predict(img3)
#gtsrb_predict(img4)
gtsrb_predict(img5)
gtsrb_predict(img6)
