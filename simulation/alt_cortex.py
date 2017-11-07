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
    i = np.argmax(res)
    return gtsrb_classes[i], res[i]

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


valid_classes = ['50 Km/h', '70 Km/h', '100 Km/h', 'Stop', 'No entry for vehicular traffic', 'Turn right ahead', 'Turn left ahead', 'No sign']
# Weights to prioritise the signs we use
# Just ignoring the others leads to very wrong behaviour

averages = {'50 Km/h':          [0.0,0.0,0.0,0.0], 
            '70 Km/h':          [0.0,0.0,0.0,0.0], 
            '100 Km/h':         [0.0,0.0,0.0,0.0], 
            'Stop':             [0.0,0.0,0.0,0.0], 
            'No entry for vehicular traffic': [0.0,0.0,0.0,0.0], 
            'Turn right ahead': [0.0,0.0,0.0,0.0], 
            'Turn left ahead':  [0.0,0.0,0.0,0.0], 
            'No sign':          [0.0,0.0,0.0,0.0]}

path = "pics/out/"
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
    average = [[]]*43
    av = [0]*43
    count = 0
    memory = ['No sign', 'No sign', 'No sign', 'No sign', 'No sign', 'No sign']
    #memory = ['No sign', 'No sign', 'No sign', 'No sign', 'No sign']
    #memory = ['No sign', 'No sign', 'No sign', 'No sign']
    memory_prob = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #memory_prob = [0.0, 0.0, 0.0, 0.0, 0.0]
    #memory_prob = [0.0, 0.0, 0.0, 0.0]

    while True:
        print "Drive"
        sleep(1)

        # Iterate cycle one step, i.e. take another picture and process it
        # Call camera script
        # Get array of the images to use next
        ########################################
        # This whole part will be replaced with a single call to a script
        print "\n Get next frame"
        # pics = ???
        # fsm = fsm_states[1]

        print "Analyse frame with QNN"
        for n in xrange(3):
            try:
                pic = pics.pop(0)
            except IndexError:
                print "No more input"
                return -1
            res = gtsrb_predict(pic[1])
            sign, prob = get_most_probable_sign(res)
            if sign not in valid_classes:
                sign = 'No sign'
                prob = 0.3
            averages[sign].pop(0)
            averages[sign].append(prob)
            memory.pop(0)
            memory.append(sign)
            memory_prob.pop(0)
            memory_prob.append(prob)
                    
        max_prob = [prob]
        max_sign = [sign]
        l = 1
        p_a = 0
        p_b = 0

        for key in averages.keys():
            if sum(averages[key]) > p_a:
                p_a = sum(averages[key])
                l = len(averages[key])
                s = key
        p = p_a/l
        max_prob.append(p)
        max_sign.append(s)

        max_prob.append(max(memory_prob))
        mem_max = max(memory_prob)
        index = memory_prob.index(mem_max)
        max_sign.append(memory[index])

        prob = max(max_prob)
        index = max_prob.index(prob)
        sign = max_sign[index]
        print sign + ': ' + str(prob*100) + '%'

        # Send UART signal to PCB
        #if prob > 0.75:
        #    fsm_states = fsm_states[pcb.send(signals.get(sign, 'f'), prob)]
        #else:
        #    fsm_states = fsm_states[pcb.send(signals['Drive'], -1)]
        #    
        # if fsm != "driving":
        print "Wait for daughter card to perform action"
        pcb.receive()
        print "Action performed"
        


if  __name__ =='__main__':
    main()
