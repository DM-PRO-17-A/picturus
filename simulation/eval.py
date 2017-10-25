# Open images
from PIL import Image
# Contains functions for using the QNN
from gtsrb import *
from eval_daughter_card import Daughter_Card
# For simulation purposes
from time import sleep
from random import randrange
# To get all files from a directory
from os import walk
import numpy as np
from operator import add

def open_images(pics):
    return map(lambda p: (p, prepare_gtsrb(Image.open(p))), pics)

# Paths to images
path = ["evaluate_test/res_images/"]

pics = []
for i in range(len(path)):
    p = []
    thispath = path[i]
    for (dirpath, dirnames, filenames) in walk(thispath):
        for filename in filenames:
            if '.jpg' in filename:
                p.append(thispath+filename)
        p = sorted(p, key=lambda x: int(x.split('-')[-1].split('.')[0]))
        pics.append(p)
        break

pcb = Daughter_Card()

for i in range(len(pics)):
    pics[i] = open_images(pics[i])
    for p in pics[i]:
        res = gtsrb_predict(p[1])
        pcb.send(res)

m_weights = [0,0,0,0,0, 1 ,0,0,0,0,0] # no weights

for key in pcb.subset_probs.keys():
    temp = pcb.subset_probs[key]
    for i in range(len(pcb.subset_probs[key])):
        value = pcb.subset_probs[key][i]
        if i > 5 and i < len(pcb.subset_probs[key])-5:
            temp[i] = np.dot(m_weights,pcb.subset_probs[key][i-5:i+6])
            #if [temp2[k] > 90 for k in range(len(temp2))]:
            #    value += np.dot(temp2, h_weights)*somevalue
    pcb.subset_probs[key] = map(add, pcb.subset_probs[key], temp)
    print key + ': ' + str(sum(pcb.subset_probs[key])/len(pcb.subset_probs[key])) + ' \n'
    

