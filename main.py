
from calFunction import segmentation
import cv2
import numpy as np
from skimage.morphology import skeletonize
import time
# import sys
# sys.path.append('./calFunction')
debug = True


def reconstruct(imgBin):
    # median filter was used to expand and fill some hole
    imgBin = cv2.medianBlur(imgBin, 9)
    if debug == True:
        cv2.imshow("Median Filtering", imgBin)
    imgSkeleton = skeletonize(imgBin, method='lee')
    return imgSkeleton


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

imgBg = cv2.imread('./sample-image/bg.JPG')
imgSample = cv2.imread('./sample-image/fish.JPG')
height, width, channels = imgSample.shape
imgBlack = np.zeros([height, width, 1], dtype=np.uint8)
imgContour = np.zeros_like(imgSample)


# pre-processing image procedure
diffImage = cv2.cvtColor(imgSample, cv2.COLOR_BGR2GRAY) - \
    cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY)
# diffImage = cv2.bitwise_not(diffImage)
if debug == True:
    cv2.imshow("Subtract Image", diffImage)
# cv2.imshow("Subtract Image 2", diffImage_2)

# medianFilt = cv2.medianBlur(diffImage, 9)
# cv2.imshow("Median Filtering", medianFilt)
# # diffImage = cv2.bitwise_not(diffImage)
# opening = cv2.morphologyEx(diffImage, cv2.MORPH_OPEN,
#                            np.ones((5, 5), np.uint8))
# opening = cv2.bitwise_not(opening)
# white = cv2.bitwise_not(imgBlack)
# opening = cv2.bitwise_and(opening, white)
# opening[np.where(opening == [255])] = 0
# if debug == True:
#     cv2.imshow("Morphology", opening)
ret, diffImageBW = cv2.threshold(diffImage, 240, 255, cv2.THRESH_BINARY_INV)
if debug == True:
    cv2.imshow("Binary", diffImageBW)
# imgObj = segmentation.obj(imgSample, diffImageBW)
# cv2.imshow("Object Image", imgObj)
# imgShadow = segmentation.shadow(diffImageBW, imgObj)
# cv2.imshow("Shadow Image", imgShadow)

# imgReconstruct = reconstruct(imgObj)
# cv2.imshow("Skeleton Image", imgReconstruct)

end = time.time()
print("processed time = ", (end - start), "s")
cv2.waitKey(0)
cv2.destroyAllWindows()
