from uart import UART


def main():
    con = UART()
    print con.test()


if __name__ == '__main__':
    main()
