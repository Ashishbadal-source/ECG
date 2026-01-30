# import cv2
# import numpy as np

# def check_tilt(image, angle_threshold=5):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 50, 150)

#     lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
#     if lines is None:
#         return True   # no strong lines → bad image

#     angles = []
#     for i in range(len(lines)):
#         rho, theta = lines[i][0]
#         angle = abs((theta * 180 / np.pi) - 90)
#         angles.append(angle)

#     avg_angle = np.mean(angles)

#     if avg_angle > angle_threshold:
#         return True   # tilted
#     return False


def check_tilt(image):
    # TEMPORARILY DISABLED
    # Reason: HoughLines misfires on ECG waveforms
    return False
