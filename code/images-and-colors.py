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

dict_colors = {
    "cyan": {
        "lower": [85, 100, 100],
        "upper": [105, 255, 255],
    },
    "purple": {
        "lower": [130, 100, 100],
        "upper": [160, 255, 255],
    },
    "green": {
        "lower": [50, 100, 100],
        "upper": [70, 255, 255],
    },
    "white": {
        "lower": [0, 0, 200],
        "upper": [180, 55, 255],
    }
}

for color_name, color_range in dict_colors.items():
    _lower = np.array(color_range["lower"])
    _upper = np.array(color_range["upper"])
    _mask = cv2.inRange(hsv_image, _lower, _upper)

    _contours, _ = cv2.findContours(
        _mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _count = len(_contours)

    # Print the results
    print(f"{color_name} count: {_count}")
