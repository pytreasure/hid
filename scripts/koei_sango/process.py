import math
import random
import time
from chip.ch9329 import control
from lib import screen
from scripts.koei_sango import position


class Run:

    # 屏幕窗口偏移
    @staticmethod
    def xy_offset(rect, element):
        rect_w = rect["x_end"] - rect["x_start"]
        rect_h = rect["y_end"] - rect["y_start"]
        x = math.floor(rect["x_start"] + rect_w * element["x"])
        y = math.floor(rect["y_start"] + rect_h * element["y"])
        return {"x": x, "y": y}

    # 窗口内相对区域截取
    def xywh_cap(self, element):
        x = math.floor(element["x"] / self.screen_ratio)
        y = math.floor(element["y"] / self.screen_ratio)
        w = math.floor(element["w"] / self.screen_ratio)
        h = math.floor(element["h"] / self.screen_ratio)
        return {"x": x, "y": y, "w": w, "h": h}

    def __init__(self, com):
        self.screen_ratio = screen.get_zoom_ratio()

        c = control.Control(com)  # 设置端口
        rect = screen.get_window_rect("圣三国蜀汉传")
        if rect is None:
            return
        print(rect)
        # 上来先释放一波
        c.keyboard_free()
        c.mouse_free()

        # 找作者名
        cap_author = self.xywh_cap(position.author)
        print(cap_author)
        screen.tesseract({
            "hwnd": rect["hwnd"],
            "x": cap_author["x"], "y": cap_author["y"],
            "w": cap_author["w"], "h": cap_author["h"],
        })

        return

        # 上来尝试跳动画
        offset = self.xy_offset(rect, position.center)
        c.mouse_move(offset)
        c.mouse_press("LEFT")
        c.mouse_free()
        time.sleep(1)

        # 按点按钮开心下
        c.mouse_move(xy_offset(rect, position.main_btn3))
        c.mouse_press("LEFT")
        c.mouse_free()
        time.sleep(0.2)
        c.keyboard("ESC", 50)

        c.mouse_move(xy_offset(rect, position.main_btn2))
        c.mouse_press("LEFT")
        c.mouse_free()
        time.sleep(0.2)
        c.mouse_move(xy_offset(rect, position.main_btn2_close))
        c.mouse_press("LEFT")
        c.mouse_free()

        # 甩一波窗口
        start = xy_offset(rect, position.title)
        c.mouse_move(start)
        c.mouse_press("LEFT")
        limit = 10
        while limit > 0:
            c.mouse_move({"x": random.randint(0, 2000), "y": random.randint(0, 800)})
            limit -= 1
        c.mouse_move(start)
        c.mouse_free()

        # 找作者名
        # cap_author = xywh_cap(position.author)
        # print(cap_author)
        # screen.tesseract({
        #     "hwnd": rect["hwnd"],
        #     "x": cap_author["x"], "y": cap_author["y"],
        #     "w": cap_author["w"], "h": cap_author["h"],
        # })

        # 退出
        c.mouse_move(xy_offset(rect, position.main_btn4))
        c.mouse_press("LEFT")
        c.mouse_free()
