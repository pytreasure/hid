#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from lib import serialer


def main():
    try:
        port = sys.argv[1]
    except IndexError:
        print("You command maybe: python main.py com1 9600 1")
        sys.exit()
    try:
        baud_rate = int(sys.argv[2])
    except IndexError:
        baud_rate = 9600
    try:
        timeout = int(sys.argv[3])
    except IndexError:
        timeout = 1
    serialer.init(port, baud_rate, timeout)


if __name__ == "__main__":
    main()
