import cv2
import numpy as np

# List to store clicked points
clicked_points = []

# Callback function to capture mouse clicks
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the clicked coordinates
        clicked_points.append((x, y))
        print(f"Point clicked at: ({x}, {y})")

        # Draw a circle where the user clicks
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Image', image)

        # Define area around click
        area_size = 150 
        x1, y1 = max(x - area_size, 0), max(y - area_size, 0)
        x2, y2 = min(x + area_size, image.shape[1]), min(y + area_size, image.shape[0])

        # get the area of the image with window
        window_area = image[y1:y2, x1:x2] 
        detect_windows_in_area(window_area)


def detect_windows_in_area(window_area):
    
    gray = cv2.cvtColor(window_area, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding to enhance window detection
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    windows = []

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

        # Look for rectangles
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            area = cv2.contourArea(contour)

            # Check aspect ratio and area thresholds to ensure it's a window
            if 0.5 < aspect_ratio < 2 and area > 1000:
                windows.append((x, y, w, h))
    
    # Merge and display boxes
    # merged_windows = merge_bounding_boxes(windows)

    for (x, y, w, h) in windows:
        cv2.rectangle(window_area, (x, y), (x + w, y + h), (0, 255, 0), 3)


# FUNCTION TO MERGE SMALLER BOXES TO MAKE A BIG ONE WHICH DIDN'T END UP BEING USEFUL
# def merge_bounding_boxes(bounding_boxes):
#     if not bounding_boxes:
#         return []

#     merged = []

#     # Function to calculate overlap between two bounding boxes
#     def calculate_overlap(bbox1, bbox2):
#         x1, y1, w1, h1 = bbox1
#         x2, y2, w2, h2 = bbox2
        
#         # Calculate intersection
#         x_inter = max(x1, x2)
#         y_inter = max(y1, y2)
#         w_inter = min(x1 + w1, x2 + w2) - x_inter
#         h_inter = min(y1 + h1, y2 + h2) - y_inter

#         if w_inter <= 0 or h_inter <= 0:
#             return 0  # No overlap

#         # Calculate area of intersection
#         inter_area = w_inter * h_inter
#         area1 = w1 * h1
#         area2 = w2 * h2

#         # Calculate overlap ratio
#         overlap = inter_area / float(min(area1, area2))
#         return overlap

#     for bbox in bounding_boxes:
#         x, y, w, h = bbox
#         merged_flag = False

#         # Try to merge with existing boxes
#         for idx, (mx, my, mw, mh) in enumerate(merged):
#             overlap = calculate_overlap(bbox, (mx, my, mw, mh))
            
#             if overlap > 0:  # Merge if there's any overlap
#                 merged[idx] = (min(mx, x), min(my, y), max(mx + mw, x + w) - min(mx, x), max(my + mh, y + h) - min(my, y))
#                 merged_flag = True
#                 break

#         # If the box couldn't be merged, add it as a new box
#         if not merged_flag:
#             merged.append(bbox)

#     return merged


image = cv2.imread(r'Spike Artifacts\house.jpg')
cv2.imshow('Image', image)
cv2.setMouseCallback('Image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

