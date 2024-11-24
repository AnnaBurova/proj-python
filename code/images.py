# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:00:36 2024

@author: KoreAnna
"""

from PIL import Image
import numpy as np
import cv2

# Load the uploaded image
image_path = "image.png"
image = Image.open(image_path)

# Convert image to an array for analysis
image_array = np.array(image)

# Display basic properties of the image
image.size, image.mode, image_array.shape

# Convert the image to BGR format (OpenCV compatible)
image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)

# Convert the image to HSV for color detection
hsv_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

# Define color ranges for cyan and purple (detected squares)
cyan_lower = np.array([85, 100, 100])
cyan_upper = np.array([105, 255, 255])

purple_lower = np.array([130, 100, 100])
purple_upper = np.array([160, 255, 255])

# Define color range for green (new color detected)
green_lower = np.array([50, 100, 100])
green_upper = np.array([70, 255, 255])

# Define color range for white (another possible color)
white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 55, 255])

# Create masks for each color
cyan_mask = cv2.inRange(hsv_image, cyan_lower, cyan_upper)
purple_mask = cv2.inRange(hsv_image, purple_lower, purple_upper)
green_mask = cv2.inRange(hsv_image, green_lower, green_upper)
white_mask = cv2.inRange(hsv_image, white_lower, white_upper)

# Count the cyan squares
cyan_contours, _ = cv2.findContours(cyan_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cyan_count = len(cyan_contours)

# Count the purple squares
purple_contours, _ = cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
purple_count = len(purple_contours)

# Count the purple squares
green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
green_count = len(green_contours)

# Count the purple squares
white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
white_count = len(white_contours)

print(cyan_count, purple_count, green_count, white_count)
