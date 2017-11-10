from uart import UART
from time import sleep
from random import randint


def main():
    con = UART()
    print con.test()
    while True:
	con.write(chr(randint(48, 57)))
        c = con.read()
#        print c
        sleep(0.5)


if __name__ == '__main__':
    main()
