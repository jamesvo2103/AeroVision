# In file: AeroVision/backend/image_processing.py

import cv2
import numpy as np

# --- PARAMETERS TO TUNE ---
# Threshold to isolate the airfoil from the background
AIRFOIL_THRESH = 80
# Max distance from the image center to find the airfoil (prevents finding noise at the edges)
MAX_DISTANCE_FROM_CENTER = 150
# Minimum area for a contour to be considered the airfoil
MIN_CONTOUR_AREA = 500

def preprocess_airfoil(image_array: np.ndarray) -> np.ndarray:
    """
    Takes an image as a NumPy array, isolates the central airfoil,
    and returns a clean black and white image of the airfoil shape.
    """
    # Convert the input image to grayscale
    gray_plate = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to get a rough black and white image
    _, binary_plate = cv2.threshold(gray_plate, AIRFOIL_THRESH, 255, cv2.THRESH_BINARY)

    # Find all distinct shapes (contours) in the image
    contours, _ = cv2.findContours(binary_plate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get image dimensions to find the center
    h, w = image_array.shape[:2]
    center_x, center_y = w // 2, h // 2

    # Create a new blank (black) image to draw the final airfoil on
    airfoil_only_mask = np.zeros((h, w), dtype=np.uint8)

    # Loop through all found contours to find the correct one
    for cnt in contours:
        # Ignore small contours that are likely noise
        if cv2.contourArea(cnt) > MIN_CONTOUR_AREA:
            # Calculate the center of the contour
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Check if the contour is close to the center of the image
            distance = np.sqrt((cx - center_x)**2 + (cy - center_y)**2)
            if distance < MAX_DISTANCE_FROM_CENTER:
                # This is likely our airfoil, draw it in white on our blank mask
                cv2.drawContours(airfoil_only_mask, [cnt], -1, (255, 255, 255), thickness=cv2.FILLED)
                # We found our main airfoil, no need to check other contours
                break

    # The final image is the black mask with the white airfoil shape
    return airfoil_only_mask