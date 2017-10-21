# Open images
from PIL import Image
# Contains functions for using the QNN
from gtsrb import *
from test_daughter_card import Daughter_Card
# For simulation purposes
from time import sleep
from random import randrange
# To get all files from a directory
from os import walk

def open_images(pics):
    return map(lambda p: (p, prepare_gtsrb(Image.open(p))), pics)

# Paths to images
path0 = "tests/left/"
path1 = "tests/right/"
path2 = "tests/stop/"
path3 = "tests/speed/20/"
path4 = "tests/speed/30/"
path5 = "tests/speed/50/"
path6 = "tests/speed/60/"
path7 = "tests/speed/70/"
path8 = "tests/speed/80/"
path9 = "tests/speed/100/"
path10 = "tests/speed/120/"
path = [path0, path1, path2, path3, path4, path5, path6, path7, path8, path9,path10]

pics = []

sign_type = ['left','right','stop','20','30','50','60','70','80','100','120']

for i in range(len(path)):
    p = []
    thispath = path[i]
    for (dirpath, dirnames, filenames) in walk(thispath):
        for filename in filenames:
            if '.ppm' in filename:
                p.append(thispath+filename)
        pics.append(p)
        break

pcb = Daughter_Card()

for i in range(len(pics)):
    pics[i] = open_images(pics[i])

for i in range(len(pics)):
    filename = 'test_results/'+sign_type[i]+'_results.txt'
    f = open(filename, 'w')
    f.write('Results for ' + sign_type[i] + '-signs: \n\n')
    f.close()
    for p in pics[i]:
        f = open(filename, 'a')
        f.write('\t Results for ' + str(p[0]) + ':\n')
        f.close()
        res = gtsrb_predict(p[1])
        pcb.send(res, filename)
    

