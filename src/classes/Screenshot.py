import win32gui
import win32api
import win32con
from mss import mss, tools
class Screenshot:
    def __init__(self, window: str):
        self.window_title = window
        self.image = None  # Placeholder for the screenshot image data
    
    def get_window(self):
        hwnd = win32gui.FindWindow(None, self.window_title)
        return hwnd if hwnd else None

    def get_window_size(self):
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        return (screen_width, screen_height)

    def get_client_size(self, window_id: int):
        rect = win32gui.GetClientRect(window_id)
        if rect:
            left, top, right, bottom = rect
            return (left, top, right, bottom)
        else:
            return None

    def get_window_location(self):
        hwnd = self.get_window()
        return win32gui.ClientToScreen(hwnd, (0, 0)) if hwnd else None
    
    def take_full_screenshot(self, window_location=None):
        sct = mss()
        if not window_location:
            left, top, right, bottom = self.get_window_size(self.get_window())
        else:
            left, top, right, bottom = window_location
        region = (left, top, right - left, bottom - top)
        self.image = sct.grab(region)
        return self.image
    
    def take_crop_screenshot(self, window_location=None):
        sct = mss()
        left, top, right, bottom = window_location
        region = (left, top, right, bottom)
        self.image = sct.grab(region)
        return self.image
    
    def save_screenshot(self, file_path: str):
        if self.image:
            tools.to_png(self.image.rgb, self.image.size, output=file_path)
        else:
            raise ValueError("No screenshot taken to save.")