# this is calculation base on shadow on object and use 4 points spline estimation from upper and lower, mirror upper
# and lower points are calculate from upper or lower point from height estimate of ray casting from shadow on object. 
from calFunction import segmentation, reconstruct
from mpl_toolkits import mplot3d
import cv2
import os
import datetime
import numpy as np
from skimage.morphology import skeletonize
import matplotlib.pyplot as plot
import time
# import sys
# sys.path.append('./calFunction')
debug = True

# start timer
start = time.time()

scale = 0.2  # percent of original size

homographyMatrix = np.array([
    [5.079053647431133e-06, -5.475219832828209e-04, 0.224511299503042],
    [- 5.494275672572568e-04, -1.011837140387550e-06, 0.974457649498132],
    [1.174112215996749e-08, -1.921899063852394e-08, -0.005134593677710]
])

virLightPos = np.array(
    [-3.382978646119368e+02, 1.228094975199053e+02, 2.164641969419283e+02])
virLightPosIMG = np.array(
    [2.907071993662571e+03, -2.682554285912778e+03, 2.164641969419283e+02])


# homographyMatrix = homographyMatrix * scale

# virLightPos = virLightPos * scale
virLightPosIMG = virLightPosIMG * scale

imgBg = cv2.imread('./sample-image/bg-1.JPG')
imgSample = cv2.imread('./sample-image/fish-1.JPG')

height, width, channels = imgSample.shape
height = int(height * scale)
width = int(width * scale)
imgBg = cv2.resize(imgBg, (width, height))
imgSample = cv2.resize(imgSample, (width, height))
imgBlack = np.zeros([height, width, 1], dtype=np.uint8)
imgContour = np.zeros_like(imgSample)

# pre-processing image procedure
# output is only object and shadow in binary
diffImage = cv2.cvtColor(imgSample, cv2.COLOR_BGR2GRAY) - \
    cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY)
# diffImage = cv2.bitwise_not(diffImage)
if debug == True:
    cv2.imshow("Subtract Image", diffImage)
ret, diffImageBW = cv2.threshold(diffImage, 240, 255, cv2.THRESH_BINARY_INV)
if debug == True:
    cv2.imshow("Binary", diffImageBW)
imgAnd = cv2.bitwise_and(diffImageBW, diffImage)
if debug == True:
    cv2.imshow("Image And", imgAnd)
ret, imgBin = cv2.threshold(imgAnd, 50, 255, cv2.THRESH_BINARY)
imgOpening = cv2.morphologyEx(imgBin, cv2.MORPH_OPEN,
                              np.ones((3, 3), np.uint8))
imgOpening = cv2.medianBlur(imgOpening, 9)
if debug == True:
    cv2.imshow("Morphology", imgOpening)

imgSegmentSource, imgSegmentBlack, imgROI, posCrop = segmentation.objShadow(
    imgSample, imgOpening)
print(posCrop[0])
if debug == True:
    cv2.imshow("ROI", imgROI[0])

imgObj, imgObjColor = segmentation.obj(imgROI[0])
if debug == True:
    cv2.imshow("Object Image", imgObj)

imgShadow = segmentation.shadow(imgROI[0], imgObj)
if debug == True:
    cv2.imshow("Shadow Image", imgShadow)

imgShadowOnObj = segmentation.shadowEdgeOnObj(imgObjColor)
if debug == True:
    cv2.imshow("Shadow On Obj", imgShadowOnObj)

objReconstruct = reconstruct.ObjReconstruction(
    imgSample, homographyMatrix, virLightPosIMG, virLightPos, scale)
objReconstruct.reconstruct(imgObj, imgShadowOnObj, imgShadow , posCrop)
objReconstruct.reconstructVolume(0.05)


# p = os.path.sep.join(
#     ['capture', "shot_{}.jpg".format(str(datetime.datetime.now()).replace(":", ''))])
# cv2.imwrite(p, imgObjColor)

# objReconstruct = reconstruct.ObjReconstruction(
#     imgSample, imgOpening, homographyMatrix, virLightPosIMG, virLightPos, scale)
# objReconstruct.reconstruct()
# objReconstruct.reconstructVolume(0.05)


end = time.time()
print("processed time = ", (end - start), "s")


# objReconstruct.imgChart_3d()
# objReconstruct.worldChart_3d()
# objReconstruct.pointCloudChart_3d()

objReconstruct.volumeChart(end - start)


cv2.waitKey(0)
cv2.destroyAllWindows()
