
from calFunction import segmentation, reconstruct
from mpl_toolkits import mplot3d
import cv2
import numpy as np
from skimage.morphology import skeletonize
import matplotlib.pyplot as plot
import time
# import sys
# sys.path.append('./calFunction')
debug = False

# start timer
start = time.time()

homographyMatrix = np.array([
    [5.079053647431133e-06, -5.475219832828209e-04, 0.224511299503042],
    [- 5.494275672572568e-04, -1.011837140387550e-06, 0.974457649498132],
    [1.174112215996749e-08, -1.921899063852394e-08, -0.005134593677710]
])

virLightPos = np.array(
    [-3.382978646119368e+02, 1.228094975199053e+02, 2.164641969419283e+02])
virLightPosIMG = np.array(
    [2.907071993662571e+03, -2.682554285912778e+03, 2.164641969419283e+02])


imgBg = cv2.imread('./sample-image/bg-1.JPG')
imgSample = cv2.imread('./sample-image/fish-1.JPG')
height, width, channels = imgSample.shape
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
                              np.ones((15, 15), np.uint8))
if debug == True:
    cv2.imshow("Morphology", imgOpening)

imgObj = segmentation.obj(imgSample, diffImageBW)
cv2.imshow("Object Image", imgObj)
# imgCentroid = segmentation.pseudoSkeleton(imgObj, imgSample)
# cv2.imshow("Centroid Image", imgCentroid)
imgShadow = segmentation.shadow(imgOpening, imgObj)
cv2.imshow("Shadow Image", imgShadow)

imgMerge = cv2.bitwise_or(imgObj, imgShadow)
cv2.imshow("Image Merge", imgMerge)

imgObjEdgeUpper, imgObjEdgeMiddle, imgObjEdgeLower, worldObjEdgeUpper, worldObjEdgeMiddle, worldObjEdgeLower, imgShadowEdgesLower, imgShadowEdgesUpper, worldShadowEdgesLower, worldShadowEdgesUpper = reconstruct.reconstruct(
    imgObj, imgShadow, homographyMatrix, virLightPosIMG)

end = time.time()
print("processed time = ", (end - start), "s")

# plot upper and lower edge in image coordinate
fig1 = plot.figure()
imageCoordinate = plot.axes(projection='3d')
imageCoordinate.plot(imgObjEdgeUpper[:, 0], imgObjEdgeUpper[:, 1],
                     imgObjEdgeUpper[:, 2], label='Upper Edge')
imageCoordinate.plot(imgObjEdgeMiddle[:, 0], imgObjEdgeMiddle[:, 1],
                     imgObjEdgeMiddle[:, 2], label='Middle Edge')
imageCoordinate.plot(imgObjEdgeLower[:, 0], imgObjEdgeLower[:, 1],
                     imgObjEdgeLower[:, 2], label='Lower Edge')
imageCoordinate.plot(imgShadowEdgesLower[:, 0], imgShadowEdgesLower[:, 1],
                     imgShadowEdgesLower[:, 2], label='Shadow Lower Edge')
imageCoordinate.plot(imgShadowEdgesUpper[:, 0], imgShadowEdgesUpper[:, 1],
                     imgShadowEdgesUpper[:, 2], label='Shadow Upper Edge')
imageCoordinate.legend()

# Upper and lower ege in world coordinate (in mm unit)
fig2 = plot.figure()
worldCoordinate = plot.axes(projection='3d')
worldCoordinate.plot(worldObjEdgeUpper[:, 0], worldObjEdgeUpper[:, 1],
                     worldObjEdgeUpper[:, 2], label='Upper Edge')
worldCoordinate.plot(worldObjEdgeMiddle[:, 0], worldObjEdgeMiddle[:, 1],
                     worldObjEdgeMiddle[:, 2], label='Middle Edge')
worldCoordinate.plot(worldObjEdgeLower[:, 0], worldObjEdgeLower[:, 1],
                     worldObjEdgeLower[:, 2], label='Lower Edge')
worldCoordinate.plot(worldShadowEdgesLower[:, 0], worldShadowEdgesLower[:, 1],
                     worldShadowEdgesLower[:, 2], label='Shadow Lower Edge')
worldCoordinate.plot(worldShadowEdgesUpper[:, 0], worldShadowEdgesUpper[:, 1],
                     worldShadowEdgesUpper[:, 2], label='Shadow Upper Edge')
worldCoordinate.legend()
plot.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
