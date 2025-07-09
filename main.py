from src.classes.Screenshot import Screenshot
from src.classes.OCR import OCR
import time
import pyautogui as pag
import regex as re
import keyboard

#Classes
screen_shot = Screenshot("Roblox")
ocr = OCR()

# Constants
fps = 120  # Controls the speed of the loop
pattern = r'\b\d+\.\d+[a-zA-Z]\b|\b\d{1,2}:\d{2}\b'

# Global variables
money_text = None
skip_line_text = None
start_time = time.time()
frames = 0  # Frame counter for FPS calculation
def money_coords() -> tuple | None:
    screen_start_x, screen_start_y = screen_shot.get_window_location()
    left, top, right, bottom = screen_shot.get_client_size(screen_shot.get_window())
    client_width = right - left
    client_height = bottom - top
    screen_width, screen_height = screen_shot.get_window_size()
    x_scale = client_width / screen_width
    y_scale = client_height / screen_height
    top += screen_start_y + int(60 * y_scale)
    bottom = top + int(100 * y_scale)
    left = int(screen_start_x + (client_width//2) - (370 * x_scale))
    right = int(left + (740 * x_scale))
    return (left, top, right, bottom)

def skip_line_coords() -> tuple | None:
    screen_start_x, screen_start_y = screen_shot.get_window_location()
    left, top, right, bottom = screen_shot.get_client_size(screen_shot.get_window())
    client_width = right - left
    client_height = bottom - top
    screen_width, screen_height = screen_shot.get_window_size()
    x_scale = client_width / screen_width
    y_scale = client_height / screen_height
    bottom += screen_start_y - int(95 * y_scale)
    top = bottom - int(125 * y_scale)
    left = int(screen_start_x + (client_width//2) - (385 * x_scale))
    right = int(left + (390 * x_scale))
    return (left, top, right, bottom)

def get_mid_coords(left, top, right, bottom) -> tuple:
    width = right - left
    height = bottom - top
    mid_x = left + (width // 2)
    mid_y = top + (height // 2)
    return (mid_x, mid_y)

def values_from_text(text: str) -> tuple | None:
    if not text:
        return None
    value =  re.findall(pattern, text)[-1] if re.findall(pattern, text) else None
    if not value:
        return None
    elif value[-1].isalpha():
        return (float(value[:-1]), value[-1])
    else:
        return tuple(int(x) for x in value.split(':'))

def update_text(org_value: tuple, image) -> tuple:
    if not image:
        return None
    value = values_from_text(ocr.extract_text(image))
    if value is None:
        return org_value
    else:
        return value

def has_enough_money(value_needed: tuple, value_available: tuple) -> bool:
    if not value_needed or not value_available:
        return False
    elif value_needed[1] == value_available[1] and value_needed[0] <= value_available[0]:
        return True
    elif value_needed[1] > value_available[1]:
        return True
    else:
        return False

def click_button() -> None:
    mid_coords = get_mid_coords(*skip_line_coords())
    pag.click(mid_coords[0], mid_coords[1])

def isTimer(value: tuple) -> bool | None:
    if not value:
        return None
    elif type(value[0]) == int and type(value[1]) == int:
        return True
    else:
        return False
    
def main():
    while keyboard.is_pressed('ctrl+q') is False:
        global frames, start_time, fps, money_text, skip_line_text
        frames += 1
        current_time = time.time()
        elapsed = current_time - start_time
        #time.sleep(1 / fps)  # Control the loop speed
        moneyImage = screen_shot.take_crop_screenshot(money_coords())
        skipLineImage = screen_shot.take_crop_screenshot(skip_line_coords())
        money_text = update_text(money_text, moneyImage)
        skip_line_text = update_text(skip_line_text, skipLineImage)
        if isTimer(skip_line_text):
            if (skip_line_text[0] == 0 and skip_line_text[1] <= 10) or (skip_line_text[0] == 1 and skip_line_text[1] <= 26):
                click_button()
        else:
            if has_enough_money(skip_line_text, money_text):
                click_button()
        if elapsed >= 1.0:  # Every 1 second
            fps = frames / elapsed
            print(f"FPS: {fps:.2f}")
            frames = 0
            start_time = current_time

if __name__ == "__main__":
    main()
