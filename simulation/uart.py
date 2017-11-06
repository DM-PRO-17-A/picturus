"""Communication class to replace daughter_card.py
   Will connect the Pynq to the EFM32 to send and receive chars"""

import serial


class UART:

    # Set up serial communication
    # python -m serial.tools.list_ports
    # https://electrosome.com/uart-raspberry-pi-python/
    # https://groups.google.com/forum/#!topic/pynq_project/pkGXZN4RED0
    ser = serial.Serial('/dev/ttyAMA0') # ttyAMA0 is UART for RaspPi
    # ser = serial.Serial("/dev/ttyPS0", baudrate=115200, timeout=3.0) This might be the correct way for the Pynq?
    ser.baudrate = 19200 # Replace with actual rate


    def read(self):
        return self.ser.read() # Implicitly one byte

    def write(self, c):
        self.ser.write(c)
