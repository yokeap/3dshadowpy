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

plot.style.use('seaborn-darkgrid')

# start timer

global config

# load config
with open('./config.json', 'r') as f:
    config = json.load(f)

objReconstruct = reconstruct.reconstruct(1, config)
imgBg = cv2.imread("./ref/background.jpg")
cv2.imshow("Background Image", imgBg)
frame = cv2.imread("./imgraw.jpg")
cv2.imshow("Input Image", frame)

imgBg = cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY)

# imgBg = cv2.fastNlMeansDenoisingColored(imgBg, h=1)
# frame = cv2.fastNlMeansDenoisingColored(frame, h=1)

def process_imgObjColor(imgROI):
    imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    imgObj, imgObjColor = segmentation.obj(imgROI, imageHSV, config["obj"]["hue"], config["obj"]["saturation"],config["obj"]["value"])
    return imgObj, imgObjColor

def process_imgObj(imgROI):
    imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    
    # h, s, v = imageHSV[:,:,0], imageHSV[:,:,1], imageHSV[:,:,2]
    # thresh1 = cv2.adaptiveThreshold(cv2.cvtColor(imgROI, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 5)
    # cv2.imshow("S Channel", thresh1)
    imgObj, imgSkeleton = segmentation.obj(imgROI, imageHSV, config["obj"]["hue"], config["obj"]["saturation"],config["obj"]["value"])
    # posOrigin, posDestination, imgPseudoSkel = segmentation.pseudoSkeleton(imgROI, skeleton)
    # print("pos origin = ", posOrigin)
    # print("pos destination = ", posDestination)
    return imgObj, imgSkeleton

def process_obj_shadow_skeleton(imgROI):
    imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    imgShadow = segmentation.shadow(imgROI, imageHSV)
    imgObj, imgSkeleton = segmentation.obj(imgROI, imgShadow)
    return imgObj, imgShadow, imgSkeleton

def process_imgShadowOnObj(imgROI):
    imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    h, s, v = imageHSV[:,:,0], imageHSV[:,:,1], imageHSV[:,:,2]
    # print(v)
    # h = cv2.calcHist([h],[0],None,[360],[0,360])
    # s = cv2.calcHist([s],[0],None,[256],[5,250])
    # v = cv2.calcHist([v],[0],None,[256],[5,256])
    thresholds = threshold_otsu(v.ravel())
    print(thresholds)
    # plot.plot(s)
    # plot.xlim([0,256])
    # plot.ylim((np.mean(h) + 0.5 * np.std(h)).tolist())
    # plot.show()
    imgShadowOnObj = segmentation.shadowEdgeOnObj(imgROI, imageHSV, config["shadowOnObj"]["hue"], config["shadowOnObj"]["saturation"], config["shadowOnObj"]["value"])
    # imgShadowOnObj = measure.find_contours(imgShadowOnObj, 0.1)
    # imgShadowOnObj = np.asarray(imgShadowOnObj, dtype="uint8")
    return imgShadowOnObj

def otsu(hist_channel):
    is_normalized = os.truncate
    index_start = 50
    # Set total number of bins in the histogram
    bins_num = 256

    # Get the image histogram
    hist, bin_edges = np.histogram(hist_channel, bins=bins_num)

    # Get normalized histogram if it is required
    if is_normalized:
        hist = np.divide(hist.ravel(), hist.max())

    # Calculate centers of bins
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.

    # Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]

    # Get the class means mu0(t)
    mean1 = np.cumsum(hist * bin_mids) / weight1
    # Get the class means mu1(t)
    mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

    inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    # Maximize the inter_class_vawiance function val
    index_of_max_val = np.argmax(inter_class_variance)

    threshold = (bin_mids[:-1][index_of_max_val]) 
    print("Otsu's algorithm implementation thresholding result: ", threshold)
    return threshold

start = time.time()

diffImage = cv2.absdiff(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), imgBg)
cv2.imshow("Diff Image", diffImage)
# cv2.imwrite('./statictest_pic/imageDiff.jpg', diffImage)
# otsu(diffImage)
ret, imgDiffBin = cv2.threshold(diffImage, 1, 255, cv2.THRESH_BINARY)
cv2.imshow("Diff Image Thresholded", imgDiffBin)
imgDiffMorphBin = cv2.morphologyEx(imgDiffBin, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
cv2.imshow("Image Morphology", imgDiffMorphBin)
# imgAnd = cv2.bitwise_and(imgDiffMorphBin, diffImage)
# ret, imgBin = cv2.threshold(imgAnd, 130, 255, cv2.THRESH_BINARY)
# cv2.imshow("Image And Thresholded", imgAnd)
# imgClose = cv2.morphologyEx(imgBin, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=2)
# cv2.imshow("Image Closing", imgClose)


# imgSegmentSource, imgSegmentBlack, imgROI, posCrop = segmentation.objShadow(frame, imgDiffMorphBin )
imgROI, posCrop = segmentation.singleObjShadow(frame, imgDiffMorphBin )
cv2.imshow("Image ROI", imgROI[0])
# cv2.imwrite('./statictest_pic/imageroi.jpg', imgROI[0])

imgObj, imgShadow, imgSkeleton = segmentation.obj_shadow_skeleton(imgROI[0])
cv2.imshow("Image Obj", imgObj)
cv2.imshow("Shadow", imgShadow)
cv2.imshow("Image Skeleton", imgSkeleton)


# imgObj, imgSkeleton= process_imgObj(imgROI[0])
# cv2.imshow("Image Obj", imgObj)
# cv2.imwrite('./statictest_pic/imageObj.jpg', imgObj)
# cv2.imshow("Image Skeleton", imgSkeleton)
# imgShadow = segmentation.shadow(imgROI[0], imgObj)
# cv2.imshow("Shadow", imgShadow)
# # imgShadowOnObj = process_imgShadowOnObj(imgObjColor)
# # cv2.imshow("Image Shadow on Object", imgShadowOnObj)

objReconstruct.reconstruct(frame, imgObj, imgSkeleton, imgShadow, posCrop)
ptCloud, volume, length = objReconstruct.reconstructVolume(0.05)

# # objReconstruct.pointCloudChart_3d()

end = time.time()
print("processed time = ", (end - start), "s")

objReconstruct.volumeChart(end - start)

cv2.waitKey(0)
cv2.destroyAllWindows()