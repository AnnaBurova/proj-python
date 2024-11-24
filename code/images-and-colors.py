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

# Define color ranges for detection
cyan_lower = np.array([85, 100, 100])
cyan_upper = np.array([105, 255, 255])

purple_lower = np.array([130, 100, 100])
purple_upper = np.array([160, 255, 255])

green_lower = np.array([50, 100, 100])
green_upper = np.array([70, 255, 255])

white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 55, 255])

# Create masks for each color
cyan_mask = cv2.inRange(hsv_image, cyan_lower, cyan_upper)
purple_mask = cv2.inRange(hsv_image, purple_lower, purple_upper)
green_mask = cv2.inRange(hsv_image, green_lower, green_upper)
white_mask = cv2.inRange(hsv_image, white_lower, white_upper)

# Count the cyan squares
cyan_contours, _ = cv2.findContours(
    cyan_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cyan_count = len(cyan_contours)

# Count the purple squares
purple_contours, _ = cv2.findContours(
    purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
purple_count = len(purple_contours)

# Count the green squares
green_contours, _ = cv2.findContours(
    green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
green_count = len(green_contours)

# Count the white squares
white_contours, _ = cv2.findContours(
    white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
white_count = len(white_contours)

# Print the results
print(f"Cyan count: {cyan_count}")
print(f"Purple count: {purple_count}")
print(f"Green count: {green_count}")
print(f"White count: {white_count}")
