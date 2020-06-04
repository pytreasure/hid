import math
import random
from chip.ch9329 import control
from lib import screen
from scripts.koei_sango import position


def xywh_percent(rect, element):
    rect_w = rect["x_end"] - rect["x_start"]
    rect_h = rect["y_end"] - rect["y_start"]
    x = math.floor(rect["x_start"] + rect_w * element["x"])
    y = math.floor(rect["y_start"] + rect_h * element["y"])
    w = math.floor(rect_w * element["w"]) if element["w"] is None else 0
    h = math.floor(rect_h * element["h"]) if element["h"] is None else 0
    return {"x": x, "y": y, "w": w, "h": h}


def run(com):  # 跑脚本
    control.set_com(com)  # 设置端口
    rect = screen.get_window_rect("圣三国蜀汉传")
    if rect is None:
        return
    print(rect)
    # 上来先释放一波
    control.keyboard_free()
    control.mouse_free()

    #
    start = xywh_percent(rect, position.title)
    print(start)
    control.mouse_move(start)
    control.mouse_press("LEFT")
    limit = 10
    while limit > 0:
        control.mouse_move({"x": random.randint(0, 2000), "y": random.randint(0, 800)})
        limit -= 1
    control.mouse_move(start)
    # 找作者名
    cap_author = xywh_percent(rect, position.author)
    print(cap_author)
    screen.captura({
        "hwnd": rect["hwnd"],
        "x": cap_author["x"], "y": cap_author["y"],
        "w": cap_author["w"], "h": cap_author["h"],
    })

    control.mouse_free()
