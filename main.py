#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import tkinter
from lib import serialer


def main():
    try:
        port = sys.argv[1]
        script = sys.argv[2]
    except IndexError:
        print("You command maybe: python main.py com1 pop_kart")
        sys.exit()

    tk = tkinter.Tk()
    print(tk.winfo_screenwidth())
    print(tk.winfo_screenheight())
    tk.destroy()

    # serialer.init(port, script)


if __name__ == "__main__":
    main()
