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

# def get_most_probable_sign(res):
   # i = np.argmax(res)
   # return gtsrb_classes[i], res[i]

A = np.array([0.10613798, 0.0967258, 0.0944901, 0.08205982, 0.08600254, 0.07336438, 0.09290288, 0.08346851, 0.08365503, 0.10139856, 0.09375499, 0.10817018, 0.12580705, 0.11591881, 0.10589285, 0.1045065,  0.09333096, 0.10654855, 0.09912547, 0.09181008, 0.10024401, 0.10732551, 0.09640726, 0.102323, 0.11001986, 0.10809018, 0.09999774, 0.10208429, 0.0995523,  0.11225812, 0.10275448, 0.09403487, 0.10364552, 0.10415483, 0.10874164, 0.12092833, 0.10799013, 0.09335944, 0.1140102,  0.09289351, 0.11192361, 0.09586933, 0.08955998])
B = np.array([-0.96071649, 0.68546766, 1.44876862, 1.84089804, 1.4770503, 2.17828822, -0.48416716, 0.3688474, 1.08563411, 0.55420429, 0.43626797, 0.16900358, -0.1347385,  0.0145933, -0.54196042, -0.37247148, -0.58978826, -0.4172011, 0.26940933, -0.02862083, 0.28240931, -0.60368943, -0.63643998,  0.05946794, -0.21361144, 0.09381656, -0.09491161, -0.64013398,  0.05029509, -0.51663965, -0.32239845, 0.43873206, -0.75330114, -0.14596492, -0.45224375, -0.29807806,  -0.57703501, -0.58822173, 0.20007333, -0.55777472, -0.56918406, -0.59853441, -0.55538076])

# The last layer of the QNN
# Used to make sense of the collective output of each frame
def scaleshift(v):
    v = np.array(v)
    # the outermost dimension is the channel dimension
    # reshape as inner dimension to apply transform
    vr = v.reshape((A.shape[0], -1)).transpose()
    return (A*vr+B).transpose().flatten().tolist()
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


# path = "pics/in/"
# pics = []
# for (dirpath, dirnames, filenames) in walk(path):
#     for filename in filenames:
#         pics.append(path + filename)
#     break
# pics = open_images(pics)


def main():
    fsm_states = ("driving", "determine sign", "keep driving", "execute sign", "receive interrupt")
    fsm = fsm_states[0]
    
    # Keep a running average
    average = [0] * 43
    folder = 0
    while True:
        
        print "Drive"
        # sleep(3)

        # Iterate cycle one step, i.e. take another picture and process it
        # Call camera script
        # Get array of the images to use next
        ########################################
        # This whole part will be replaced with a single call to a script
        print "Get next picture"
        path = "pics/demo/" + str(folder) + "/"
        print path
        pics = []
        for (dirpath, dirnames, filenames) in walk(path):
            for filename in filenames:
                pics.append(path + filename)
            break
        # print pics
        pics = open_images(pics)
        
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
            # break
        ########################################

        # Get output values from QNN and process them
        # Will be a C++ script
        average = scaleshift(average)
        average = softmax(average)
        # print average.sum()
        # Send a single result per frame
        print "Send result array to daughter card"
        sign, prob = get_most_probable_sign(average)
        print sign
        print prob
        # Send UART signal to PCB
        if prob > 0.75:
            fsm_states = fsm_states[pcb.send(signals.get(sign, 'f'), prob)]
        else:
            fsm_states = fsm_states[pcb.send(signals['Drive'], -1)]
                
        if fsm != "driving":
            print "Wait for daughter card to perform action"
            pcb.receive()
            print "Action performed"

        folder += 1
        if folder >= 3:
            break


if  __name__ =='__main__':
    main()
