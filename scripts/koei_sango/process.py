import math
import random
import time
from chip.ch9329 import control
from lib import screen
from scripts.koei_sango import position

screen_ratio = screen.get_zoom_ratio()
print(screen_ratio)


# 屏幕窗口偏移
def xy_offset(rect, element):
    rect_w = rect["x_end"] - rect["x_start"]
    rect_h = rect["y_end"] - rect["y_start"]
    x = math.floor(rect["x_start"] + rect_w * element["x"])
    y = math.floor(rect["y_start"] + rect_h * element["y"])
    return {"x": x, "y": y}


# 窗口内相对区域截取
def xywh_cap(element):
    x = math.floor(element["x"] / screen_ratio)
    y = math.floor(element["y"] / screen_ratio)
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
    offset = xy_offset(rect, position.center)
    control.mouse_move(offset)
    control.mouse_press("LEFT")
    control.mouse_free()
    time.sleep(1)

    # 按点按钮开心下
    control.mouse_move(xy_offset(rect, position.main_btn3))
    control.mouse_press("LEFT")
    control.mouse_free()
    time.sleep(0.2)
    control.keyboard("ESC", 50)

    control.mouse_move(xy_offset(rect, position.main_btn2))
    control.mouse_press("LEFT")
    control.mouse_free()
    time.sleep(0.2)
    control.mouse_move(xy_offset(rect, position.main_btn2_close))
    control.mouse_press("LEFT")
    control.mouse_free()

    # 甩一波窗口
    start = xy_offset(rect, position.title)
    control.mouse_move(start)
    control.mouse_press("LEFT")
    limit = 10
    while limit > 0:
        control.mouse_move({"x": random.randint(0, 2000), "y": random.randint(0, 800)})
        limit -= 1
    control.mouse_move(start)
    control.mouse_free()

    # 找作者名
    # cap_author = xywh_cap(position.author)
    # print(cap_author)
    # screen.tesseract({
    #     "hwnd": rect["hwnd"],
    #     "x": cap_author["x"], "y": cap_author["y"],
    #     "w": cap_author["w"], "h": cap_author["h"],
    # })

    # 退出
    control.mouse_move(xy_offset(rect, position.main_btn4))
    control.mouse_press("LEFT")
    control.mouse_free()
