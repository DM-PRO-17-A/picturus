from uart import UART
from time import sleep
from random import randint


def main():
    con = UART()
    while True:
	con.write(randint(0, 7))
        # c = con.read()
#        print c
        sleep(0.5)


if __name__ == '__main__':
    main()
