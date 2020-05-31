import win32gui
from PyQt5.QtWidgets import QApplication
import sys
import time

# DPI支持
# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

hwnd_windows = dict()


def all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_windows.update({hwnd: win32gui.GetWindowText(hwnd)})


def get_all_window_items():
    win32gui.EnumWindows(all_hwnd, 0)
    return hwnd_windows.items()


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
        w = screen.grabWindow(wid)
        img = w.toImage()
        img.save(save_dir + title + "_" + str(time.time()) + ".jpg")


shot_all("C:/Users/hunzs/Desktop/py/")
shot_title("Fork 1.46.1.0", "C:/Users/hunzs/Desktop/py/")
