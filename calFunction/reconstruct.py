import cv2
import numpy as np
from skimage.morphology import skeletonize
from . import mathTools
from . import segmentation
debug = False

# Reconstruct 3D of Object from shadow,
# height of object is calculated from range of shadow,
# all of edges of images is transform to real world coordinate,
# - finding pseudo skeleton (centroid) of object image
# - detect edges by perform column scanning and transform to real world coordinate,
# -


def reconstruct(imgSample, imgOpening, homographyMatrix, posVirlightImg, posVirlightWorld):
    loop = 0
    # median filter was used to expand and fill some hole
    # imgBin = cv2.blur(imgBin, (3, 3))
    imgObjBin, posCrop = segmentation.obj(
        imgSample, imgOpening)
    cv2.imshow("Object Image", imgObjBin)

    imgShadowBin = segmentation.shadow(imgOpening, imgObjBin)
    cv2.imshow("Shadow Image", imgShadowBin)
    imgSkeleton = skeletonize(imgObjBin, method='lee')
    # imgSkeleton = cv2.dilate(imgSkeleton, np.ones(
    #     (3, 3), np.uint8), iterations=3)
    # imgSkeleton = skeleton(imgObjBin)
    # posImgSkeletonOrigin, posImgSkeletonDestination, imgSkeleton = segmentation.pseudoSkeleton(
    #     imgObjBin)
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
    posSamplingHomo = []
    objHeight = []
    heightShadow = np.empty(imgHeight)
    # scan for all (object: upper, middle and lower edge; shadow lower edge)
    for x in range(posCrop[0], posCrop[0] + posCrop[2]):
        flagObjUpperEdge = False
        flagObjMiddleEdge = False
        flagObjLowerEdge = False
        flagShadowLowerEdge = False
        flagShadowUpperEdge = False
        # for uppper edges
        for y in range(posCrop[1], posCrop[1] + posCrop[3]):
            pixObjVal = imgObjBin.item(y, x)
            pixSkeletonVal = imgSkeleton.item(y, x)
            pixShadowVal = imgShadowBin.item(y, x)
            # xx, yy is origianl position before cropped
            # upper edges detection
            if flagObjUpperEdge == False and pixObjVal > 0:
                flagObjUpperEdge = True
                # save x y coordinate with homogeneous coordiate
                edgeObjUpper.append(np.array([x, y, 1]))
                edgeObjUpperWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]]), 0.2))
                # #  centroid edges (from skeleton image), then lower edges (object image) and then lower edges of shadow (max shadow distance)
            if flagObjMiddleEdge == False and flagObjUpperEdge == True and pixSkeletonVal > 0:
                flagObjMiddleEdge = True
                posCentroid = np.array([x, y, 1])
                posCentroidWorld = mathTools.homographyTransform(
                    homographyMatrix, posCentroid, 0.2)
                edgeObjMiddle.append(posCentroid)
                edgeObjMiddleWorld.append(posCentroidWorld)
                # compute unit vector from centroid position (direction vector related with virtual light position)
                centroid2LightUnitVector = mathTools.unitVector2D(
                    [x, y], posVirlightImg[0:2])
                # scanning to find the maximum shadow distance (shadow lowest edge) with respect with centroid
                # using unit vector for direction reference then interpolate from centroid position until found the maximum shadow edge
                flagShadowLowerEdge = False
                flagShadowUpperEdge = False
                for s in range(0, (imgHeight - 1)):
                    posSampling = np.array(
                        [float(x), float(y)]) + s*centroid2LightUnitVector
                    # print(posSampling)
                    if(posSampling[0] > imgWidth):
                        posSampling[0] = imgWidth - 1
                    if(posSampling[1] > imgHeight):
                        break
                    # append homogeneous coordinate
                    posSamplingHomo = [posSampling[0], posSampling[1], 1.0]
                    if flagShadowLowerEdge == False and imgShadowBin.item(int(posSampling[1]), int(posSampling[0])) > 0:
                        flagShadowLowerEdge = True
                        posShadowLower = np.array(posSamplingHomo)
                        posShadowLowerWorld = mathTools.homographyTransform(
                            homographyMatrix, np.array([[posSampling[0]], [posSampling[1]], [1]]), 0.2)
                        edgesShadowLower.append(posShadowLower)
                        edgesShadowLowerWorld.append(posShadowLowerWorld)
                    if flagShadowLowerEdge == True and flagShadowUpperEdge == False and imgShadowBin.item(int(posSampling[1]), int(posSampling[0])) < 1:
                        flagShadowUpperEdge = True
                        posShadowUpper = np.array(posSamplingHomo)
                        posShadowUpperWorld = mathTools.homographyTransform(
                            homographyMatrix, np.array([[posSampling[0]], [posSampling[1]], [1]]), 0.2)
                        edgesShadowUpper.append(posShadowUpper)
                        edgesShadowUpperWorld.append(posShadowUpperWorld)
                        objHeight.append(mathTools.calHeightFromShadow(
                            posShadowUpper, posCentroid, posShadowUpperWorld, posCentroidWorld, posVirlightWorld))
                        break
            # for lower edges
            if flagObjLowerEdge == False and flagObjUpperEdge == True and pixObjVal < 255:
                flagObjLowerEdge = True
                edgeObjLower.append(np.array([x, y, 1]))
                edgeObjLowerWorld.append(mathTools.homographyTransform(
                    homographyMatrix, np.array([[x], [y], [1]]), 0.2))
        # end experimental
    return np.array(edgeObjUpper), np.array(edgeObjMiddle), np.array(edgeObjLower), np.array(edgeObjUpperWorld), np.array(
        edgeObjMiddleWorld), np.array(edgeObjLowerWorld), np.array(edgesShadowLower), np.array(
            edgesShadowUpper), np.array(edgesShadowLowerWorld), np.array(edgesShadowUpperWorld), np.array(objHeight)


# def reconstruct(imgObjBin, imgShadowBin, posCrop, homographyMatrix, posVirlightImg, posVirlightWorld):
#     loop = 0
#     # median filter was used to expand and fill some hole
#     # imgBin = cv2.blur(imgBin, (3, 3))
#     imgSkeleton = skeletonize(imgObjBin, method='lee')
#     # imgSkeleton = cv2.dilate(imgSkeleton, np.ones(
#     #     (3, 3), np.uint8), iterations=3)
#     # imgSkeleton = skeleton(imgObjBin)
#     # posImgSkeletonOrigin, posImgSkeletonDestination, imgSkeleton = segmentation.pseudoSkeleton(
#     #     imgObjBin)
#     imgHeight, imgWidth = imgObjBin.shape
#     if debug == True:
#         cv2.imshow("Skeleton image", imgSkeleton)
#     # scaning input binary image to detect the object edge
#     # variable declaration
#     edgeObjUpper = []
#     edgeObjUpperWorld = []
#     edgeObjMiddle = []
#     edgeObjMiddleWorld = []
#     edgeObjLower = []
#     edgeObjLowerWorld = []
#     edgesShadowUpper = []
#     edgesShadowUpperWorld = []
#     edgesShadowLower = []
#     edgesShadowLowerWorld = []
#     posSamplingHomo = []
#     objHeight = []
#     heightShadow = np.empty(imgHeight)
#     # scan for all (object: upper, middle and lower edge; shadow lower edge)
#     for x in range(imgWidth - 1):
#         flagObjUpperEdge = False
#         flagObjMiddleEdge = False
#         flagObjLowerEdge = False
#         flagShadowLowerEdge = False
#         flagShadowUpperEdge = False
#         # for uppper edges
#         for y in range(imgHeight - 1):
#             pixObjVal = imgObjBin.item(y, x)
#             pixSkeletonVal = imgSkeleton.item(y, x)
#             pixShadowVal = imgShadowBin.item(y, x)
#             # xx, yy is origianl position before cropped
#             xx = x + posCrop[0]
#             yy = y + posCrop[1]
#             # upper edges detection
#             if flagObjUpperEdge == False and pixObjVal > 0:
#                 flagObjUpperEdge = True
#                 # save x y coordinate with homogeneous coordiate
#                 edgeObjUpper.append(np.array([xx, yy, 1]))
#                 edgeObjUpperWorld.append(mathTools.homographyTransform(
#                     homographyMatrix, np.array([[xx], [yy], [1]]), 0.2))
#                 # #  centroid edges (from skeleton image), then lower edges (object image) and then lower edges of shadow (max shadow distance)
#             if flagObjMiddleEdge == False and flagObjUpperEdge == True and pixSkeletonVal > 0:
#                 flagObjMiddleEdge = True
#                 posCentroid = np.array([xx, yy, 1])
#                 posCentroidWorld = mathTools.homographyTransform(
#                     homographyMatrix, posCentroid, 0.2)
#                 edgeObjMiddle.append(posCentroid)
#                 edgeObjMiddleWorld.append(posCentroidWorld)
#                 # compute unit vector from centroid position (direction vector related with virtual light position)
#                 centroid2LightUnitVector = mathTools.unitVector2D(
#                     [xx, yy], posVirlightImg[0:2])
#                 # scanning to find the maximum shadow distance (shadow lowest edge) with respect with centroid
#                 # using unit vector for direction reference then interpolate from centroid position until found the maximum shadow edge
#                 flagShadowLowerEdge = False
#                 flagShadowUpperEdge = False
#                 for s in range(0, (imgHeight - 1)):
#                     posSampling = np.array(
#                         [float(xx), float(yy)]) + s*centroid2LightUnitVector
#                     # print(posSampling)
#                     if(posSampling[0] > imgWidth):
#                         posSampling[0] = imgWidth - 1
#                     if(posSampling[1] > imgHeight):
#                         break
#                     # append homogeneous coordinate
#                     posSamplingHomo = [posSampling[0], posSampling[1], 1.0]
#                     if flagShadowLowerEdge == False and imgShadowBin.item(int(posSampling[1]), int(posSampling[0])) > 0:
#                         flagShadowLowerEdge = True
#                         posShadowLower = np.array(posSamplingHomo)
#                         posShadowLowerWorld = mathTools.homographyTransform(
#                             homographyMatrix, np.array([[posSampling[0]], [posSampling[1]], [1]]), 0.2)
#                         edgesShadowLower.append(posShadowLower)
#                         edgesShadowLowerWorld.append(posShadowLowerWorld)
#                     if flagShadowLowerEdge == True and flagShadowUpperEdge == False and imgShadowBin.item(int(posSampling[1]), int(posSampling[0])) < 1:
#                         flagShadowUpperEdge = True
#                         posShadowUpper = np.array(posSamplingHomo)
#                         posShadowUpperWorld = mathTools.homographyTransform(
#                             homographyMatrix, np.array([[posSampling[0]], [posSampling[1]], [1]]), 0.2)
#                         edgesShadowUpper.append(posShadowUpper)
#                         edgesShadowUpperWorld.append(posShadowUpperWorld)
#                         objHeight.append(mathTools.calHeightFromShadow(
#                             posShadowUpper, posCentroid, posShadowUpperWorld, posCentroidWorld, posVirlightWorld))
#                         break
#             # for lower edges
#             if flagObjLowerEdge == False and flagObjUpperEdge == True and pixObjVal < 255:
#                 flagObjLowerEdge = True
#                 edgeObjLower.append(np.array([xx, yy, 1]))
#                 edgeObjLowerWorld.append(mathTools.homographyTransform(
#                     homographyMatrix, np.array([[xx], [yy], [1]]), 0.2))
#         # end experimental
#     return np.array(edgeObjUpper), np.array(edgeObjMiddle), np.array(edgeObjLower), np.array(edgeObjUpperWorld), np.array(
#         edgeObjMiddleWorld), np.array(edgeObjLowerWorld), np.array(edgesShadowLower), np.array(
#             edgesShadowUpper), np.array(edgesShadowLowerWorld), np.array(edgesShadowUpperWorld), np.array(objHeight)


def skeleton(imgBin):
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    size = np.size(imgBin)
    skel = np.zeros_like(imgBin)
    eroded = np.zeros_like(imgBin)
    temp = np.zeros_like(imgBin)
    imgOriginal = imgBin.copy()
    while(not done):
        # eroded = cv2.erode(imgOriginal, element)
        # temp = cv2.dilate(eroded, element)
        # temp = cv2.subtract(imgOriginal, temp)
        # skel = cv2.bitwise_or(skel, temp)
        # imgOriginal, eroded = eroded, imgOriginal
        cv2.erode(imgOriginal, element, eroded)
        cv2.dilate(eroded, element, temp)
        cv2.subtract(imgOriginal, temp, temp)
        cv2.bitwise_or(skel, temp, skel)
        imgOriginal, eroded = eroded, imgOriginal

        # zeros = size - cv2.countNonZero(imgBin)
        # if zeros == size:
        #     done = True
        if cv2.countNonZero(imgOriginal) == 0:
            return skel
