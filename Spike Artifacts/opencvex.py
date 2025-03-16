import cv2
import numpy as np
import os

def detect_windows(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # width = int(image.shape[1] * 0.6)
    # height = int(image.shape[0] * 0.6)
    # dim = (width, height)
    # image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

     # Reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding to enhance window detection
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Alternatively, use Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        if len(approx) == 4:  # Ensure it's a quadrilateral (likely a window)
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            area = cv2.contourArea(contour)

            if 0.5 < aspect_ratio < 2 and area > 15000:  # Adjust area threshold as needed
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # # Apply edge detection
    # edges = cv2.Canny(gray, 50, 150)
    
    # # Find contours
    # contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # # Filter rectangular contours (potential windows)
    # for contour in contours:
    #     approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    #     if len(approx) == 4:
    #         x, y, w, h = cv2.boundingRect(approx)
    #         aspect_ratio = w / float(h)
    #         if 0.5 < aspect_ratio < 2:
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Show the detected windows
    cv2.imshow('Detected Windows', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_windows(r"Spike Artifacts\house.jpg")