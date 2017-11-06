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
# For normalising result array
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


# The last layer of the QNN
# Used to make sense of the collective output of each frame
def softmax(v):
    e_x = np.exp(v - np.max(v))
    return e_x / e_x.sum()


# FSM is most likely not needed here
fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
fsm = fsm_states[0]
pcb = Daughter_Card()
signals = {'Turn right ahead': 'r', 'Turn left ahead': 'l', 'Stop': 's', 'No entry for vehicular traffic': 'u', '50 Km/h': '5', '70 Km/h': '7', '100 Km/h': '1', 'Drive': 'f'}


# Weights to prioritise the signs we use
# Just ignoring the others leads to very wrong behaviour
weights = [0.5] * 43
weights[2] = 1 # 50 km/h
weights[4] = 1 # 70 km/h
weights[7] = 1 # 100 km/h
weights[14] = 1 #stop
weights[17] = 1 # no entry
weights[33] = 1 # turn right
weights[34] = 1 # turn left


path = "pics/demo/"
pics = []
for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
        pics.append(path + filename)
    break
pics = open_images(pics)


def main():
    fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
    fsm = fsm_states[0]
    # Keep a running average
    average = [0] * 43
    while True:
        print "Drive"
        # sleep(3)

        # Iterate cycle one step, i.e. take another picture and process it
        # Call camera script
        # Get array of the images to use next
        ########################################
        # This whole part will be replaced with a single call to a script
        print "Get next picture"
        # pics = ???
        # fsm = fsm_states[1]

        print "Analyse frame with QNN"
        for pic in pics:
            # Replace with call to actual QNN on FPGA
            # Will be done in a C++ script?
            res = gtsrb_predict(pic[1])
            # print gtsrb_classes[res.argmax(axis=0)]
            for i in range(len(res)):
                if res[i] > 0.9:
                    average[i] += res[i]*weights[i]
        ########################################
        # Get output values from QNN and process them
        average = softmax(average)
                    
        # Send a single result per frame
        print "Send result array to daughter card"
        sign, prob = get_most_probable_sign(average)
        print prob
        # Send UART signal to PCB
        if prob > 0.75:
            fsm_states = fsm_states[pcb.send(signals.get(sign, 'f'), prob)]
        else:
            fsm_states = fsm_states[pcb.send(signals['Drive'], -1)]
            
        # if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"
        
        break


if  __name__ =='__main__':
    main()
