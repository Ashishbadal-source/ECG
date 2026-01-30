# # # import numpy as np

# # # def pixel_to_signal(skel, scale=0.01):
# # #     """
# # #     Convert skeletonized ECG trace pixels to voltage signal.
# # #     """
# # #     h, w = skel.shape
# # #     signal = []

# # #     for x in range(w):
# # #         ys = np.where(skel[:, x] > 0)[0]
# # #         if len(ys) == 0:
# # #             signal.append(0.0)
# # #         else:
# # #             signal.append(float(h - ys.mean()) * scale)

# # #     return np.array(signal, dtype=np.float32)




# # # import numpy as np

# # # def pixel_to_signal(mask, scale=0.01):
# # #     """
# # #     Convert ECG mask directly to signal (NO skeletonization).
# # #     """
# # #     h, w = mask.shape
# # #     signal = np.zeros(w, dtype=np.float32)

# # #     for x in range(w):
# # #         ys = np.where(mask[:, x] > 0)[0]

# # #         if len(ys) == 0:
# # #             signal[x] = 0.0
# # #         else:
# # #             # center of waveform
# # #             signal[x] = (h - ys.mean()) * scale

# # #     return signal




# # print(">>> LOADED NEW pixel_to_signal FUNCTION <<<")

# # import numpy as np
# # import cv2

# # # def pixel_to_signal(mask, scale=0.01, target_len=5000):
# # #     """
# # #     Medical-grade ECG signal extraction.
# # #     Resize first, then extract centerline.
# # #     """
# # #     print(">>> ENTER pixel_to_signal <<<")

# # #     h, w = mask.shape

# # #     # 1️⃣ Resize mask to target time resolution
# # #     resized = cv2.resize(
# # #         mask,
# # #         (target_len, h),
# # #         interpolation=cv2.INTER_NEAREST
# # #     )

# # #     # 2️⃣ Vectorized center extraction
# # #     signal = np.zeros(target_len, dtype=np.float32)

# # #     for x in range(target_len):
# # #         ys = np.where(resized[:, x] > 0)[0]
# # #         if len(ys) > 0:
# # #             signal[x] = (h - ys.mean()) * scale

# # #     return signal






# # def pixel_to_signal(mask, scale=0.01, target_len=5000):
# #     import cv2
# #     import numpy as np

# #     h, w = mask.shape

# #     resized = cv2.resize(mask, (target_len, h),
# #                           interpolation=cv2.INTER_NEAREST)

# #     signal = np.zeros(target_len, dtype=np.float32)

# #     for x in range(target_len):
# #         ys = np.where(resized[:, x] > 0)[0]
# #         if len(ys) > 0:
# #             # take darkest / highest density point
# #             signal[x] = (h - ys.min()) * scale

# #     return signal




# import numpy as np
# import cv2

# def pixel_to_signal(mask, scale=0.01, target_len=5000):
#     h, w = mask.shape

#     resized = cv2.resize(
#         mask,
#         (target_len, h),
#         interpolation=cv2.INTER_NEAREST
#     )

#     signal = np.zeros(target_len, dtype=np.float32)

#     for x in range(target_len):
#         ys = np.where(resized[:, x] > 0)[0]

#         # 🔥 STEP 2: SAFETY CHECK (THIS IS THE STEP)
#         if len(ys) < 2:
#             continue   # ignore weak / noisy columns

#         # take strongest waveform point
#         signal[x] = (h - ys.min()) * scale

#     return signal







import numpy as np
import cv2


def pixel_to_signal(mask, scale=0.01, target_len=5000):
    """
    Convert segmented ECG lead mask into 1D signal
    """

    h, w = mask.shape

    # ===============================
    # STEP 1: Resize width to target
    # ===============================
    resized = cv2.resize(
        mask,
        (target_len, h),
        interpolation=cv2.INTER_NEAREST
    )

    signal = np.zeros(target_len, dtype=np.float32)

    # ===============================
    # STEP 2: Column-wise extraction
    # ===============================
    for x in range(target_len):
        ys = np.where(resized[:, x] > 0)[0]

        # SAFETY: ignore empty / weak columns
        if len(ys) < 3:
            signal[x] = np.nan
            continue

        # ===============================
        # STEP 3: Robust centerline
        # ===============================
        y_top = np.min(ys)
        y_bottom = np.max(ys)

        y_center = (y_top + y_bottom) / 2.0

        # ===============================
        # STEP 4: Convert to amplitude
        # ===============================
        signal[x] = (h - y_center) * scale

    # ===============================
    # STEP 5: Handle missing values
    # ===============================
    valid_idx = np.where(~np.isnan(signal))[0]

    if len(valid_idx) > 10:
        signal = np.interp(
            np.arange(target_len),
            valid_idx,
            signal[valid_idx]
        )
    else:
        # extreme failure case
        signal[:] = 0.0

    return signal
