# import numpy as np

# def normalize(signal):
#     if np.std(signal) == 0:
#         return signal
#     return (signal - np.mean(signal)) / np.std(signal)



import numpy as np

def normalize_signal(signal):
    std = np.std(signal)
    if std < 1e-6:
        return signal
    return (signal - np.mean(signal)) / std
