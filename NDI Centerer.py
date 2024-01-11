import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
from io import BytesIO
import cv2
import numpy as np
from PIL import Image

def resize_window(title, width, height):
    window = gw.getWindowsWithTitle(title)
    if window:
        window = window[0]
        window.resizeTo(width, height)
    else:
        print(f"No window found with title: {title}")

app_title = 'NDI'

resize_option = input("Do you want to resize the window? (y/n): ").lower()

if resize_option == 'y':
    width = int(input("Enter the width in pixels: "))
    height = int(input("Enter the height in pixels: "))
    resize_window(app_title, width, height)

reference_image = Image.open("ndi_region_reference.png")

app_window = gw.getWindowsWithTitle(app_title)

if app_window:
    app_window = app_window[0]  

    screenshot_before_full = ImageGrab.grab()

    screen_width, screen_height = pyautogui.size()

    window_width, window_height = app_window.width, app_window.height

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2 - 12  

    app_window.moveTo(x_position, y_position)

    screenshot_after_full = ImageGrab.grab()

    pyautogui.mouseDown(x=x_position + 1, y=y_position + 1)  
    pyautogui.mouseUp()

    screenshot_before = screenshot_before_full.crop((x_position, y_position, x_position + window_width, y_position + window_height))
    screenshot_after = screenshot_after_full.crop((x_position, y_position, x_position + window_width, y_position + window_height))

    screenshot_before_cv2 = cv2.cvtColor(np.array(screenshot_before), cv2.COLOR_RGB2BGR)
    screenshot_after_cv2 = cv2.cvtColor(np.array(screenshot_after), cv2.COLOR_RGB2BGR)

    difference = cv2.absdiff(screenshot_before_cv2, screenshot_after_cv2)

    _, thresholded = cv2.threshold(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY), 30, 255, cv2.THRESH_BINARY)

    green_color = (0, 255, 0)

    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_count = 0 
    for contour in contours:
        if cv2.contourArea(contour) > 10:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(screenshot_after_cv2, (x, y), (x + w, y + h), green_color, 2)
            contour_count += 1

    screenshot_with_border = Image.fromarray(cv2.cvtColor(screenshot_after_cv2, cv2.COLOR_BGR2RGB))

    screenshot_with_border.save("screenshot_with_border.png")

    print(f"Number of contours found: {contour_count}")

    print(f"The window is now centered.")
else:
    print(f"Window with title '{app_title}' not found.")
