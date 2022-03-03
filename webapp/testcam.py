from unicodedata import is_normalized
import cv2
import numpy as np
from skimage.morphology import skeletonize, convex_hull_image
from skimage import measure
from src import mathTools
from src import segmentation
from src import reconstruct
import matplotlib.pyplot as plot
import os
import json
import time

plot.style.use('seaborn-darkgrid')

# start timer

global config

# load config
with open('./config.json', 'r') as f:
    config = json.load(f)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)  # manual mode

print(cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))

cap.release()