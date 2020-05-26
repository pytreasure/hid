# Core code of HID.
# Build commands for HID keyboard and mouse.

import time
from map import keyboard as map_keyboard

hid_com = None


def set_com(which_com):
    global hid_com
    hid_com = which_com


def keyboard(keys, delay):
    global hid_com
    if hid_com is None:
        return
    commands = {

    }
    keys_type = type(keys)
    if keys_type == "string":
        keys_type = 2
    elif keys_type == "number":
        keys = str(keys)
    elif keys_type == "list" or keys_type == "tuple":
        keys_type = 1
    put = bytes([0x57, 0XAB, 0X00, 0X02, 0X08, 0X00, 0X00, 0X04, 0X00, 0X00, 0X00, 0X00, 0X00, 0X10])
    hid_com.write(put)
    time.sleep(delay)


def mouse(keys):
    commands = {

    }
    keys_type = type(keys)
    if keys_type == "number":
        keys_type = str(keys_type)
    if keys_type == "list" or keys_type == "tuple":
        keys_type = 1
    elif keys_type == "string":
        keys_type = 2
    else:
        return ()
