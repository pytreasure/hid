# Core code of HID.
# Build commands for HID keyboard and mouse.

from chip.ch9329 import control
from lib import screen


def run(com):  # 跑脚本
    control.set_com(com)  # 设置端口
    rect = screen.get_window_rect("圣三国蜀汉传")
    print(rect)
    # # 上来先释放一波
    # hid.keyboard_free()
    # hid.mouse_free()
    # once = 10
    # while True:  # 死循环
    #     once -= 1
    #     if once < 0:
    #         break
    #     hid.keyboard("UP", 0)
