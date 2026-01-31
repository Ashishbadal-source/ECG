# # # # import cv2
# # # # import numpy as np

# # # # from quality_check.run_quality_check import run_quality_checks
# # # # from segmentation.segment_waveform import segment_waveform
# # # # from lead_extraction.crop_leads import crop_leads
# # # # from signal_extraction.skeletonize import skeletonize
# # # # from signal_extraction.pixel_to_signal import pixel_to_signal
# # # # from assemble.build_ecg_tensor import build_ecg_tensor

# # # # img = cv2.imread("data/raw_images/ecg_sample.jpg")

# # # # ok, reason = run_quality_checks(img)
# # # # if not ok:
# # # #     print("QUALITY FAIL:", reason)
# # # #     exit()

# # # # mask = segment_waveform(img)
# # # # lead_masks = crop_leads(mask)

# # # # signals = []
# # # # for i in range(len(lead_masks)):
# # # #     skel = skeletonize(lead_masks[i])
# # # #     sig = pixel_to_signal(skel)
# # # #     signals.append(sig)

# # # # ecg = build_ecg_tensor(signals)
# # # # np.save("ecg_signal.npy", ecg)

# # # # print("DONE → ecg_signal.npy", ecg.shape)






# # # import cv2
# # # import numpy as np

# # # from quality_check.run_quality_check import run_quality_checks
# # # from segmentation.segment_waveform import segment_waveform
# # # from lead_extraction.crop_leads import crop_leads
# # # from signal_extraction.skeletonize import skeletonize
# # # from signal_extraction.pixel_to_voltage import pixel_to_signal
# # # from assemble.build_ecg_tensor import build_ecg_tensor

# # # img = cv2.imread("data/raw_images/ecg_001.png")

# # # ok, reason = run_quality_checks(img)
# # # if not ok:
# # #     print("QUALITY FAIL:", reason)
# # #     exit()

# # # mask = segment_waveform(img)
# # # lead_masks = crop_leads(mask)

# # # signals = []
# # # for i in range(len(lead_masks)):
# # #     skel = skeletonize(lead_masks[i])
# # #     sig = pixel_to_signal(skel)
# # #     signals.append(sig)

# # # ecg = build_ecg_tensor(signals)
# # # np.save("ecg_signal.npy", ecg)

# # # print("DONE → ecg_signal.npy", ecg.shape)






# # # import cv2
# # # import numpy as np

# # # from quality_check.run_quality_check import run_quality_checks
# # # from segmentation.segment_waveform import segment_waveform
# # # from lead_extraction.crop_leads import crop_leads
# # # # from signal_extraction.skeletonize import skeletonize
# # # from signal_extraction.denoise import median_denoise
# # # from signal_extraction.baseline_correction import remove_baseline
# # # from signal_extraction.bandpass_filter import bandpass_filter
# # # from signal_extraction.normalize import normalize_signal
# # # from signal_extraction.pixel_to_voltage import pixel_to_signal
# # # from assemble.build_ecg_tensor import build_ecg_tensor
# # # from quality_check.check_quality import check_quality


# # # print("STEP 1: Loading image...")
# # # img = cv2.imread("data/raw_images/ecg_002.png")

# # # print("STEP 2: Quality check...")
# # # ok, reason = run_quality_checks(img)
# # # if not ok:
# # #     print("QUALITY FAIL:", reason)
# # #     exit()

# # # print("STEP 3: Segmentation started...")
# # # mask = segment_waveform(img)
# # # print("STEP 3 DONE")

# # # print("STEP 4: Lead extraction...")
# # # lead_masks = crop_leads(mask)
# # # print(f"Extracted {len(lead_masks)} lead regions")

# # # print("DEBUG: lead mask shape =", lead_masks[0].shape)

# # # signals = []
# # # for i in range(len(lead_masks)):
# # #     print(f"STEP 5: Processing lead {i+1}")
# # #     # skel = skeletonize(lead_masks[i])
# # #     # sig = pixel_to_signal(skel)
# # #     sig = pixel_to_signal(lead_masks[0])
# # #     sig = remove_baseline(sig)
# # #     sig = bandpass_filter(sig)
# # #     sig = median_denoise(sig)
# # #     sig = normalize_signal(sig)
# # #     signals.append(sig)

# # # print("STEP 6: Assembling ECG tensor...")
# # # ecg = build_ecg_tensor(signals)

# # # np.save("ecg_signal.npy", ecg)
# # # print("DONE → ecg_signal.npy", ecg.shape)

# # # print("DEBUG: mask non-zero pixels =", cv2.countNonZero(mask))
# # # cv2.imshow("DEBUG_MASK", mask)
# # # cv2.waitKey(0)
# # # cv2.destroyAllWindows()

# # # from utils.plot_ecg import plot_ecg
# # # plot_ecg(ecg)









# # import cv2
# # import numpy as np

# # # ================= QUALITY CHECK =================
# # from quality_check.check_quality import check_quality

# # # ================= SEGMENTATION =================
# # from segmentation.segment_waveform import segment_waveform

# # # ================= LEAD EXTRACTION =================
# # from lead_extraction.crop_leads import crop_leads

# # # ================= SIGNAL PROCESSING =================
# # from signal_extraction.pixel_to_voltage import pixel_to_signal
# # from signal_extraction.baseline_correction import remove_baseline
# # from signal_extraction.bandpass_filter import bandpass_filter
# # from signal_extraction.denoise import median_denoise
# # from signal_extraction.normalize import normalize_signal

# # # ================= ASSEMBLY =================
# # from assemble.build_ecg_tensor import build_ecg_tensor

# # # ================= VIS =================
# # from utils.plot_ecg import plot_ecg


# # # ==================================================
# # # STEP 1: LOAD IMAGE
# # # ==================================================
# # print("STEP 1: Loading ECG image...")
# # image_path = "data/raw_images/ecg_001.png"
# # img = cv2.imread(image_path)

# # if img is None:
# #     raise ValueError("❌ Image not found or unreadable")


# # # ==================================================
# # # STEP 2: QUALITY CHECK (HARD GATE)
# # # ==================================================
# # print("STEP 2: Running quality checks...")
# # quality = check_quality(image_path)

# # if not quality["quality_pass"]:
# #     print("❌ QUALITY CHECK FAILED")
# #     print("Reasons:", quality["reasons"])
# #     exit()

# # print("✅ Quality check passed")


# # # ==================================================
# # # STEP 3: SEGMENT ECG WAVEFORM
# # # ==================================================
# # print("STEP 3: Segmenting waveform...")
# # mask = segment_waveform(img)

# # if mask is None or cv2.countNonZero(mask) == 0:
# #     raise ValueError("❌ Segmentation failed (empty mask)")

# # print("✅ Segmentation complete")


# # # ==================================================
# # # STEP 4: EXTRACT LEADS
# # # ==================================================
# # print("STEP 4: Extracting leads...")
# # lead_masks = crop_leads(mask)

# # if len(lead_masks) == 0:
# #     raise ValueError("❌ No leads extracted")

# # print(f"✅ Extracted {len(lead_masks)} leads")


# # # ==================================================
# # # STEP 5: SIGNAL EXTRACTION & PROCESSING
# # # ==================================================
# # signals = []

# # for i in range(len(lead_masks)):
# #     print(f"STEP 5.{i+1}: Processing lead {i+1}")

# #     lead_mask = lead_masks[i]

# #     # pixel → signal
# #     sig = pixel_to_signal(lead_mask)

# #     # preprocessing pipeline
# #     sig = remove_baseline(sig)
# #     sig = bandpass_filter(sig)
# #     sig = median_denoise(sig)
# #     sig = normalize_signal(sig)

# #     signals.append(sig)


# # # ==================================================
# # # STEP 6: BUILD ECG TENSOR
# # # ==================================================
# # print("STEP 6: Building ECG tensor...")
# # ecg = build_ecg_tensor(signals)

# # print("✅ ECG tensor shape:", ecg.shape)

# # np.save("ecg_signal.npy", ecg)
# # print("📁 Saved → ecg_signal.npy")


# # # ==================================================
# # # STEP 7: DEBUG + VISUALIZATION
# # # ==================================================
# # print("DEBUG: Non-zero pixels in mask =", cv2.countNonZero(mask))

# # cv2.imshow("SEGMENTATION_MASK", mask)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()

# # plot_ecg(ecg)

# # print("🎉 PIPELINE COMPLETED SUCCESSFULLY")










# # import cv2
# # import numpy as np

# # # ================= QUALITY CHECK =================
# # from quality_check.check_quality import check_quality

# # # ================= SEGMENTATION =================
# # from segmentation.segment_waveform import segment_waveform
# # from segmentation.postprocess import clean_segmentation_mask
# # # ================= LEAD EXTRACTION =================
# # from lead_extraction.crop_leads import crop_leads

# # # ================= SIGNAL PROCESSING =================
# # from signal_extraction.pixel_to_voltage import pixel_to_signal
# # from signal_extraction.baseline_correction import remove_baseline
# # from signal_extraction.bandpass_filter import bandpass_filter
# # from signal_extraction.denoise import median_denoise
# # from signal_extraction.normalize import normalize_signal

# # # ================= ASSEMBLY =================
# # from assemble.build_ecg_tensor import build_ecg_tensor

# # # ================= VIS =================
# # from utils.plot_ecg import plot_ecg


# # # ==================================================
# # # STEP 1: LOAD IMAGE
# # # ==================================================
# # print("STEP 1: Loading ECG image...")
# # image_path = "data/raw_images/ecg_001.png"
# # img = cv2.imread(image_path)

# # if img is None:
# #     raise ValueError("❌ Image not found or unreadable")


# # # ==================================================
# # # STEP 2: QUALITY CHECK (HARD GATE)
# # # ==================================================
# # print("STEP 2: Running quality checks...")
# # quality = check_quality(image_path)

# # if not quality["quality_pass"]:
# #     print("❌ QUALITY CHECK FAILED")
# #     print("Reasons:", quality["reasons"])
# #     exit()

# # print("✅ Quality check passed")


# # # ==================================================
# # # STEP 3: SEGMENT ECG WAVEFORM
# # # ==================================================
# # print("STEP 3: Segmenting waveform...")
# # mask = segment_waveform(img)

# # if mask is None or cv2.countNonZero(mask) == 0:
# #     raise ValueError("❌ Segmentation failed (empty mask)")

# # print("✅ Segmentation complete")


# # # ==================================================
# # # STEP 4: EXTRACT LEADS
# # # ==================================================
# # print("STEP 4: Extracting leads...")
# # lead_masks = crop_leads(mask)

# # if len(lead_masks) == 0:
# #     raise ValueError("❌ No leads extracted")

# # print(f"✅ Extracted {len(lead_masks)} leads")


# # # ==================================================
# # # STEP 5: SIGNAL EXTRACTION & PROCESSING
# # # ==================================================
# # signals = []

# # for i in range(len(lead_masks)):
# #     print(f"STEP 5.{i+1}: Processing lead {i+1}")

# #     lead_mask = lead_masks[i]

# #     sig = pixel_to_signal(lead_mask)
# #     sig = remove_baseline(sig)
# #     sig = bandpass_filter(sig)
# #     sig = median_denoise(sig)
# #     sig = normalize_signal(sig)

# #     signals.append(sig)


# # # ==================================================
# # # STEP 6: BUILD ECG TENSOR
# # # ==================================================
# # print("STEP 6: Building ECG tensor...")
# # ecg = build_ecg_tensor(signals)

# # print("✅ ECG tensor shape:", ecg.shape)

# # np.save("ecg_signal.npy", ecg)
# # print("📁 Saved → ecg_signal.npy")


# # # ==================================================
# # # STEP 7: DEBUG VISUALIZATION (IMPORTANT)
# # # ==================================================
# # print("DEBUG: Non-zero pixels in mask =", cv2.countNonZero(mask))

# # # --- Show segmentation mask properly ---
# # mask_vis = (mask > 0).astype("uint8") * 255
# # cv2.imshow("SEGMENTATION_MASK", mask_vis)

# # # --- Show each extracted lead ---
# # for i in range(len(lead_masks)):
# #     lead_vis = (lead_masks[i] > 0).astype("uint8") * 255
# #     cv2.imshow(f"LEAD_{i+1}", lead_vis)

# # cv2.waitKey(0)
# # cv2.destroyAllWindows()

# # # --- Plot ECG signals ---
# # plot_ecg(ecg)

# # print("🎉 PIPELINE COMPLETED SUCCESSFULLY")










# import cv2
# import numpy as np

# # ================= QUALITY CHECK =================
# from quality_check.check_quality import check_quality

# # ================= SEGMENTATION =================
# from segmentation.segment_waveform import segment_waveform
# from segmentation.postprocess import clean_segmentation_mask

# # ================= LEAD EXTRACTION =================
# from lead_extraction.crop_leads import crop_leads

# # ================= SIGNAL PROCESSING =================
# from signal_extraction.pixel_to_voltage import pixel_to_signal
# from signal_extraction.baseline_correction import remove_baseline
# from signal_extraction.bandpass_filter import bandpass_filter
# from signal_extraction.denoise import median_denoise
# from signal_extraction.normalize import normalize_signal

# # ================= ASSEMBLY =================
# from assemble.build_ecg_tensor import build_ecg_tensor

# # ================= VIS =================
# from utils.plot_ecg import plot_ecg


# # ==================================================
# # STEP 1: LOAD IMAGE
# # ==================================================
# print("STEP 1: Loading ECG image...")
# image_path = "data/raw_images/ecg_001.png"
# img = cv2.imread(image_path)

# if img is None:
#     raise ValueError("❌ Image not found or unreadable")


# # ==================================================
# # STEP 2: QUALITY CHECK (HARD GATE)
# # ==================================================
# print("STEP 2: Running quality checks...")
# quality = check_quality(image_path)

# if not quality["quality_pass"]:
#     print("❌ QUALITY CHECK FAILED")
#     print("Reasons:", quality["reasons"])
#     exit()

# print("✅ Quality check passed")


# # ==================================================
# # STEP 3: SEGMENT ECG WAVEFORM
# # ==================================================
# print("STEP 3: Segmenting waveform...")
# raw_mask = segment_waveform(img)

# if raw_mask is None or cv2.countNonZero(raw_mask) == 0:
#     raise ValueError("❌ Segmentation failed (empty raw mask)")

# print("✅ Raw segmentation complete")


# # ==================================================
# # STEP 3.5: CLEAN SEGMENTATION MASK (🔥 MOST IMPORTANT)
# # ==================================================
# print("STEP 3.5: Cleaning segmentation mask...")
# mask = clean_segmentation_mask(raw_mask)

# if mask is None or cv2.countNonZero(mask) == 0:
#     raise ValueError("❌ Cleaned mask is empty")

# print("✅ Mask cleaning complete")


# # ==================================================
# # STEP 4: EXTRACT LEADS (USE CLEAN MASK ONLY)
# # ==================================================
# print("STEP 4: Extracting leads...")
# lead_masks = crop_leads(mask)

# if len(lead_masks) == 0:
#     raise ValueError("❌ No leads extracted")

# print(f"✅ Extracted {len(lead_masks)} leads")


# # ==================================================
# # STEP 5: SIGNAL EXTRACTION & PROCESSING
# # ==================================================
# signals = []

# for i in range(len(lead_masks)):
#     print(f"STEP 5.{i+1}: Processing lead {i+1}")

#     lead_mask = lead_masks[i]

#     sig = pixel_to_signal(lead_mask)
#     sig = remove_baseline(sig)
#     sig = bandpass_filter(sig)
#     sig = median_denoise(sig)
#     sig = normalize_signal(sig)

#     signals.append(sig)


# # ==================================================
# # STEP 6: BUILD ECG TENSOR
# # ==================================================
# print("STEP 6: Building ECG tensor...")
# ecg = build_ecg_tensor(signals)

# print("✅ ECG tensor shape:", ecg.shape)

# np.save("ecg_signal.npy", ecg)
# print("📁 Saved → ecg_signal.npy")


# # ==================================================
# # STEP 7: DEBUG VISUALIZATION (CRITICAL)
# # ==================================================
# print("DEBUG: Non-zero pixels (RAW mask)   =", cv2.countNonZero(raw_mask))
# print("DEBUG: Non-zero pixels (CLEAN mask) =", cv2.countNonZero(mask))

# # --- Show raw vs clean segmentation ---
# raw_vis = (raw_mask > 0).astype("uint8") * 255
# clean_vis = (mask > 0).astype("uint8") * 255

# cv2.imshow("RAW_SEGMENTATION_MASK", raw_vis)
# cv2.imshow("CLEAN_SEGMENTATION_MASK", clean_vis)

# # --- Show each extracted lead ---
# for i in range(len(lead_masks)):
#     lead_vis = (lead_masks[i] > 0).astype("uint8") * 255
#     cv2.imshow(f"LEAD_{i+1}", lead_vis)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # --- Plot ECG signals ---
# plot_ecg(ecg)

# print("🎉 PIPELINE COMPLETED SUCCESSFULLY")










import cv2
import numpy as np

# ================= QUALITY CHECK =================
from quality_check.check_quality import check_quality

# ================= EDGE-BASED WAVEFORM EXTRACTION =================
from segmentation.edge_waveform import extract_waveform_edges

# ================= LEAD EXTRACTION =================
from lead_extraction.crop_leads import crop_leads

# ================= SIGNAL PROCESSING =================
from signal_extraction.pixel_to_voltage import pixel_to_signal
from signal_extraction.baseline_correction import remove_baseline
from signal_extraction.bandpass_filter import bandpass_filter
from signal_extraction.denoise import median_denoise
from signal_extraction.normalize import normalize_signal
from lead_extraction.order_and_polarity import order_and_fix_ecg

# ================= ASSEMBLY =================
from assemble.build_ecg_tensor import build_ecg_tensor

# ================= VIS =================
from utils.plot_ecg import plot_ecg


# ==================================================
# STEP 1: LOAD IMAGE
# ==================================================
print("STEP 1: Loading ECG image...")
image_path = "data/raw_images/ecg_002.png"
img = cv2.imread(image_path)

if img is None:
    raise ValueError("❌ Image not found or unreadable")


# ==================================================
# STEP 2: QUALITY CHECK (HARD GATE)
# ==================================================
print("STEP 2: Running quality checks...")
quality = check_quality(image_path)

if not quality["quality_pass"]:
    print("❌ QUALITY CHECK FAILED")
    print("Reasons:", quality["reasons"])
    exit()

print("✅ Quality check passed")


# ==================================================
# STEP 3: EDGE-BASED WAVEFORM EXTRACTION (🔥 KEY FIX)
# ==================================================
print("STEP 3: Extracting waveform using edge-based method...")
mask = extract_waveform_edges(img)

# if cv2.countNonZero(mask) == 0:
#     raise ValueError("❌ Edge-based extraction failed")
if cv2.countNonZero(mask) == 0:
    print("⚠️ Empty mask detected, continuing with raw edges")


print("✅ Edge waveform extraction complete")


# ==================================================
# STEP 4: EXTRACT LEADS
# ==================================================
print("STEP 4: Extracting leads...")
lead_masks = crop_leads(mask)

if len(lead_masks) == 0:
    raise ValueError("❌ No leads extracted")

print(f"✅ Extracted {len(lead_masks)} leads")


# ==================================================
# STEP 5: SIGNAL EXTRACTION & PROCESSING
# ==================================================
signals = []

for i in range(len(lead_masks)):
    print(f"STEP 5.{i+1}: Processing lead {i+1}")

    lead_mask = lead_masks[i]

    sig = pixel_to_signal(lead_mask)
    sig = remove_baseline(sig)
    sig = bandpass_filter(sig)
    sig = median_denoise(sig)
    sig = normalize_signal(sig)

    signals.append(sig)


# ==================================================
# STEP 6: BUILD ECG TENSOR
# ==================================================
print("STEP 6: Building ECG tensor...")
ecg = build_ecg_tensor(signals)
ecg = order_and_fix_ecg(ecg)

print("✅ ECG tensor shape:", ecg.shape)

np.save("ecg_signal.npy", ecg)
print("📁 Saved → ecg_signal.npy")


# ==================================================
# STEP 7: DEBUG VISUALIZATION
# ==================================================
print("DEBUG: Non-zero pixels (EDGE mask) =", cv2.countNonZero(mask))

cv2.imshow("EDGE_WAVEFORM_MASK", mask)

for i in range(len(lead_masks)):
    lead_vis = (lead_masks[i] > 0).astype("uint8") * 255
    cv2.imshow(f"LEAD_{i+1}", lead_vis)

cv2.waitKey(0)
cv2.destroyAllWindows()

plot_ecg(ecg)

print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
