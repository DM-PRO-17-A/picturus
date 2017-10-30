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

import numpy as np


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


def softmax(v):
    e_x = np.exp(v - np.max(v))
    return e_x / e_x.sum()

def relulayer(v):
    return np.asarray(map(lambda x: x if x>0 else 0, v))
    

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
signals = {'Turn right ahead': 'r', 'Turn left ahead': 'l', 'Stop': 's', 'No entry for vehicular traffic': 'u', '50 Km/h': '5', '70 Km/h': '7', '100 Km/h': '1'}
weights = [0] * 43
weights[2] = 1 # 50 km/h
weights[4] = 1 # 70 km/h
weights[7] = 1 # 100 km/h
weights[14] = 1 #stop
weights[17] = 1 # no entry
weights[33] = 1 # turn right
weights[34] = 1 # turn left


print "Drive"
sleep(3)

while True:
    print "Get next picture"
    fsm = fsm_states[1]

    print "Analyse frame with QNN"
    average = [0] * 43
    for pic in pics:
        res = gtsrb_predict(pic[1])

        for i in range(len(res)):
            if res[i] > 0.9:
                average[i] *= 0.8
                average[i] += res[i]*weights[i]

    average = softmax(average)
    average = relulayer(average)
    
    # Send a single result per frame
    print "Send result array to daughter card"
    sign, prob = get_most_probable_sign(average)
    print prob
    if prob > 0.5:
        fsm = fsm_states[pcb.send(signals[sign], prob)]
    else:
        fsm = fsm_states[pcb.send('f', -1)]
                
    if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"

    # Iterate cycle one step, i.e. take another picture and process it, replacing the old ones
    # !!!Somehow call the script!!!
    break
