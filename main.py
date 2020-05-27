#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from lib import serialer


def main():
    try:
        port = sys.argv[1]
        script = sys.argv[2]
    except IndexError:
        print("You command maybe: python main.py com1 pop_kart")
        sys.exit()
    serialer.init(port, script)


if __name__ == "__main__":
    main()
