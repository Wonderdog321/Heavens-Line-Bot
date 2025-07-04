from src.classes.Screenshot import Screenshot
screen_shot = Screenshot("Roblox")
top_adjust = 40
adjust = 10
scale = 0.33

def get_adjusted_coordinates():
    left, top, right, bottom = screen_shot.get_window_size(screen_shot.get_window())
    top += top_adjust
    left += adjust
    right -= adjust
    bottom -= adjust
    width = right - left
    left += int(width * scale)
    right -= int(width * scale)
    return (left, top, right, bottom)

def main():
    screen_shot.take_screenshot(get_adjusted_coordinates())
    screen_shot.save_screenshot(".\\src\\imgs\\screenshot.png")
if __name__ == "__main__":
    main()
