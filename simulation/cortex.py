# Open images
from PIL import Image
# Contains functions for using the QNN
from gtsrb import *
from daughter_card import Daughter_Card
# For simulation purposes
from time import sleep
from random import randrange



# Maybe install termcolor for colored output?
# from termcolor import colored

fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
fsm = fsm_states[0]
pcb = Daughter_Card()


def open_images(pics):
    return map(lambda p: (p, prepare_gtsrb(Image.open(p))), pics)


# TODO: give images more meaningful file names
test_case_normal_signs = open_images(("pics/50.jpg", "pics/left.jpg", "pics/right.jpg", "pics/stop.jpg"))
test_case_zoom = open_images(("test_pics/stoptest.jpg", "test_pics/stoptest1.jpg", "test_pics/stoptest2.jpg", "test_pics/stoptest3.jpg"))
test_case_partially_covered = open_images(("test_pics/stop75.jpg", "test_pics/stop85.jpg", "test_pics/stop90.jpg", "test_pics/stop95.jpg"))
tests = (test_case_normal_signs, test_case_zoom, test_case_partially_covered)


# # TODO: improve readability of output
# for pics in tests:
#     for pic in pics:
#         print pic[0]
#         gtsrb_predict(pic[1])


while True:
    break
    print "Drive"
    sleep(3)

    print "Get random picture"
    fsm = fsm_states[1]
    pic = test_case_normal_signs[randrange(0, len(test_case_normal_signs))]
    print "The chosen picture is " + pic[0]

    print "Send to QNN"
    res = gtsrb_predict(pic[1])

    print "Send result array to daughter card"
    fsm = fsm_states[pcb.send(res)]

    if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"

        
# Code example of how to get all files from a directory
# We want to look at all the pictures taken at a given time
from os import walk
path = "pics/"

pics = []
for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
        pics.append(path + filename)
    break
print pics

# Use with average
average_result = [0] * 43
# Update for each picture, each frame?
# How to decay?
