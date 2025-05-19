import numpy as np

def check_crossing(curr_cx, prev_cx, red_line_x, blue_line_x, offset=10):
    # Left to right
    if prev_cx < red_line_x - offset and curr_cx > blue_line_x + offset:
        return "right"
    # Right to left
    elif prev_cx > blue_line_x + offset and curr_cx < red_line_x - offset:
        return "left"
    else:
        return None

def is_tailgating(bbox1, bbox2, direction='horizontal', threshold=50):
    """
    Check if two vehicles are tailgating based on their bounding box centers.
    Direction: 'horizontal' (default) or 'vertical'
    """
    cx1 = bbox1[0] + bbox1[2] / 2
    cy1 = bbox1[1] + bbox1[3] / 2
    cx2 = bbox2[0] + bbox2[2] / 2
    cy2 = bbox2[1] + bbox2[3] / 2

    if direction == 'horizontal':
        # Tailgating in X direction (e.g., left to right traffic)
        x_dist = abs(cx1 - cx2)
        y_dist = abs(cy1 - cy2)
        return x_dist < threshold and y_dist < 50
    else:
        # Tailgating in Y direction (e.g., top to bottom traffic)
        x_dist = abs(cx1 - cx2)
        y_dist = abs(cy1 - cy2)
        return y_dist < threshold and x_dist < 50
