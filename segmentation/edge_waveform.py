# # import cv2
# # import numpy as np

# # def extract_waveform_edges(image):
# #     """
# #     Edge-based ECG waveform extraction
# #     Works even when segmentation fails
# #     """
# #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# #     # Remove grid (light smoothing)
# #     blur = cv2.GaussianBlur(gray, (5, 5), 0)

# #     # Strong edge detection
# #     edges = cv2.Canny(blur, 50, 150)

# #     # Remove vertical grid lines
# #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
# #     cleaned = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel, iterations=1)

# #     return cleaned




# import cv2
# import numpy as np

# def extract_waveform_edges(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Smooth image to reduce noise
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Edge detection
#     edges = cv2.Canny(blur, 50, 150)

#     # ===============================
#     # REMOVE VERTICAL GRID LINES
#     # ===============================
#     vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
#     vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)

#     edges_no_vertical = cv2.subtract(edges, vertical_lines)

#     # ===============================
#     # REMOVE HORIZONTAL GRID LINES
#     # ===============================
#     horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
#     horizontal_lines = cv2.morphologyEx(edges_no_vertical, cv2.MORPH_OPEN, horizontal_kernel)

#     cleaned = cv2.subtract(edges_no_vertical, horizontal_lines)

#     return cleaned




import cv2
import numpy as np

def extract_waveform_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Moderate blur (not too strong)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Conservative edge detection
    edges = cv2.Canny(blur, 50, 150)

    # -------- Attempt 1: moderate grid removal --------
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))

    vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
    no_vertical = cv2.subtract(edges, vertical_lines)

    horizontal_lines = cv2.morphologyEx(no_vertical, cv2.MORPH_OPEN, horizontal_kernel)
    cleaned = cv2.subtract(no_vertical, horizontal_lines)

    # If waveform survives → good
    if cv2.countNonZero(cleaned) > 0:
        return cleaned

    # -------- Fallback: VERY IMPORTANT --------
    # If aggressive suppression killed waveform,
    # return raw edges instead of failing
    print("⚠️ Grid suppression too aggressive, falling back to raw edges")

    return edges
