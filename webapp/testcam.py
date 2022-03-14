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

if not cap.isOpened():
    raise IOError("Cannot open webcam")

exposure = 100

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
cap.set(cv2.CAP_PROP_EXPOSURE, exposure)  # manual mode

print(cap.get(cv2.CAP_PROP_EXPOSURE))

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = cap.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    # if cv2.waitKey(1) & 0xFF == ord('i'):
    #     exposure = exposure + 10
    #     cap.set(cv2.CAP_PROP_EXPOSURE, exposure)  # manual mode
    #     print(cap.get(cv2.CAP_PROP_EXPOSURE))

    # if cv2.waitKey(1) & 0xFF == ord('d'):
    #     if exposure > 10:
    #         exposure = exposure - 10
    #     cap.set(cv2.CAP_PROP_EXPOSURE, exposure)  # manual mode
    #     print(cap.get(cv2.CAP_PROP_EXPOSURE))

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break 

    k = cv2.waitKey(1)
    if k == 27:    # Esc key to stop
        break
    else:
        continue


cap.release()