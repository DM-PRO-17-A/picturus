import numpy as np
import pickle
from QNN.layers import *
# TODO: find a way to print pretty colors in predict
# Maybe install termcolor?
# from termcolor import colored


qnn = pickle.load(open("gtsrb-w1a1.pickle", "rb"))


gtsrb_classes = ['20 Km/h', '30 Km/h', '50 Km/h', '60 Km/h', '70 Km/h', '80 Km/h',
                 'End 80 Km/h', '100 Km/h', '120 Km/h', 'No overtaking',
                 'No overtaking for large trucks', 'Priority crossroad', 'Priority road',
                 'Give way', 'Stop', 'No vehicles',
                 'Prohibited for vehicles with a permitted gross weight over 3.5t including their trailers, and for tractors except passenger cars and buses',
                 'No entry for vehicular traffic', 'Danger Ahead', 'Bend to left',
                 'Bend to right', 'Double bend (first to left)', 'Uneven road',
                 'Road slippery when wet or dirty', 'Road narrows (right)', 'Road works',
                 'Traffic signals', 'Pedestrians in road ahead', 'Children crossing ahead',
                 'Bicycles prohibited', 'Risk of snow or ice', 'Wild animals',
                 'End of all speed and overtaking restrictions', 'Turn right ahead',
                 'Turn left ahead', 'Ahead only', 'Ahead or right only',
                 'Ahead or left only', 'Pass by on right', 'Pass by on left', 'Roundabout',
                 'End of no-overtaking zone',
                 'End of no-overtaking zone for vehicles with a permitted gross weight over 3.5t including their trailers, and for tractors except passenger cars and buses']


def prepare_gtsrb(img):
    # make sure the image is the size expected by the network
    img = img.resize((32, 32))
    # convert to numpy array
    img = np.asarray(img)
    # we need the data layout to be (channels, rows, columns)
    # but it comes in (rows, columns, channels) format, so we
    # need to transpose the axes:
    img = img.transpose((2, 0, 1))
    # finally, our network is trained with BGR instead of RGB images,
    # so we need to invert the order of channels in the channel axis:
    img = img[::-1, :, :]
    return img


def gtsrb_predict(img):
    # get the predictions array
    res = predict(qnn, img)
    return res
    # return the index of the largest prediction, then use the
    # classes array to map to a human-readable string
    # winner_ind = np.argmax(res)
    # winner_class = gtsrb_classes[winner_ind]
    # res[winner_ind] -= 1
    # second_ind = np.argmax(res)
    # second_class = gtsrb_classes[second_ind]

    # the sum of the output values add up to 1 due to softmax,
    # so we can interpret them as probabilities
    # winner_prob = 100 * res[winner_ind] + 100
    # second_prob = 100 * res[second_ind]
    # print("The QNN predicts this is a %s sign with %f percent probability" % (winner_class, winner_prob))
    # print("It could also be a %s sign with %f percent probability" %
            # (second_class, second_prob))
    return winner_class
