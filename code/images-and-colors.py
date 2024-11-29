# -*- coding: utf-8 -*-
"""
Created on Nov 2024

@author: KoreAnna
"""

# Import required libraries
from PIL import Image
import numpy as np
import cv2
import os

# Load the uploaded image
image_path = "images-and-colors.png"

# Check if the image exists
assert os.path.exists(image_path), "Image file not found!"

# Load the image using Pillow
image = Image.open(image_path)

# Convert "P" mode images to RGB
if image.mode == "P":
    print("Converting image from 'P' mode to 'RGB'.")
    image = image.convert("RGB")

# Display image properties
print("Image size:", image.size)
print("Image mode after conversion:", image.mode)

# Convert the image to a NumPy array
image_array = np.array(image)

# Ensure the array has the correct shape
print("Image array shape:", image_array.shape)

# Convert the image to BGR format for OpenCV
if image.mode == "RGBA":
    image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
elif image.mode == "RGB":
    image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
else:
    raise ValueError("Unsupported image mode after conversion:", image.mode)

# Convert the image to HSV for color detection
hsv_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

rgb_list = {
    "BGL": [0, 255, 255],
    "BGB": [178, 0, 255],
    "BGA": [0, 38, 255],
    "BGV": [255, 0, 0],
    "A4": [255, 255, 255],
    "BGM": [76, 255, 0],
    "A1": [255, 216, 0],
}

dict_colors = {}
for rgb_name, rgb_color in rgb_list.items():
    # BGR
    check_color = np.uint8([[[rgb_color[2], rgb_color[1], rgb_color[0]]]])
    hsv_color = cv2.cvtColor(check_color, cv2.COLOR_BGR2HSV)
    hue, saturation, value = hsv_color[0][0]
    dict_colors[rgb_name] = {}
    dict_colors[rgb_name]["lower"] = [hue-10, 100, 100]
    dict_colors[rgb_name]["upper"] = [hue+10, 255, 255]
    # print(dict_colors)

for color_name, color_range in dict_colors.items():
    _lower = np.array(color_range["lower"])
    _upper = np.array(color_range["upper"])
    _mask = cv2.inRange(hsv_image, _lower, _upper)

    _contours, _ = cv2.findContours(
        _mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _count = len(_contours)

    # Print the results
    print(f"{color_name} : {_count}")
