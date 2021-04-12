
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

objReconstruct = reconstruct.ObjReconstruction(
    imgSample, imgOpening, homographyMatrix, virLightPosIMG, virLightPos, scale)
objReconstruct.reconstruct()


# imgObjEdgeUpper, imgObjEdgeMiddle, imgObjEdgeLower, worldObjEdgeUpper, worldObjEdgeMiddle, worldObjEdgeLower, imgShadowEdgesLower, imgShadowEdgesUpper, worldShadowEdgesLower, worldShadowEdgesUpper, objHeight = reconstruct.reconstruct(
#     imgSample, imgOpening, homographyMatrix, virLightPosIMG, virLightPos)

# worldObjEdgeUpper[:, 2] =

# volumetric visualization constructing
# sectionLeftCloudPoint = [(worldObjEdgeUpper[:, 0]),
#                          (worldObjEdgeUpper[:, 1]), (objHeight[:]/2)]
# sectionRightCloudPoint = [worldObjEdgeLower[:, 0],
#                           worldObjEdgeLower[:, 1], objHeight[:]/2]
# upperCloudPoint = [worldObjEdgeMiddle[:, 0],
#                    worldObjEdgeMiddle[:, 1], objHeight[:]]
# lowerCloudPoint = [worldObjEdgeMiddle[:, 0],
#                    worldObjEdgeMiddle[:, 1], np.zeros(objHeight.shape)]
# sectionLeftCloudPoint = np.array(
#     [(worldObjEdgeUpper[:, 0].tolist()), (worldObjEdgeUpper[:, 1].tolist())]).T
# sectionRightCloudPoint = np.array(
#     [worldObjEdgeLower[:, 0], worldObjEdgeLower[:, 1], objHeight[:]/2])
# upperCloudPoint = np.array(
#     [worldObjEdgeMiddle[:, 0], worldObjEdgeMiddle[:, 1], objHeight[:]])
# LowerCloudPoint = np.array(
#     [worldObjEdgeMiddle[:, 0], worldObjEdgeMiddle[:, 1], np.zeros(objHeight.shape)])

# print(sectionLeftCloudPoint[:][1].tolist())
# sectionLeftCloudPoint = np.array(sectionLeftCloudPoint)

# sectionLeftCloudPoint = np.column_stack(
#     (worldObjEdgeUpper[:, 0], worldObjEdgeUpper[:, 1], objHeight[:].tolist()), dtype='object')

# print(sectionLeftCloudPoint.shape)

end = time.time()
print("processed time = ", (end - start), "s")

objReconstruct.imgChart_3d()
objReconstruct.worldChart_3d()

# plot upper and lower edge in image coordinate

# # Upper and lower ege in world coordinate (in mm unit)
# fig2 = plot.figure()
# worldCoordinate = plot.axes(projection='3d')
# worldCoordinate.scatter(worldObjEdgeUpper[:, 0], worldObjEdgeUpper[:, 1],
#                         worldObjEdgeUpper[:, 2], label='Upper Edge')
# worldCoordinate.scatter(worldObjEdgeMiddle[:, 0], worldObjEdgeMiddle[:, 1],
#                         worldObjEdgeMiddle[:, 2], label='Middle Edge')
# worldCoordinate.scatter(worldObjEdgeLower[:, 0], worldObjEdgeLower[:, 1],
#                         worldObjEdgeLower[:, 2], label='Lower Edge')
# worldCoordinate.scatter(worldShadowEdgesLower[:, 0], worldShadowEdgesLower[:, 1],
#                         worldShadowEdgesLower[:, 2], label='Shadow Lower Edge')
# worldCoordinate.scatter(worldShadowEdgesUpper[:, 0], worldShadowEdgesUpper[:, 1],
#                         worldShadowEdgesUpper[:, 2], label='Shadow Upper Edge')
# # draw line from virtual light source position to head and tail shadow position
# # shadow head
# for i in range(0, imgShadowEdgesUpper.shape[0], 100):
#     worldCoordinate.plot([virLightPos[0], worldShadowEdgesUpper[i, 0]], [virLightPos[1], worldShadowEdgesUpper[i, 1]],
#                          [virLightPos[2], worldShadowEdgesUpper[i, 2]])
# worldCoordinate.set_xlabel('x (mm)')
# worldCoordinate.set_ylabel('y (mm)')
# worldCoordinate.set_zlabel('z (mm)')
# worldCoordinate.legend()

# Volumetric chart
# fig3 = plot.figure()
# volumetricChart = plot.axes(projection='3d')
# volumetricChart.scatter(
#     worldObjEdgeUpper[:, 0], worldObjEdgeUpper[:, 1], objHeight[:], s=[0.1], label='Section left')
# # volumetricChart.scatter(
# #     sectionRightCloudPoint[:][0], sectionRightCloudPoint[:][1], sectionRightCloudPoint[:][2], s=[0.1], label='Section Right')
# # volumetricChart.scatter(
# #     upperCloudPoint[:][0], upperCloudPoint[:][1], upperCloudPoint[:][2], s=[0.1], label='Upper')
# # volumetricChart.scatter(
# #     lowerCloudPoint[:][0], lowerCloudPoint[:][1], lowerCloudPoint[:][2], s=[0.1], label='Lower')
# volumetricChart.set_xlabel('x (mm)')
# volumetricChart.set_ylabel('y (mm)')
# volumetricChart.set_zlabel('z (mm)')
# volumetricChart.legend()

# plot.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
