import numpy as np
import pickle
from QNN.layers import *


qnn = pickle.load(open("gtsrb-w1a1-fc.pickle", "rb"))


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
