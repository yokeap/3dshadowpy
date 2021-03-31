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
    edgeObjMiddle = []
    edgeObjMiddleWorld = []
    edgeObjLower = []
    edgeObjLowerWorld = []
    edgesShadowUpper = []
    edgesShadowUpperWorld = []
    edgesShadowLower = []
    edgesShadowLowerWorld = []
    heightShadow = np.empty(imgHeight)
    # scan for all (object: upper, middle and lower edge; shadow lower edge)
    for x in range(imgWidth):
        flagObjUpperEdge = False
        flagObjMiddleEdge = False
        flagObjLowerEdge = False
        for y in range(imgHeight):
            pixObjVal = imgObjBin.item(y, x)
            pixSkeletonVal = imgSkeleton.item(y, x)
            pixShadowVal = imgShadowBin.item(y, x)
            # upper edges
            if flagObjUpperEdge == False and pixObjVal > 0:
                flagObjUpperEdge = True
                # save x y coordinate with homogeneous coordiate
                edgeObjUpper.append(np.array([x, y, 1]))
                edgeObjUpperWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
            #  centroid edges (from skeleton image), then lower edges (object image) and then lower edges of shadow (max shadow distance)
            if flagObjMiddleEdge == False and flagObjUpperEdge == True and pixSkeletonVal > 0:
                flagObjMiddleEdge = True
                edgeObjMiddle.append(np.array([x, y, 1]))
                edgeObjMiddleWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
                # compute unit vector from centroid position (direction vector related with virtual light position)
                centroid2LightUnitVector = mathTools.unitVector2D(
                    [x, y], virlightPosIMG[0:1])
                # scanning to find the maximum shadow distance (shadow lowest edge) with respect with centroid
                # using unit vector for direction reference then interpolate from centroid position until found the maximum shadow edge
                flagShadowLowerEdge = False
                flagShadowUpperEdge = False
                for s in range(y, imgHeight):
                    posShadow = np.array(
                        [[x], [y]]) + (s*centroid2LightUnitVector)
                    # append homogeneous coordinate
                    posShadow.append(posShadow, [1], axis=1)
                    posShadow = posShadow.T                         # transpose to row matrix
                    if flagShadowLowerEdge == 0 and imgObjBin.item(posShadow[1], posShadow[0]) < 255:
                        flagShadowLowerEdge = 1
                        edgesShadowLower.append(posShadow)
                    if flagShadowUpperEdge == 0 and imgShadowBin.item(posShadow[1], posShadow[0]) < 255:
                        flagShadowUpperEdge = 1
                        edgesShadowUpper.append(posShadow)
                        break
            # for lower edges
            if flagObjLowerEdge == False and flagObjUpperEdge == True and pixObjVal < 255:
                flagObjLowerEdge = True
                edgeObjUpper.append(np.array([x, y, 1]))
                edgeObjUpperWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
                # reset flagObjUpperEdge when found lower edge
                break

    return np.array(edgeObjUpper), np.array(edgeObjMiddle), np.array(edgeObjLower), np.array(edgeObjUpperWorld), np.array(edgeObjLowerWorld)


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
