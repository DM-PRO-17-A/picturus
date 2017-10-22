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
# Multithreading
from thread import start_new_thread


def open_images(pics):
    return map(lambda p: (p, prepare_gtsrb(Image.open(p))), pics)


path = "pics/"
pics = []
for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
        pics.append(path + filename)
    break
#pics = []
#filename_base = 'test'
#for i in range(15):
#    filename = filename_base + str(i) + '.jpg'
#    pics.append(path + filename)



average_result = [0] * 43
# Update for each picture, each frame?
# How to decay?


fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
fsm = fsm_states[0]
pcb = Daughter_Card()


pics = open_images(pics)


# For testing only, to run through a certain set of pictures
# count = 0

while True:
    print "Drive"
    sleep(3)

    # if fsm == "driving":
    print "Get random picture"
    fsm = fsm_states[1]
    pic = pics[randrange(0, len(pics))]
    #pic = pics[count]
    print "The chosen picture is " + pic[0]

    print "Send to QNN"
    res = gtsrb_predict(pic[1])

    print "Send result array to daughter card"
    # TODO: implement sends as new threads
    # How to update state?
    # start_new_thread(pcb.send, (res, ))
    # pcb.get_state() perhaps?
    fsm = fsm_states[pcb.send(res)]

    if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"
    
    # count += 1
    #if count >= len(pics):
    #    break
