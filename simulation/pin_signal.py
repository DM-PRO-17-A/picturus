''' 
Communication between Pynq and EFM32 via pins
No UART, no serial stuff. Pins.
Code only works on Pynq
'''


from pynq import Overlay
from pynq.iop import Arduino_IO

class Pins(object):
    def __init__():
        out_pins = [Arduino_IO(3, 0, 'out'),
                    Arduino_IO(3, 1, 'out'),
                    Arduino_IO(3, 2, 'out'),
                    Arduino_IO(3, 3, 'out')]
        in_pins = [Arduino_IO(3, 4, 'in'),
                   Arduino_IO(3, 5, 'in')]

        signals = {'f':[1, 0, 0, 0],
                   'r':[1, 0, 0, 1],
                   'l':[1, 0, 1, 0],
                   's':[1, 0, 1, 1],
                   'u':[1, 1, 0, 0],
                   '5':[1, 1, 0, 1],
                   '7':[1, 1, 1, 0],
                   '1':[1, 1, 1, 1]}
        

    def read():
        if in_pins[0].read() == 1:
            if in_pins[0].read() == 1:
                return 'x'
            else:
                return '0'
        else:
            return '-1'

        
    def write(c):
        for i in xrange(len(out_pins)):
            out_pins[i].write(signals[c][i])
        return signals[c]
