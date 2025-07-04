import win32gui
import pyautogui as pag
class Screenshot:
    def __init__(self, window: str):
        self.window_title = window
        self.image = None  # Placeholder for the screenshot image data
    
    def get_window(self):
        hwnd = win32gui.FindWindow(None, self.window_title)
        return hwnd if hwnd else None

    def get_window_size(self, window_id: int):
        rect = win32gui.GetWindowRect(window_id)
        if rect:
            left, top, right, bottom = rect
            return (left, top, right, bottom)
        else:
            return None

    def take_screenshot(self, window_location=None):
        if not window_location:
            left, top, right, bottom = self.get_window_size(self.get_window())
        else:
            left, top, right, bottom = window_location
        self.image = pag.screenshot(region=(left, top, right - left, bottom - top))
        return self.image
    
    def save_screenshot(self, file_path: str):
        if self.image:
            self.image.save(file_path)
        else:
            raise ValueError("No screenshot taken to save.")