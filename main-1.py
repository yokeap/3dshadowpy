
from calFunction import segmentation, reconstruct
from mpl_toolkits import mplot3d
import cv2
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

imgObjEdgeUpper, imgObjEdgeMiddle, imgObjEdgeLower, worldObjEdgeUpper, worldObjEdgeMiddle, worldObjEdgeLower, imgShadowEdgesLower, imgShadowEdgesUpper, worldShadowEdgesLower, worldShadowEdgesUpper, objHeight = reconstruct.reconstruct(
    imgSample, imgOpening, homographyMatrix, virLightPosIMG, virLightPos)

end = time.time()
print("processed time = ", (end - start), "s")

# plot upper and lower edge in image coordinate
fig1 = plot.figure()
imageCoordinate = plot.axes(projection='3d')

imageCoordinate.scatter(imgObjEdgeUpper[:, 0], imgObjEdgeUpper[:, 1],
                        imgObjEdgeUpper[:, 2], s=[0.1], label='Upper Edge')
imageCoordinate.scatter(imgObjEdgeMiddle[:, 0], imgObjEdgeMiddle[:, 1],
                        imgObjEdgeMiddle[:, 2], s=[0.1], label='Middle Edge')
imageCoordinate.scatter(imgObjEdgeLower[:, 0], imgObjEdgeLower[:, 1],
                        imgObjEdgeLower[:, 2], s=[0.1], label='Lower Edge')
imageCoordinate.scatter(imgShadowEdgesLower[:, 0], imgShadowEdgesLower[:, 1],
                        imgShadowEdgesLower[:, 2], s=[0.1], label='Shadow Lower Edge')
imageCoordinate.scatter(imgShadowEdgesUpper[:, 0], imgShadowEdgesUpper[:, 1],
                        imgShadowEdgesUpper[:, 2], s=[0.1], label='Shadow Upper Edge')
# draw line from virtual light source position to head and tail shadow position
# shadow head
for i in range(0, imgShadowEdgesUpper.shape[0], 100):
    imageCoordinate.plot([virLightPosIMG[0], imgShadowEdgesUpper[i, 0]], [virLightPosIMG[1], imgShadowEdgesUpper[i, 1]],
                         [virLightPosIMG[2], imgShadowEdgesUpper[i, 2]])
# # shadow tail
# imageCoordinate.plot([virLightPosIMG[0], imgShadowEdgesUpper[imgShadowEdgesUpper.shape[0] - 1, 0]], [virLightPosIMG[1], imgShadowEdgesUpper[imgShadowEdgesUpper.shape[0] - 1, 1]],
#                      [virLightPosIMG[2], imgShadowEdgesUpper[imgShadowEdgesUpper.shape[0] - 1, 2]])
imageCoordinate.set_xlabel('x (Pixels)')
imageCoordinate.set_ylabel('y (Pixels)')
imageCoordinate.set_zlabel('z (mm)')
imageCoordinate.legend()

# Upper and lower ege in world coordinate (in mm unit)
fig2 = plot.figure()
worldCoordinate = plot.axes(projection='3d')
worldCoordinate.scatter(worldObjEdgeUpper[:, 0], worldObjEdgeUpper[:, 1],
                        worldObjEdgeUpper[:, 2], label='Upper Edge')
worldCoordinate.scatter(worldObjEdgeMiddle[:, 0], worldObjEdgeMiddle[:, 1],
                        worldObjEdgeMiddle[:, 2], label='Middle Edge')
worldCoordinate.scatter(worldObjEdgeLower[:, 0], worldObjEdgeLower[:, 1],
                        worldObjEdgeLower[:, 2], label='Lower Edge')
worldCoordinate.scatter(worldShadowEdgesLower[:, 0], worldShadowEdgesLower[:, 1],
                        worldShadowEdgesLower[:, 2], label='Shadow Lower Edge')
worldCoordinate.scatter(worldShadowEdgesUpper[:, 0], worldShadowEdgesUpper[:, 1],
                        worldShadowEdgesUpper[:, 2], label='Shadow Upper Edge')
# draw line from virtual light source position to head and tail shadow position
# shadow head
for i in range(0, imgShadowEdgesUpper.shape[0], 100):
    worldCoordinate.plot([virLightPos[0], worldShadowEdgesUpper[i, 0]], [virLightPos[1], worldShadowEdgesUpper[i, 1]],
                         [virLightPos[2], worldShadowEdgesUpper[i, 2]])
worldCoordinate.set_xlabel('x (mm)')
worldCoordinate.set_ylabel('y (mm)')
worldCoordinate.set_zlabel('z (mm)')
worldCoordinate.legend()
plot.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
