import math
import random
from chip.ch9329 import control
from lib import screen
from scripts.koei_sango import position

screen_ratio = screen.get_zoom_ratio()


def xywh_percent(rect, element):
    x = math.floor(rect["x_start"] + element["x"] / screen_ratio)
    y = math.floor(rect["y_start"] + element["y"] / screen_ratio)
    w = math.floor(element["w"] / screen_ratio)
    h = math.floor(element["h"] / screen_ratio)
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

    # 上来尝试跳动画
    control.mouse_move(xywh_percent(rect, position.center))
    control.mouse_press("LEFT")
    control.mouse_free()

    # 找作者名
    cap_author = xywh_percent(rect, position.author)
    print(cap_author)
    screen.captura({
        "hwnd": rect["hwnd"],
        "x": cap_author["x"], "y": cap_author["y"],
        "w": cap_author["w"], "h": cap_author["h"],
    })

    # 甩一波窗口
    start = xywh_percent(rect, position.title)
    print(start)
    control.mouse_move(start)
    control.mouse_press("LEFT")
    limit = 10
    while limit > 0:
        control.mouse_move({"x": random.randint(0, 2000), "y": random.randint(0, 800)})
        limit -= 1
    control.mouse_move(start)
    control.mouse_free()

