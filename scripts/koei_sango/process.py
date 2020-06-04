import math
from chip.ch9329 import control
from lib import screen
from scripts.koei_sango import position


def xy_percent(rect, element):
    x = math.floor(rect["x_start"] + (rect["x_end"] - rect["x_start"]) * element["x"])
    y = math.floor(rect["y_start"] + (rect["y_end"] - rect["y_start"]) * element["y"])
    return {"x": x, "y": y}


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
    control.mouse_move(xy_percent(rect, position.bar))
    control.mouse_press("LEFT")
    control.mouse_move({"x": 100, "y": 100})
    control.mouse_free()
