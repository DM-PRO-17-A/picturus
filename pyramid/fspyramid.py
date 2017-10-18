import time
import os

def takepicture():
    orig_img_path = 'test_images/' + 'test' + '.jpg'
    os.system("fswebcam --no-banner --resolution 432x240 --save {} -d /dev/video0 > /dev/null".format(orig_img_path))
    return orig_img_path

print(takepicture())




