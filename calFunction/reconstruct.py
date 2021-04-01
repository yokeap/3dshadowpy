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
    posImgSkeletonOrigin, posImgSkeletonDestination, imgSkeleton = segmentation.pseudoSkeleton(
        imgObjBin)
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
        flagShadowLowerEdge = False
        flagShadowUpperEdge = False
        # for uppper edges
        for y in range(imgHeight):
            pixObjVal = imgObjBin.item(y, x)
            # pixSkeletonVal = imgSkeleton.item(y, x)
            # pixShadowVal = imgShadowBin.item(y, x)
            # upper edges
            if pixObjVal > 0:
                # save x y coordinate with homogeneous coordiate
                edgeObjUpper.append(np.array([x, y, 1]))
                edgeObjUpperWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
                break
            # #  centroid edges (from skeleton image), then lower edges (object image) and then lower edges of shadow (max shadow distance)
            # if flagObjMiddleEdge == False and flagObjUpperEdge == True and pixSkeletonVal > 0:
            #     flagObjMiddleEdge = True
            #     edgeObjMiddle.append(np.array([x, y, 1]))
            #     edgeObjMiddleWorld.append(mathTools.homographyTransform(
            #         homographyMatrix, np.array([[x], [y], [1]])))
            #     # compute unit vector from centroid position (direction vector related with virtual light position)
            #     centroid2LightUnitVector = mathTools.unitVector2D(
            #         [x, y], virlightPosIMG[0:1])
            #     # scanning to find the maximum shadow distance (shadow lowest edge) with respect with centroid
            #     # using unit vector for direction reference then interpolate from centroid position until found the maximum shadow edge
            #     flagShadowLowerEdge = False
            #     flagShadowUpperEdge = False
            #     for s in range(y, imgHeight):
            #         posSampling = np.array(
            #             [[x], [y]]) + (s*centroid2LightUnitVector)
            #         # append homogeneous coordinate
            #         posSampling.append(posSampling, [1], axis=1)
            #         posSampling = posSampling.T                         # transpose to row matrix
            #         if flagShadowLowerEdge == 0 and imgObjBin.item(posSampling[1], posSampling[0]) < 255:
            #             flagShadowLowerEdge = 1
            #             edgesShadowLower.append(posSampling)
            #         if flagShadowUpperEdge == 0 and imgShadowBin.item(posSampling[1], posSampling[0]) < 255:
            #             flagShadowUpperEdge = 1
            #             edgesShadowUpper.append(posSampling)
            #             break
            # for lower edges
            # if flagObjLowerEdge == False and flagObjUpperEdge == True and pixObjVal < 255:
            #     flagObjLowerEdge = True
            #     edgeObjUpper.append(np.array([x, y, 1]))
            #     edgeObjUpperWorld.append(mathTools.homographyTransform(
            #         homographyMatrix, np.array([[x], [y], [1]])))
            #     # reset flagObjUpperEdge when found lower edge
            #     break
        # experimental
        # for lower edges
        # for y in reversed(range(imgHeight)):
        #     pixObjVal = imgObjBin.item(y, x)
        #     if pixObjVal > 0:
        #         # save x y coordinate with homogeneous coordiate
        #         edgeObjLower.append(np.array([x, y, 1]))
        #         edgeObjLowerWorld.append(mathTools.homographyTransform(
        #             homographyMatrix, np.array([[x], [y], [1]])))
        #         break
        # for shadow edges and centroid intersection point
        for y in reversed(range(imgHeight)):
            pixShadowVal = imgObjBin.item(y, x)
            pixObjVal = imgObjBin.item(y, x)
            if pixShadowVal > 0:
                # save x y coordinate with homogeneous coordiate
                edgesShadowUpper.append(np.array([x, y, 1]))
                edgesShadowUpperWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]])))
                # compute unit vector from shadow upper edge position (direction vector related with virtual light position, virtual light position viewing)
                shadow2LightUnitVector = mathTools.unitVector2D(
                    [x, y], virlightPosIMG[0:2])
                # centroidHorizonUnitVector = mathTools.unitVector2D(
                #     posImgSkeletonOrigin, posImgSkeletonDestination)
                # posOriginShadow = [x, y]
                # posOirignCentroid = [0, posImgSkeletonOrigin[1]]
                # intersectPos = mathTools.rayintersect(
                #     posOriginShadow, posOirignCentroid, shadow2LightUnitVector, centroidHorizonUnitVector)
                # intersectPosHomogeneous = np.append(intersectPos, [1], axis=0)
                # edgeObjMiddle.append(intersectPosHomogeneous)
                # edgeObjMiddleWorld.append(mathTools.homographyTransform(
                #     homographyMatrix, np.array([[intersectPosHomogeneous[0]], [intersectPosHomogeneous[1]], [1]])))
                # posSamplingHomo = []
                for s in range(0, y):
                    posSampling = np.array(
                        [x, y]) + (s*shadow2LightUnitVector)
                    # append homogeneous coordinate
                    posSamplingHomo = np.append(posSampling, [1], axis=0)
                    if flagObjLowerEdge == False and imgObjBin.item(int(posSampling[1]), int(posSampling[0])) > 0:
                        flagObjLowerEdge = True
                        edgeObjLower.append(posSamplingHomo)
                        edgeObjLowerWorld.append(mathTools.homographyTransform(
                            homographyMatrix, np.array([[posSamplingHomo[0]], [posSamplingHomo[1]], [1]])))
                        posShadowLowerWorld.append(mathTools.homographyTransform(
                            homographyMatrix, np.array([[posSamplingHomo[0]], [posSamplingHomo[1]], [1]])))
                        break
                    # if flagObjMiddleEdge == False and imgSkeleton.item(int(posSampling[1]), int(posSampling[0])) > 0:
                    #     print(posSampling)
                    #     flagObjMiddleEdge = True
                    #     edgeObjMiddle.append(posSamplingHomo)
                    #     edgeObjMiddleWorld.append(mathTools.homographyTransform(
                    #         homographyMatrix, np.array([[posSamplingHomo[0]], [posSamplingHomo[1]], [posSamplingHomo[2]]])))
                    #     break
                break
        # end experimental
    return np.array(edgeObjUpper), np.array(edgeObjMiddle), np.array(edgeObjLower), np.array(edgeObjUpperWorld), np.array(edgeObjMiddleWorld), np.array(edgeObjLowerWorld)


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
