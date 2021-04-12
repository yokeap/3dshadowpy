import cv2
import numpy as np
from skimage.morphology import skeletonize
from . import mathTools
from . import segmentation
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plot

debug = False

# Reconstruct 3D of Object from shadow,
# height of object is calculated from range of shadow,
# all of edges of images is transform to real world coordinate,
# - finding pseudo skeleton (centroid) of object image
# - detect edges by perform column scanning and transform to real world coordinate,
# -


class ObjReconstruction:
    def __init__(self, imgSample, imgOpening, homographyMatrix, posVirlightIMG, posVirlightWorld, scale):
        self.imgSample = imgSample
        self.imgOpening = imgOpening
        self.homographyMatrix = homographyMatrix
        self.posVirlightIMG = posVirlightIMG
        self.posVirlightWorld = posVirlightWorld
        height, width, channel = imgSample.shape
        self.ptCloudSectionLeft = np.empty((height, 3))
        self.ptCloudSectionRight = np.empty((height, 3))
        self.ptCloudObjHeightUpper = np.empty((height, 3))
        self.ptCloudObjHeightLower = np.empty((height, 3))
        # self.ptCloudSectionLeft = np.array((height, 3))
        # self.ptCloudSectionRight = np.array((height, 3))
        # self.ptCloudObjHeightUpper = np.array((height, 3))
        print(self.ptCloudSectionLeft.shape)
        self.scale = scale

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

    def reconstruct(self):
        loop = 0
        # median filter was used to expand and fill some hole
        # imgBin = cv2.blur(imgBin, (3, 3))
        imgObjBin, posCrop = segmentation.obj(
            self.imgSample, self.imgOpening)
        cv2.imshow("Object Image", imgObjBin)

        imgShadowBin = segmentation.shadow(self.imgOpening, imgObjBin)
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
        self.edgeObjUpper = []
        self.edgeObjUpperWorld = []
        self.edgeObjMiddle = []
        self.edgeObjMiddleWorld = []
        self.edgeObjLower = []
        self.edgeObjLowerWorld = []
        self.edgesShadowUpper = []
        self.edgesShadowUpperWorld = []
        self.edgesShadowLower = []
        self.edgesShadowLowerWorld = []
        # self.ptCloudObjHeightUpper=[]
        self.heightShadow = np.empty(imgHeight)
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
                    # edgeObjUpper.append(np.array([x, y, 1]))
                    # edgeObjUpperWorld.append(mathTools.homographyTransform(
                    #     homographyMatrix, [x, y, 1], 0.2))]
                    posUpper = [x, y, 1]
                    posUpperWorld = mathTools.homographyTransform(
                        self.homographyMatrix, posUpper, self.scale)
                    self.edgeObjUpper.append(np.array(posUpper))
                    self.edgeObjUpperWorld.append(posUpperWorld)
                    self.ptCloudSectionLeft[loop, :] = posUpperWorld
                    # #  centroid edges (from skeleton image), then lower edges (object image) and then lower edges of shadow (max shadow distance)
                if flagObjMiddleEdge == False and flagObjUpperEdge == True and pixSkeletonVal > 0:
                    flagObjMiddleEdge = True
                    posCentroid = [x, y, 1]
                    posCentroidWorld = mathTools.homographyTransform(
                        self.homographyMatrix, posCentroid, self.scale)
                    self.edgeObjMiddle.append(np.array(posCentroid))
                    self.edgeObjMiddleWorld.append(posCentroidWorld)
                    self.ptCloudObjHeightUpper[loop, :] = posCentroidWorld
                    self.ptCloudObjHeightLower[loop, :] = posCentroidWorld
                    # compute unit vector from centroid position (direction vector related with virtual light position)
                    centroid2LightUnitVector = mathTools.unitVector2D(
                        [x, y], self.posVirlightIMG[0:2])
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
                        if flagShadowLowerEdge == False and imgShadowBin.item(int(posSampling[1]), int(posSampling[0])) > 0:
                            flagShadowLowerEdge = True
                            # add 1.0 as homogeneous coordinate
                            posShadowLower = [
                                posSampling[0], posSampling[1], 1.0]
                            posShadowLowerWorld = mathTools.homographyTransform(
                                self.homographyMatrix, posShadowLower, self.scale)
                            self.edgesShadowLower.append(
                                np.array(posShadowLower))
                            self.edgesShadowLowerWorld.append(
                                posShadowLowerWorld)
                            # self.ptCloudSectionRight[loop,
                            #                          :] = posShadowLowerWorld
                        if flagShadowLowerEdge == True and flagShadowUpperEdge == False and imgShadowBin.item(int(posSampling[1]), int(posSampling[0])) < 1:
                            flagShadowUpperEdge = True
                            posShadowUpper = [
                                posSampling[0], posSampling[1], 1.0]
                            posShadowUpperWorld = mathTools.homographyTransform(
                                self.homographyMatrix, posShadowUpper, self.scale)
                            self.edgesShadowUpper.append(
                                np.array(posShadowUpper))
                            self.edgesShadowUpperWorld.append(
                                posShadowUpperWorld)
                            skeletonHeight = mathTools.calHeightFromShadow(
                                posShadowUpper, posCentroid, posShadowUpperWorld, posCentroidWorld, self.posVirlightWorld)
                            self.ptCloudSectionLeft[loop,
                                                    2] = skeletonHeight / 2
                            self.ptCloudSectionRight[loop,
                                                     2] = skeletonHeight / 2
                            self.ptCloudObjHeightUpper[loop,
                                                       2] = skeletonHeight
                            self.ptCloudObjHeightLower[loop,
                                                       2] = 0
                            loop = loop + 1
                            break
                # for lower edges
                if flagObjLowerEdge == False and flagObjUpperEdge == True and pixObjVal < 255:
                    flagObjLowerEdge = True
                    posLower = [x, y, 1]
                    posLowerWorld = mathTools.homographyTransform(
                        self.homographyMatrix, posLower, 0.2)
                    self.edgeObjLower.append(np.array(posLower))
                    self.edgeObjLowerWorld.append(posLowerWorld)
                    self.ptCloudSectionRight[loop, 0] = posLowerWorld[0]
                    self.ptCloudSectionRight[loop, 1] = posLowerWorld[1]
                    break

    def imgChart_3d(self):
        imgObjEdgeUpper = np.array(self.edgeObjUpper)
        imgObjEdgeMiddle = np.array(self.edgeObjMiddle)
        imgObjEdgeLower = np.array(self.edgeObjLower)
        imgShadowEdgesUpper = np.array(self.edgesShadowUpper)
        imgShadowEdgesLower = np.array(self.edgesShadowLower)

        figIMG = plot.figure()
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
            imageCoordinate.plot([self.posVirlightIMG[0], imgShadowEdgesUpper[i, 0]], [self.posVirlightIMG[1], imgShadowEdgesUpper[i, 1]],
                                 [self.posVirlightIMG[2], imgShadowEdgesUpper[i, 2]])
        imageCoordinate.set_xlabel('x (Pixels)')
        imageCoordinate.set_ylabel('y (Pixels)')
        imageCoordinate.set_zlabel('z (mm)')
        imageCoordinate.legend()

        figIMG.show()

    def worldChart_3d(self):
        worldObjEdgeUpper = np.array(self.edgeObjUpperWorld)
        worldObjEdgeMiddle = np.array(self.edgeObjMiddleWorld)
        worldObjEdgeLower = np.array(self.edgeObjLowerWorld)
        worldShadowEdgesUpper = np.array(self.edgesShadowUpperWorld)
        worldShadowEdgesLower = np.array(self.edgesShadowLowerWorld)

        figWorld = plot.figure()
        worldCoordinate = plot.axes(projection='3d')
        worldCoordinate.scatter(worldObjEdgeUpper[:, 0], worldObjEdgeUpper[:, 1],
                                worldObjEdgeUpper[:, 2], s=[0.1], label='Upper Edge')
        worldCoordinate.scatter(worldObjEdgeMiddle[:, 0], worldObjEdgeMiddle[:, 1],
                                worldObjEdgeMiddle[:, 2], s=[0.1], label='Middle Edge')
        worldCoordinate.scatter(worldObjEdgeLower[:, 0], worldObjEdgeLower[:, 1],
                                worldObjEdgeLower[:, 2], s=[0.1], label='Lower Edge')
        worldCoordinate.scatter(worldShadowEdgesLower[:, 0], worldShadowEdgesLower[:, 1],
                                worldShadowEdgesLower[:, 2], s=[0.1], label='Shadow Lower Edge')
        worldCoordinate.scatter(worldShadowEdgesUpper[:, 0], worldShadowEdgesUpper[:, 1],
                                worldShadowEdgesUpper[:, 2], s=[0.1], label='Shadow Upper Edge')
        # draw line from virtual light source position to head and tail shadow position
        # shadow head
        for i in range(0, worldShadowEdgesUpper.shape[0], 100):
            worldCoordinate.plot([self.posVirlightWorld[0], worldShadowEdgesUpper[i, 0]], [self.posVirlightWorld[1], worldShadowEdgesUpper[i, 1]],
                                 [self.posVirlightWorld[2], worldShadowEdgesUpper[i, 2]])
        worldCoordinate.set_xlabel('x (mm)')
        worldCoordinate.set_ylabel('y (mm)')
        worldCoordinate.set_zlabel('z (mm)')
        worldCoordinate.legend()

        figWorld.show()

    def volumeChart_3d(self):
        figVolume = plot.figure()
        volumeChart = plot.axes(projection='3d')

        volumeChart.scatter(self.ptCloudSectionLeft[:, 0], self.ptCloudSectionLeft[:, 1],
                            self.ptCloudSectionLeft[:, 2], s=[0.1], label='Section Left')
        volumeChart.scatter(self.ptCloudSectionRight[:, 0], self.ptCloudSectionRight[:, 1],
                            self.ptCloudSectionRight[:, 2], s=[0.1], label='Section Right')
        volumeChart.scatter(self.ptCloudObjHeightUpper[:, 0], self.ptCloudObjHeightUpper[:, 1],
                            self.ptCloudObjHeightUpper[:, 2], s=[0.1], label='Section Middle Upper')
        volumeChart.scatter(self.ptCloudObjHeightLower[:, 0], self.ptCloudObjHeightLower[:, 1],
                            self.ptCloudObjHeightLower[:, 2], s=[0.1], label='Section Middle Lower')

        volumeChart.set_xlabel('x (mm)')
        volumeChart.set_ylabel('y (mm)')
        volumeChart.set_zlabel('z (mm)')
        volumeChart.legend()

        figVolume.show()
