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
from signal_extraction.length_normalize import normalize_length
from signal_extraction.amplitude_normalize import normalize_amplitude


# ================= ASSEMBLY =================
from assemble.build_ecg_tensor import build_ecg_tensor

# ================= VIS =================
from utils.plot_ecg import plot_ecg


# ==================================================
# STEP 1: LOAD IMAGE
# ==================================================
print("STEP 1: Loading ECG image...")
image_path = "data/raw_images/ecg_001.png"
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
ecg = normalize_length(ecg, target_len=5000)
ecg = normalize_amplitude(ecg, target_mv=1.0)

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
    # cv2.imshow(f"LEAD_{i+1}", lead_vis)

cv2.waitKey(0)
cv2.destroyAllWindows()

plot_ecg(ecg)

print("🎉 PIPELINE COMPLETED SUCCESSFULLY")


from ml.validate_input import validate_ecg

ok, reason = validate_ecg(ecg)

if not ok:
    raise ValueError(f"❌ ECG validation failed: {reason}")

print("✅ ECG input validated for ML")


from ml.prepare_input import prepare_ml_input

ml_input = prepare_ml_input(ecg)
print("✅ ML input ready:", ml_input.shape)
print(type(ecg), ecg.shape)
