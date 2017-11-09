from uart import UART
from time import sleep


def main():
    con = UART()
    print con.test()
    while True:
        c = con.read()
        print c
        sleep(0.5)


if __name__ == '__main__':
    main()
