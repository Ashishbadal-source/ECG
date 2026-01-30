import numpy as np

def crop_leads(mask):
    h, w = mask.shape
    lead_height = h // 6

    leads = []
    for i in range(6):
        y1 = i * lead_height
        y2 = (i + 1) * lead_height
        lead = mask[y1:y2, :]
        leads.append(lead)

    return leads
