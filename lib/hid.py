# Core code of HID.
# Build commands for HID keyboard and mouse.

import time
import random
from lib import map

hid_com = None

hid_command_keys = [
    "LEFT_CTRL",
    "RIGHT_CTRL",
    "LEFT_SHIFT"
    "RIGHT_SHIFT",
    "LEFT_ALT",
    "RIGHT_ALT",
    "LEFT_WIN",
    "RIGHT_WIN"
]


def set_com(which_com):
    global hid_com
    hid_com = which_com


# keys 只支持Command键 + 6个普通按键组合
# delay 释放延时
def keyboard(keys, delay):
    global hid_com

    if hid_com is None:
        return

    target_keys = {
        "command": None,
        "normal": []
    }

    keys_type = type(keys)
    if keys_type == str:
        keys = str.upper(keys)
        if keys in hid_command_keys:
            target_keys["command"] = map.keyboard[keys]
        else:
            target_keys["normal"].append(map.keyboard[keys])
    elif keys_type == int:
        keys = str.upper(str(keys))
        if keys in hid_command_keys:
            target_keys["command"] = map.keyboard[keys]
        else:
            target_keys["normal"].append(map.keyboard[keys])
    elif keys_type == list or keys_type == tuple:
        for v in keys:
            if type(v) == int:
                v = str(v)
            v = str.upper(v)
            if v in hid_command_keys:
                target_keys["command"] = map.keyboard[v]
            else:
                target_keys["normal"].append(map.keyboard[v])

    # 固有头部
    put = [0X57, 0XAB, 0X00, 0X02, 0X08]
    # 命令键组合判断
    if target_keys["command"] is not None:
        put.append(target_keys["command"])
    else:
        put.append(0X00)
    # 这一位必须是 0X00
    put.append(0X00)
    # 最多 6 个组合键
    for i in range(0, 6):
        try:
            put.append(target_keys["normal"][i])
        except TypeError:
            put.append(0X00)
        except IndexError:
            put.append(0X00)
    # 收尾
    put.append(0X10)
    # 按下组合键
    hid_com.write(bytes(put))
    if delay < 10:
        delay = random.randint(10, 100)
    delay = round(0.001 * delay, 2)
    time.sleep(delay)
    # 释放按键
    hid_com.write(bytes([0X57, 0XAB, 0X00, 0X02, 0X08, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X0C]))
    time.sleep(0.01)


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
