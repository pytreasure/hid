# Core code of HID.
# Build commands for HID keyboard and mouse.

from chip.ch9329 import control
from lib import screen


class Run:
    def __init__(self, com):
        self.screen_ratio = screen.get_zoom_ratio()
        print(self.screen_ratio)

        c = control.Control(com)  # 设置端口
        rect = screen.get_window_rect("跑跑卡丁车")
        if rect is None:
            return
        print(rect)
        