import numpy as np
import cv2

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
imContour = imgSample.copy()

# pre-processing image procedure
diffImage = cv2.cvtColor(imgBg, cv2.COLOR_BGR2GRAY) - \
    cv2.cvtColor(imgSample, cv2.COLOR_BGR2GRAY)
cv2.imshow("Subtract Image", diffImage)
# medianFilt = cv2.medianBlur(diffImage, 5)
# cv2.imshow("Median Filtering", medianFilt)

# ret, diffImageBW = cv2.threshold(medianFilt, 10, 20, cv2.THRESH_BINARY)
# cv2.imshow("Binary", diffImageBW)
opening = cv2.morphologyEx(diffImage, cv2.MORPH_OPEN,
                           np.ones((16, 16), np.uint8))

ret, diffImageBW = cv2.threshold(opening, 0, 200, cv2.THRESH_BINARY)
cv2.imshow("Binary", diffImageBW)

# contours, hierarchy = cv2.findContours(
#     diffImageBW, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# if len(contours) != 0:
#     # the contours are drawn here
#     cv2.drawContours(imContour, contours, -1, 255, 3)

#     # find the biggest area of the contour
#     c = max(contours, key=cv2.contourArea)

#     x, y, w, h = cv2.boundingRect(c)
#     # draw the 'human' contour (in green)
#     cv2.rectangle(imContour, (x, y), (x+w, y+h), (0, 255, 0), 2)

# print(ret)
cv2.imshow("Image Show", opening)
cv2.waitKey(0)
cv2.destroyAllWindows()
