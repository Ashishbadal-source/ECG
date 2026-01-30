# # import cv2
# # import numpy as np

# # from quality_check.run_quality_check import run_quality_checks
# # from segmentation.segment_waveform import segment_waveform
# # from lead_extraction.crop_leads import crop_leads
# # from signal_extraction.skeletonize import skeletonize
# # from signal_extraction.pixel_to_signal import pixel_to_signal
# # from assemble.build_ecg_tensor import build_ecg_tensor

# # img = cv2.imread("data/raw_images/ecg_sample.jpg")

# # ok, reason = run_quality_checks(img)
# # if not ok:
# #     print("QUALITY FAIL:", reason)
# #     exit()

# # mask = segment_waveform(img)
# # lead_masks = crop_leads(mask)

# # signals = []
# # for i in range(len(lead_masks)):
# #     skel = skeletonize(lead_masks[i])
# #     sig = pixel_to_signal(skel)
# #     signals.append(sig)

# # ecg = build_ecg_tensor(signals)
# # np.save("ecg_signal.npy", ecg)

# # print("DONE → ecg_signal.npy", ecg.shape)






# import cv2
# import numpy as np

# from quality_check.run_quality_check import run_quality_checks
# from segmentation.segment_waveform import segment_waveform
# from lead_extraction.crop_leads import crop_leads
# from signal_extraction.skeletonize import skeletonize
# from signal_extraction.pixel_to_voltage import pixel_to_signal
# from assemble.build_ecg_tensor import build_ecg_tensor

# img = cv2.imread("data/raw_images/ecg_001.png")

# ok, reason = run_quality_checks(img)
# if not ok:
#     print("QUALITY FAIL:", reason)
#     exit()

# mask = segment_waveform(img)
# lead_masks = crop_leads(mask)

# signals = []
# for i in range(len(lead_masks)):
#     skel = skeletonize(lead_masks[i])
#     sig = pixel_to_signal(skel)
#     signals.append(sig)

# ecg = build_ecg_tensor(signals)
# np.save("ecg_signal.npy", ecg)

# print("DONE → ecg_signal.npy", ecg.shape)






import cv2
import numpy as np

from quality_check.run_quality_check import run_quality_checks
from segmentation.segment_waveform import segment_waveform
from lead_extraction.crop_leads import crop_leads
# from signal_extraction.skeletonize import skeletonize
from signal_extraction.denoise import median_denoise
from signal_extraction.baseline_correction import remove_baseline
from signal_extraction.bandpass_filter import bandpass_filter
from signal_extraction.normalize import normalize_signal
from signal_extraction.pixel_to_voltage import pixel_to_signal
from assemble.build_ecg_tensor import build_ecg_tensor

print("STEP 1: Loading image...")
img = cv2.imread("data/raw_images/ecg_002.png")

print("STEP 2: Quality check...")
ok, reason = run_quality_checks(img)
if not ok:
    print("QUALITY FAIL:", reason)
    exit()

print("STEP 3: Segmentation started...")
mask = segment_waveform(img)
print("STEP 3 DONE")

print("STEP 4: Lead extraction...")
lead_masks = crop_leads(mask)
print(f"Extracted {len(lead_masks)} lead regions")

print("DEBUG: lead mask shape =", lead_masks[0].shape)

signals = []
for i in range(len(lead_masks)):
    print(f"STEP 5: Processing lead {i+1}")
    # skel = skeletonize(lead_masks[i])
    # sig = pixel_to_signal(skel)
    sig = pixel_to_signal(lead_masks[0])
    sig = remove_baseline(sig)
    sig = bandpass_filter(sig)
    sig = median_denoise(sig)
    sig = normalize_signal(sig)
    signals.append(sig)

print("STEP 6: Assembling ECG tensor...")
ecg = build_ecg_tensor(signals)

np.save("ecg_signal.npy", ecg)
print("DONE → ecg_signal.npy", ecg.shape)

print("DEBUG: mask non-zero pixels =", cv2.countNonZero(mask))
cv2.imshow("DEBUG_MASK", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

from utils.plot_ecg import plot_ecg
plot_ecg(ecg)
