import cv2
import numpy as np
from skimage.morphology import skeletonize, convex_hull_image
from skimage import measure
from src import mathTools
from src import segmentation
from src import reconstruct
import matplotlib.pyplot as plt
import os
import json
import time


# start timer
start = time.time()

global config

# load config
with open('./config.json', 'r') as f:
    config = json.load(f)

objReconstruct = reconstruct.reconstruct(1, config)
imgBg = cv2.imread("./ref/background.jpg")
frame = cv2.imread("./shots/obj.jpg")

def process_imgObjColor(imgROI):
    imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    imgObj, imgObjColor = segmentation.obj(imgROI, imageHSV, config["obj"]["hue"], config["obj"]["saturation"],config["obj"]["value"])
    return imgObj, imgObjColor

def process_imgShadowOnObj(imgROI):
    imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    imgShadowOnObj = segmentation.shadowEdgeOnObj(imgROI, imageHSV, config["shadowOnObj"]["hue"], config["shadowOnObj"]["saturation"], config["shadowOnObj"]["value"])
    # imgShadowOnObj = measure.find_contours(imgShadowOnObj, 0.1)
    # imgShadowOnObj = np.asarray(imgShadowOnObj, dtype="uint8")
    return imgShadowOnObj 

diffImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY)
cv2.imshow("Diff Image", diffImage)
ret, imgDiffBin = cv2.threshold(diffImage, 232, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Diff Image Thresholded", imgDiffBin)
imgAnd = cv2.bitwise_and(imgDiffBin, diffImage)
ret, imgBin = cv2.threshold(imgAnd, 130, 255, cv2.THRESH_BINARY)
cv2.imshow("Image And Thresholded", imgBin)
imgClose = cv2.morphologyEx(imgBin, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=2)
cv2.imshow("Image Closing", imgClose)


imgSegmentSource, imgSegmentBlack, imgROI, posCrop = segmentation.objShadow(frame, imgClose)
cv2.imshow("Image ROI", imgROI[0])

imgObj, imgObjColor = process_imgObjColor(imgROI[0])
cv2.imshow("Image Obj", imgObj)
imgShadow = segmentation.shadow(imgROI[0], imgObj)
cv2.imshow("Shadow", imgShadow)
# imgShadowOnObj = process_imgShadowOnObj(imgObjColor)
# cv2.imshow("Image Shadow on Object", imgShadowOnObj)

# objReconstruct.reconstruct(frame, imgObj, imgShadowOnObj, imgShadow, posCrop)
# ptCloud, volume, length = objReconstruct.reconstructVolume(0.05)

# objReconstruct.pointCloudChart_3d()

# end = time.time()
# print("processed time = ", (end - start), "s")

# objReconstruct.volumeChart(end - start)

cv2.waitKey(0)
cv2.destroyAllWindows()