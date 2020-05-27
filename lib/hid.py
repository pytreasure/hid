# Core code of HID.
# Build commands for HID keyboard and mouse.

import time
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


# [累加和]收尾
# 关于SUM累加和的理解：SUM = HEAD+ADDR+CMD+LEN+DATA
# 如鼠标释放: 57 AB 00 02 08 00 00 00 00 00 00 00 00 0C
# SUM=57+AB+2+8=10C，然后只取低位十六进制数0C
def get_tail_low(put):
    tail_sum = 0x00
    for i in put:
        tail_sum += i
    _, tail_low = divmod(tail_sum, 0x100)
    return tail_low


# 释放键盘
def keyboard_free():
    global hid_com
    hid_com.write(bytes([0x57, 0xAB, 0x00, 0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C]))
    time.sleep(0.075)


# 释放鼠标
def mouse_free():
    global hid_com
    hid_com.write(bytes([0x57, 0xAB, 0x00, 0x05, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D]))
    time.sleep(0.075)


# keys 只支持Command键 + 6个普通按键组合
# delay 毫秒，释放延时
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
    put = [0x57, 0xAB, 0x00, 0x02, 0x08]
    # 命令键组合判断
    if target_keys["command"] is not None:
        put.append(target_keys["command"])
    else:
        put.append(0x00)
    # 这一位必须是 0x00
    put.append(0x00)
    # 最多 6 个组合键
    for i in range(0, 6):
        try:
            put.append(target_keys["normal"][i])
        except TypeError:
            put.append(0x00)
        except IndexError:
            put.append(0x00)
    # [累加和]收尾
    put.append(get_tail_low(put))
    # 按下组合键
    hid_com.write(bytes(put))
    if delay > 0:
        time.sleep(0.001 * delay)
    keyboard_free()


# keyboard 的拓展,支持一个句子
def word(words, delay):
    for k in words:
        keyboard(k, delay)


def mouse(move_type, button, x, y, delay):
    # 固有头部
    if move_type == "A":  # absolute
        put = [0x57, 0xAB, 0x00, 0x05, 0x05, 0x01]
    elif move_type == "R":  # relation
        put = [0x57, 0xAB, 0x00, 0x04, 0x07, 0x02]
    else:
        return
    # 哪个按键
    if button is None:
        put.append(0x00)
    else:
        put.append(map.mouse[button])
    # 不同的移动附加不同的数据
    if move_type == "absolute":
        put.append(0)  # x坐标低位
        put.append(0)  # x坐标高位
        put.append(0)  # y坐标低位
        put.append(0)  # y坐标高位
    elif move_type == "relation":
        put.append(0)  #
        put.append(0)
    put.append(0x00)
    # 最多 6 个组合键
    for i in range(0, 6):
        try:
            put.append(target_keys["normal"][i])
        except TypeError:
            put.append(0x00)
        except IndexError:
            put.append(0x00)
    # [累加和]收尾
    put.append(get_tail_low(put))
