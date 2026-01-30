import cv2

def postprocess(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
