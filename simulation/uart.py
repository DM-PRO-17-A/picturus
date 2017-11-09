"""Communication class to replace daughter_card.py

   Will connect the Pynq to the EFM32 to send and receive chars"""

import serial


class UART(object):

    # Set up serial communication
    # python -m serial.tools.list_ports
    # https://electrosome.com/uart-raspberry-pi-python/
    # https://groups.google.com/forum/#!topic/pynq_project/pkGXZN4RED0

    
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyPS0", baudrate=115200, timeout=3.0) # This might be the correct way for the Pynq?
        print "Initialised"
    

    def read(self):
        c = self.ser.read() # Implicitly one byte
        print c
        return c

    
    def write(self, c):
        print c
        self.ser.write(c)


    def test(self):
        return "Howdy!"
