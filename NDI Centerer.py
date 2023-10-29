# NDI Configurator
# Author: 0x00
# Moonlight > All


# Install all of these if anything is underlined

#----------------------------
#pip install PyGetWindow
#pip install pyautogui
#pip install Pillow
##pip install opencv-python
#pip install numpy
#----------------------------

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# To install all the packages listed in the requirements.txt file, someone can use the following command:
# pip install -r "requirements.txt"
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
from io import BytesIO
import cv2
import numpy as np
from PIL import Image

# Replace 'NDI Region of Interest' with the actual title of your application window
app_title = 'NDI Region of Interest'

# Load the reference image (with the border)
reference_image = Image.open("ndi_region_reference.png")

# Find the application window by title
app_window = gw.getWindowsWithTitle(app_title)

if app_window:
    app_window = app_window[0]  # Assuming there is only one window with that title

    # Capture a screenshot of the entire screen before moving
    screenshot_before_full = ImageGrab.grab()

    # Get the screen dimensions using pyautogui
    screen_width, screen_height = pyautogui.size()

    # Get the window's dimensions
    window_width, window_height = app_window.width, app_window.height

    # Calculate the position to center the window (accounting for the offset)
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2 - 12  # Adjust the offset as needed

    # Move the application window to the calculated position using pygetwindow
    app_window.moveTo(x_position, y_position)

    # Capture a screenshot of the entire screen after moving
    screenshot_after_full = ImageGrab.grab()

    # Simulate clicking and dragging on the window's border to center it
    pyautogui.mouseDown(x=x_position + 1, y=y_position + 1)  # Adjust coordinates as needed
    pyautogui.mouseUp()

    # Crop the screenshots to the area where the window was
    screenshot_before = screenshot_before_full.crop((x_position, y_position, x_position + window_width, y_position + window_height))
    screenshot_after = screenshot_after_full.crop((x_position, y_position, x_position + window_width, y_position + window_height))

    # Convert the screenshots to numpy arrays (OpenCV format)
    screenshot_before_cv2 = cv2.cvtColor(np.array(screenshot_before), cv2.COLOR_RGB2BGR)
    screenshot_after_cv2 = cv2.cvtColor(np.array(screenshot_after), cv2.COLOR_RGB2BGR)

    # Find the differences between the two screenshots
    difference = cv2.absdiff(screenshot_before_cv2, screenshot_after_cv2)

    # Apply thresholding to the difference image
    _, thresholded = cv2.threshold(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY), 30, 255, cv2.THRESH_BINARY)

    green_color = (0, 255, 0)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a green border around the actual area and count contours
    contour_count = 0  # To count the number of contours
    for contour in contours:
        if cv2.contourArea(contour) > 10:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(screenshot_after_cv2, (x, y), (x + w, y + h), green_color, 2)
            contour_count += 1

    # Convert the image back to PIL format
    screenshot_with_border = Image.fromarray(cv2.cvtColor(screenshot_after_cv2, cv2.COLOR_BGR2RGB))

    # Save the screenshot with the green border
    screenshot_with_border.save("screenshot_with_border.png")

    print(f"Number of contours found: {contour_count}")  # Debug statement

    print(f"The window is now centered.")
else:
    print(f"Window with title '{app_title}' not found.")
