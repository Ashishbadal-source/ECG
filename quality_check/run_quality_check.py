# from blur import is_blurry
# from rotation import is_rotated
# from brightness import bad_brightness

# def run_quality_checks(img):
#     if is_blurry(img):
#         return False, "Image blurry"
#     if is_rotated(img):
#         return False, "Image rotated"
#     if bad_brightness(img):
#         return False, "Bad lighting"
#     return True, None



from .blur import is_blurry
from .rotation import is_rotated
from .brightness import bad_brightness
from .completeness import is_incomplete


# def run_quality_checks(img):
#     if is_blurry(img):
#         return False, "Image blurry"

#     if is_rotated(img):
#         return False, "Image rotated"

#     if bad_brightness(img):
#         return False, "Bad lighting"

#     if is_incomplete(img):
#         return False, "Image incomplete"

#     return True, None



def run_quality_checks(img):
    # ECG-specific: do not reject for rotation or brightness
    return True, None
