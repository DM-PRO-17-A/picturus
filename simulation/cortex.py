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
        if res[i] > 0.01:
            if res[i] > temp_max:
                temp_max = res[i]
                index = i
                sign = gtsrb_classes[index]
    return sign, temp_max


# path = "pics/"
path = "pics/demo/"
pics = []
for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
        pics.append(path + filename)
    break
pics = open_images(pics)


fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
fsm = fsm_states[0]
pcb = Daughter_Card()
signals = {'Turn right ahead': 'r', 'Turn left ahead': 'l', 'Stop': 's', '50 Km/h': '5', '70 Km/h': '7', '100 Km/h': '1'}
weights = [0] * 43
weights[2] = 1 # 50 km/h
weights[4] = 1 # 70 km/h
weights[7] = 1 # 100 km/h
weights[14] = 1 #stop
weights[33] = 1 # turn right
weights[34] = 1 # turn left


while True:
    print "Drive"
    sleep(3)

###################
# This should loop through all pictures for each frame, calculating a final result array to use
    print "Get next picture"
    fsm = fsm_states[1]
    print "Analyse frame with QNN"
    for pic in pics:
    # pic = pics[randrange(0, len(pics))]
        # print "The chosen picture is " + pic[0]

        res = gtsrb_predict(pic[1])

        average = [0] * 43
        for i in range(len(res)):
            average[i] += res[i]*weights[i]
    
###################

    # Send a single result per frame
    print "Send result array to daughter card"
    sign, prob = get_most_probable_sign(average)
    fsm = fsm_states[pcb.send(signals[sign], prob)]
    
    if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"

    # Iterate cycle one step, i.e. take another picture and process it, replacing the old ones
    # !!!Somehow call the script!!!
    break
