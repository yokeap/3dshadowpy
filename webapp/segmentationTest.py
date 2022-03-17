from unicodedata import is_normalized
import cv2
import numpy as np
from skimage.morphology import skeletonize, convex_hull_image
from skimage.filters import threshold_otsu
from skimage import measure
from src import mathTools
from src import segmentation
from src import reconstruct
import matplotlib.pyplot as plot
import os
import json
import time

frame = cv2.imread("./shots/obj.jpg")
cv2.imshow("Input Image", frame)

mask = np.zeros(frame.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
