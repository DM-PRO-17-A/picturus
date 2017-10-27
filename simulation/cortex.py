# Open images
from PIL import Image
# Contains functions for using the QNN
from gtsrb import *
from daughter_card import Daughter_Card
# For simulation purposes
from time import sleep
from random import randrange
# For finding all files in a directory
from os import walk

# Multithreading and signaling
# Not necessary at this point?
from thread import start_new_thread
import signal


def open_images(pics):
    return map(lambda p: (p, prepare_gtsrb(Image.open(p))), pics)


def get_most_probable_sign(res):
    temp_max = -1
    index = -1
    for i in range(len(res)):
        if int(res[i]*100) != 0:
            if res[i] > temp_max:
                temp_max = res[i]
                index = i
                sign = gtsrb_classes[index]
    return sign, temp_max


path = "pics/"
pics = []
for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
        pics.append(path + filename)
    break
pics = open_images(pics)


fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
fsm = fsm_states[0]
pcb = Daughter_Card()


while True:
    print "Drive"
    sleep(3)

    print "Get random picture"
    fsm = fsm_states[1]
    pic = pics[randrange(0, len(pics))]
    print "The chosen picture is " + pic[0]

    print "Send to QNN"
    res = gtsrb_predict(pic[1])

    print "Send result array to daughter card"
    sign, prob = get_most_probable_sign(res)
    fsm = fsm_states[pcb.send(sign, prob)]
    
    if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"
