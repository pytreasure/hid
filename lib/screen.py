import ctypes
import win32api
import win32gui
import win32print
import win32con
from PyQt5.QtWidgets import QApplication
import sys
import time
import math


# DPI支持
# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)


# 获取屏幕分辨率缩放比例
def get_zoom_ratio():
    hdc = win32gui.GetDC(0)
    dpi = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    return round(dpi / 96, 2)


# 获取真实的分辨率
def get_real_resolution():
    hdc = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
    return w, h


# 获取缩放后的分辨率
def get_zoom_resolution():
    real = get_real_resolution()
    ratio = get_zoom_ratio()
    return math.floor(real[0] / ratio), math.floor(real[1] / ratio)


def all_hwnd(hwnd, mouse):
    hwnd_windows = dict()
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_windows.update({hwnd: win32gui.GetWindowText(hwnd)})
    return hwnd_windows


def get_all_window_items():
    return win32gui.EnumWindows(all_hwnd, 0).items()


# 把屏幕上所有窗口截图
# 最小化时截图黑色
def shot_all(save_dir):
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    for wid, title in get_all_window_items():
        if title != "":
            w = screen.grabWindow(wid)
            img = w.toImage()
            img.save(save_dir + title + "_" + str(time.time()) + ".jpg")


# 根据窗口title截图
# 最小化时截图黑色
def shot_title(title, save_dir):
    if title != "":
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        wid = win32gui.FindWindow(None, title)
        if wid > 0:
            w = screen.grabWindow(wid)
            img = w.toImage()
            img.save(save_dir + title + "_" + str(time.time()) + ".jpg")


# 去除边框毛玻璃的区域
def get_window_real_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        f(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(9), ctypes.byref(rect), ctypes.sizeof(rect))
        return rect.left, rect.top, rect.right, rect.bottom


# 根据title获取窗口区域
# 坐标由左上角到右下角
def get_window_rect(title):
    if title != "":
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        wid = win32gui.FindWindow(None, title)
        if wid > 0:
            rect = win32gui.GetWindowRect(wid)
            # rect = get_window_real_rect(wid)
            ratio = get_zoom_ratio()
            if rect[0] < 0 and rect[1] < 0 and rect[2] < 0 and rect[3] < 0:
                print("window minimized")
                return
            return {
                "x_start": math.floor(rect[0] / ratio),
                "y_start": math.floor(rect[1] / ratio),
                "x_end": math.floor(rect[2] / ratio),
                "y_end": math.floor(rect[3] / ratio),
            }
