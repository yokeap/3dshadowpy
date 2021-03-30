import cv2
import numpy as np
from skimage.morphology import skeletonize
from . import mathTools
from . import segmentation
debug = True

#   compute the position of 2-rays intersection
# def rayintersect(originA, originB, unitVectorA, unitVectorB)

#     return poisiton

# Reconstruct 3D of Object from shadow,
# height of object is calculated from range of shadow,
# all of edges of images is transform to real world coordinate,
# - finding pseudo skeleton (centroid) of object image
# - detect edges by perform column scanning and transform to real world coordinate,
# -


def reconstruct(imgObjBin, imgShadowBin, homographyMatrix, virlightPosIMG):
    count = 0
    # median filter was used to expand and fill some hole
    # imgBin = cv2.blur(imgBin, (3, 3))
    # imgSkeleton = skeletonize(imgObjBin, method='lee')
    imgSkeleton = segmentation.pseudoSkeleton(imgObjBin)
    imgHeight, imgWidth = imgObjBin.shape
    if debug == True:
        cv2.imshow("Skeleton image", imgSkeleton)

    # scaning input binary image to detect the object edge
    # variable declaration
    edgeObjUpper = []
    edgeObjUpperWorld = []
    edgeMiddle = []
    edgeMiddleWorld = []
    edgeLower = []
    edgeLowerWorld = []
    heightShadow = np.empty(imgHeight)
    # scan for all (object: upper, middle and lower edge; shadow lower edge)
    for x in range(imgWidth):
        flagUpperEdge = False
        flagMiddleEdge = False
        flagLowerEdge = False
        flagShadowEdge = False
        for y in range(imgHeight):
            pixObjVal = imgObjBin.item(y, x)
            pixSkeletonVal = imgSkeleton.item(y, x)
            pixShadowVal = imgShadowBin.item(y, x)
            # upper edges
            if flagUpperEdge == False and pixObjVal > 0:
                flagUpperEdge = True
                # save x y coordinate with homogeneous coordiate
                edgeObjUpper.append(np.array([x, y, 1]))
                edgeObjUpperWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
            #  centroid edges (from skeleton image), then lower edges (object image) and then lower edges of shadow (max shadow distance)
            if flagMiddleEdge == False and flagUpperEdge == True and pixSkeletonVal > 0:
                flagMiddleEdge = True
                edgeMiddle.append(np.array([x, y, 1]))
                edgeMiddleWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
                # compute unit vector from centroid position (direction vector related with virtual light position)
                centroid2LightUnitVector = mathTools.unitVector2D(
                    [x, y], virlightPosIMG[0:1])
                # scanning to find the maximum shadow distance (shadow lowest edge) with respect with centroid
                # using unit vector for direction reference then interpolate from centroid position until found the maximum shadow edge
                for s in range(y, imgHeight):
                    posShadow = np.array(
                        [[x], [y]]) + (s*centroid2LightUnitVector)

            # # for lower edges
            # if flagLowerEdge == False and flagUpperEdge == True and pixObjVal < 255:
            #     flagLowerEdge = True
            #     edgeObjUpper.append(np.array([x, y, 1]))
            #     edgeObjUpperWorld.append(mathTools.homographyTransform(
            #         homographyMatrix, np.array([[x], [y], [1]])))
            #     # reset flagUpperEdge when found lower edge
            #     break

    return np.array(edgeObjUpper), np.array(edgeMiddle), np.array(edgeLower), np.array(edgeObjUpperWorld), np.array(edgeLowerWorld)


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
