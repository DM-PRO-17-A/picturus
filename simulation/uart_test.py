'''
No longer UART. Just pin communication
'''


from time import sleep
from pin_signal import Pins


def main():
    con = Pins()
    # while True:
        # c = con.read()
        # print c
        # sleep(0.5)
    print str(con.read())
    print con.write('f')
        

if __name__ == '__main__':
    main()
