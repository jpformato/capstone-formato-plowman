import cv2
import numpy as np

def detect_windows(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter rectangular contours (potential windows)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 0.5 < aspect_ratio < 2:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Show the detected windows
    cv2.imshow('Detected Windows', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_windows('house.jpg')