"""Communication class to replace daughter_card.py

   Will connect the Pynq to the EFM32 to send and receive chars"""

import serial
import struct


class UART(object):

    # Set up serial communication
    # python -m serial.tools.list_ports
    # https://electrosome.com/uart-raspberry-pi-python/
    # https://groups.google.com/forum/#!topic/pynq_project/pkGXZN4RED0

    # ser = serial.Serial('/dev/ttyAMA0') # ttyAMA0 is UART for RaspPi
    # ser.baudrate = 19200 # Replace with actual rate

    # For the USB-UART cable:
    #    Yellow: input
    #    Orange: output
    #    Black:  gnd
    
    def __init__(self):
        # self.ser = serial.Serial("/dev/ttyUSB2", baudrate=115200, timeout=3.0) # This might be the correct way for the Pynq?
        print "Initialised"
    

    def read(self):
        c = self.ser.read() # Implicitly one byte
        print "Receive: " + str(c)
        return c

    
    def write(self, c):
        self.ser = serial.Serial("/dev/ttyUSB0", baudrate=115200) # This might be the correct way for the Pynq?
        
        # print "Send: " + str(c)
        self.ser.write(ord('f'))
        self.ser.close()
