
from calFunction import maskObject
import cv2
import numpy as np
from skimage import morphology
# import sys
# sys.path.append('./calFunction')

homographyMatrix = np.array([
    [5.079053647431133e-06, -5.475219832828209e-04, 0.224511299503042],
    [- 5.494275672572568e-04, -1.011837140387550e-06, 0.974457649498132],
    [1.174112215996749e-08, -1.921899063852394e-08, -0.005134593677710]
])

virLightPos = np.array(
    [-3.382978646119368e+02, 1.228094975199053e+02, 2.164641969419283e+02])
virLightPosIMG = np.array(
    [2.907071993662571e+03, -2.682554285912778e+03, 2.164641969419283e+02])

imgBg = cv2.imread('./sample-image/DSC_0332.JPG')
imgSample = cv2.imread('./sample-image/DSC_0331.JPG')
imgContour = np.zeros_like(imgSample)

# pre-processing image procedure
diffImage = cv2.cvtColor(imgSample, cv2.COLOR_BGR2GRAY) - \
    cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY)
# diffImage_2 = cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY) - \
#     cv2.cvtColor(imgSample, cv2.COLOR_BGR2GRAY)
cv2.imshow("Subtract Image", diffImage)
# cv2.imshow("Subtract Image 2", diffImage_2)

# medianFilt = cv2.medianBlur(diffImage, 9)
# cv2.imshow("Median Filtering", medianFilt)

opening = cv2.morphologyEx(diffImage, cv2.MORPH_OPEN,
                           np.ones((16, 16), np.uint8))
cv2.imshow("Morphology", opening)

ret, diffImageBW = cv2.threshold(opening, 10, 255, cv2.THRESH_BINARY)
cv2.imshow("Binary", diffImageBW)

# Contour process for segment the object and shadow.
contours, hierarchy = cv2.findContours(
    diffImageBW, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

if len(contours) != 0:
    # find the biggest area of the contour
    big_contour = max(contours, key=cv2.contourArea)
    # draw filled contour on black background
    mask = np.zeros_like(imgSample)
    # mask[:, :] = (255, 0, 0)
    cv2.drawContours(mask, [big_contour], 0, (255, 255, 255), -1)
    cv2.imshow("Mask", mask)

    # apply mask to input image
    # Create a green screen image (background color is used to seperated the object).
    # ie. apple used green screen, mango used red screen.
    greenScreenImage = cv2.bitwise_and(imgSample, mask)
    cv2.imshow("Green Screen Masking Result", greenScreenImage)

    # draw boundary box of objet
    # x, y, w, h = cv2.boundingRect(big_contour)
    # # draw the 'human' contour (in green)
    # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)


# Object and shadow segmentation process
# first, object segment from greenScreenImage
hsvImage = maskObject.segmentObj(greenScreenImage)
cv2.imshow("HSV Image", hsvImage)


print("success")
cv2.waitKey(0)
cv2.destroyAllWindows()
