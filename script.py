# Core code of HID.
# Build commands for HID keyboard and mouse.

import time
import hid


def run(com):  # 跑脚本
    hid.set_com(com) # 设置端口
    while True:  # 死循环
        time.sleep(1)  # 设置发送间隔时间
        hid.keyboard(["A"])
