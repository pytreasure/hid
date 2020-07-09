import ctypes
import win32gui
import win32print
import win32con
import pyautogui
import sys
import time
import math
import io
import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QBuffer


def QImage_to_PILimage(img):
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_im = Image.open(io.BytesIO(buffer.data()))
    return pil_im


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


# 获取鼠标当前位置的xy坐标
def get_mouse_position():
    x, y = pyautogui.position()
    ratio = get_zoom_ratio()
    return math.floor(x / ratio), math.floor(y / ratio)


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


# 分析区域文字
# 支持简体中文、繁体中文、英语、数字
# lang: chi_sim | chi_tra | eng
# config:
def tesseract(rect, lang=None, config=None):
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    w = screen.grabWindow(rect["hwnd"], rect["x"], rect["y"], rect["w"], rect["h"])
    image = w.toImage()
    # image.save("C:/Users/hunzs/Desktop/tesseract.jpg")
    if config is None:
        if lang == "chi_sim" or lang == "chi_tra":
            config = "-psm 9"
        elif lang == "eng":
            config = "-psm 6"
        elif lang == "num":
            lang = None
            config = "tessedit_char_whitelist=0123456789"
    return pytesseract.image_to_string(
        QImage_to_PILimage(Image.open("C:/Users/hunzs/Desktop/tesseract.jpg")),
        lang=lang,
        config=config
    )


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
                "hwnd": wid,
                "x_start": math.floor(rect[0] / ratio),
                "y_start": math.floor(rect[1] / ratio),
                "x_end": math.floor(rect[2] / ratio),
                "y_end": math.floor(rect[3] / ratio),
            }
