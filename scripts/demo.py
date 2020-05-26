# Core code of HID.
# Build commands for HID keyboard and mouse.

import time
from lib import hid


def run(com):  # 跑脚本
    hid.set_com(com)  # 设置端口
    while True:  # 死循环
        hid.keyboard("0", 0)
