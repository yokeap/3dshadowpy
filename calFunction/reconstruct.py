import cv2
import numpy as np
from skimage.morphology import skeletonize
from . import segmentation
debug = True


def homographyTransform(homographyMatrix, inputMatrix):
    PR = np.multiply(homographyMatrix, inputMatrix)
    newX = PR[0, 0]/PR[2, 0]
    newY = PR[1, 0]/PR[2, 0]
    worldUnit = [newX, newY, 0]
    return worldUnit


#   compute the position of 2-rays intersection
# def rayintersect(originA, originB, unitVectorA, unitVectorB)

#     return poisiton

def reconstruct(imgObjBin, imgShadowBin, homographyMatrix):
    count = 0
    # median filter was used to expand and fill some hole
    # imgBin = cv2.blur(imgBin, (3, 3))
    # imgSkeleton = skeletonize(imgObjBin, method='lee')
    imgSkeleton = segmentation.pseudoSkeleton(imgObjBin)
    height, width = imgObjBin.shape
    if debug == True:
        cv2.imshow("Skeleton image", imgSkeleton)

    # scan input binary image to detect the object edge
    # variable declaration
    edgeUpper = []
    edgeUpperWorld = []
    edgeMiddle = []
    edgeMiddleWorld = []
    edgeLower = []
    edgeLowerWorld = []
    heightShadow = np.empty(height)
    # scan for all (object: upper, middle and lower edge; shadow lower edge)
    for x in range(width):
        flagUpperEdge = False
        flagMiddleEdge = False
        flagLowerEdge = False
        flagShadowEdge = False
        for y in range(height):
            pixObjVal = imgObjBin.item(y, x)
            pixSkeletonVal = imgSkeleton.item(y, x)
            pixShadowVal = imgShadowBin.item(y, x)
            # for upper edge
            if flagUpperEdge == False and pixObjVal > 0:
                flagUpperEdge = True
                # save x y coordinate with homogeneous coordiate (1)
                edgeLower.append(np.array([x, y, 1]))
                # edgeLowerWorld.append(np.append(homographyTransform(
                #     homographyMatrix, np.array([[x], [y], [1]])), 0, axis=0))
                edgeLowerWorld.append(homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
            # for middle of object (from skeleton image)
            if flagUpperEdge == True and flagMiddleEdge == False and pixSkeletonVal > 0:
                flagMiddleEdge = True
                edgeMiddle.append(np.array([x, y, 1]))
                edgeMiddleWorld.append(homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
            # for lower edges
            if flagUpperEdge == True and flagLowerEdge == False and pixObjVal < 255:
                edgeUpper.append(np.array([x, y, 1]))
                edgeUpperWorld.append(homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
                # reset flagUpperEdge when found lower edge
                flagLowerEdge = True
                break

    return np.array(edgeUpper), np.array(edgeMiddle), np.array(edgeLower), np.array(edgeUpperWorld), np.array(edgeLowerWorld)


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
