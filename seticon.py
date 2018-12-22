import atexit
import win32con
import win32gui
def set_icon(window, icon_path):
    if not win32gui.IsWindowVisible(int(window.winfo_id())):
        window.wait_visibility(window)
    hwnd = win32gui.GetParent(int(window.winfo_id()))
    icon = win32gui.LoadImage(0, icon_path, win32con.IMAGE_ICON, 0, 0,
                              win32con.LR_DEFAULTSIZE |
                              win32con.LR_LOADFROMFILE)
    win32gui.SendMessage(hwnd, win32con.WM_SETICON,
                         win32con.ICON_BIG, icon)
    win32gui.SendMessage(hwnd, win32con.WM_SETICON,
                         win32con.ICON_SMALL, icon)
    atexit.register(destroy_icon, icon)

def destroy_icon(icon):
    win32gui.DestroyIcon(icon)