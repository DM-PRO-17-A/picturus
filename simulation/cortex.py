from PIL import Image
from gtsrb import *
import daughter_card as pcb
from time import sleep
# Maybe install termcolor for colored output?
# from termcolor import colored

fsm_states = ["driving", "determine sign", "keep driving", "execute sign", "receive interrupt"]
fsm = fsm_states[0]


def open_images(pics):
    return map(lambda p: (p, prepare_gtsrb(Image.open(p))), pics)


# TODO: give images more meaningful file names
test_case_normal_signs = open_images(("pics/50.jpg", "pics/left.jpg", "pics/right.jpg", "pics/stop.jpg"))
test_case_zoom = open_images(("test_pics/stoptest.jpg", "test_pics/stoptest1.jpg", "test_pics/stoptest2.jpg", "test_pics/stoptest3.jpg"))
test_case_partially_covered = open_images(("test_pics/stop75.jpg", "test_pics/stop85.jpg", "test_pics/stop90.jpg", "test_pics/stop95.jpg"))
tests = (test_case_normal_signs, test_case_zoom, test_case_partially_covered)


# TODO: improve readability of output
for pics in tests:
    for pic in pics:
        print pic[0]
        gtsrb_predict(pic[1])


while True:
    print "Drive"
    sleep(3)
    print "Get random picture (currently just one picture)"
    fsm = fsm_states[1]
    pic = prepare_gtsrb(Image.open("pics/50.jpg"))
    print "Send to QNN"
    # Dependent on what the QNN says, set fsm to either 2 or 3
    sign = gtsrb_predict(pic)
    print "Send conclusion to daughter card"
    pcb.send(sign)
    fsm = fsm_states[4]
    print "Sign action carried through"
    pcb.receive()
    print "Keep driving"
    break
