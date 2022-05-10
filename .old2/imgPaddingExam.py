import cv2
import numpy as np
import sys


img = cv2.imread('assets/shapes-2.jpg', cv2.IMREAD_COLOR)
if img is None:
    sys.exit("Not found input image")


# # Padding img
img_pad = np.zeros([img.shape[0] + 50, img.shape[1] + 50, 3])
img_pad += 100      # grey color BGR: [100, 100, 100] <=> hex: #646464
img_pad[20:, 20:, :] = img