
from calFunction import segmentation
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

homographyMatrix = np.array([
    [5.079053647431133e-06, -5.475219832828209e-04, 0.224511299503042],
    [- 5.494275672572568e-04, -1.011837140387550e-06, 0.974457649498132],
    [1.174112215996749e-08, -1.921899063852394e-08, -0.005134593677710]
])

virLightPos = np.array(
    [-3.382978646119368e+02, 1.228094975199053e+02, 2.164641969419283e+02])
virLightPosIMG = np.array(
    [2.907071993662571e+03, -2.682554285912778e+03, 2.164641969419283e+02])


def homographyTransform(homographyMatrix, inputMatrix):
    PR = np.multiply(homographyMatrix, inputMatrix)
    newX = PR[0, 0]/PR[2, 0]
    newY = PR[1, 0]/PR[2, 0]
    worldUnit = [newX, newY]
    return worldUnit


def reconstruct(imgObjBin, imgShadowBin):
    count = 0
    # median filter was used to expand and fill some hole
    # imgBin = cv2.blur(imgBin, (3, 3))
    imgObjBin = cv2.medianBlur(imgObjBin, 9)
    if debug == True:
        cv2.imshow("Median Filtering", imgBin)
    imgSkeleton = skeletonize(imgObjBin, method='lee')
    height, width = imgObjBin.shape

    # scan input binary image to detect the object edge
    # variable declaration
    edgeUpper = []
    edgeUpperWorld = []
    edgeLower = []
    edgeLowerWorld = []
    heightShadow = np.empty(height)
    for x in range(width):
        flag = 0
        for y in range(height):
            pixVal = imgObjBin.item(y, x)
            # for upper edge
            if flag == 0 and pixVal > 0:
                flag = 1
                # save x y coordinate with homogeneous coordiate (1)
                edgeUpper.append(np.array([x, y, 1]))
                # edgeUpper[count, 0] = x
                # edgeUpper[count, 1] = y
                # # add homogeneous coordinate
                # edgeUpper[count, 2] = 1
                edgeUpperWorld.append(homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
            if flag == 1 and pixVal < 255:
                edgeLower.append(np.array([x, y, 1]))
                # edgeLower[count, 0] = x
                # edgeLower[count, 1] = y
                # # add homogeneous coordinate
                # edgeLower[count, 2] = 1
                edgeLowerWorld.append(homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))

                count = count + 1
                # reset flag when found lower edge
                flag = 0
                break
    print(edgeLower)
    return np.array(edgeUpper), np.array(edgeLower)


def skeleton(imgBin):
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    size = np.size(imgBin)
    skel = np.zeros_like(imgBin)
    while(not done):
        eroded = cv2.erode(imgBin, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(imgBin, temp)
        skel = cv2.bitwise_or(skel, temp)
        imgBin = eroded.copy()

        zeros = size - cv2.countNonZero(imgBin)
        if zeros == size:
            done = True
    return skel


imgBg = cv2.imread('./sample-image/bg.JPG')
imgSample = cv2.imread('./sample-image/fish.JPG')
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
ret, imgBin = cv2.threshold(imgAnd, 1, 255, cv2.THRESH_BINARY)
imgOpening = cv2.morphologyEx(imgBin, cv2.MORPH_OPEN,
                              np.ones((5, 5), np.uint8))
if debug == True:
    cv2.imshow("Morphology", imgOpening)

imgObj = segmentation.obj(imgSample, diffImageBW)
cv2.imshow("Object Image", imgObj)
imgShadow = segmentation.shadow(imgBin, imgObj)
cv2.imshow("Shadow Image", imgShadow)

#
imgObjEdgeLower, imgObjEdgeUpper = reconstruct(imgObj, imgShadow)
fig = plot.figure()
ax = plot.axes(projection='3d')
print(imgObjEdgeUpper.shape)
ax.plot(imgObjEdgeUpper[:, 0], imgObjEdgeUpper[:, 1],
        imgObjEdgeUpper[:, 2], label='Upper Edge')
ax.plot(imgObjEdgeLower[:, 0], imgObjEdgeLower[:, 1],
        imgObjEdgeLower[:, 2], label='Lower Edge')
ax.legend()
plot.show()

# cv2.imshow("Skeleton Image", imgObjEdgeUpper)


end = time.time()
print("processed time = ", (end - start), "s")
cv2.waitKey(0)
cv2.destroyAllWindows()
