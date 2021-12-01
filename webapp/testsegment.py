import cv2
import numpy as np
from skimage.morphology import skeletonize
from src import mathTools
from src import segmentation
import matplotlib.pyplot as plt
import os

imgSample = cv2.imread('./capture/2021-11-25 015652.342325/imgraw.jpg')
cv2.imshow("Image Sample", imgSample)
imgMask = cv2.imread('./capture/2021-11-25 015652.342325/imgopening.jpg')
ret, imgMask = cv2.threshold(imgMask, 75, 255, cv2.THRESH_BINARY)
cv2.imshow("Image Mask", imgMask)

imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

# imgContour = np.zeros_like(imgMask)

# contours, hierarchy = cv2.findContours(
#     imgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# cv2.fillPoly(imgContour, pts =[contours], color=(255,255,255))

# cv2.drawContours(imgContour, contours, 0, (255, 255, 255), -1)

# if len(contours) != 0: 
#     cv2.drawContours(imgContour, [contours], 0, (255, 255, 255), thickness=cv2.FILLED)
# boudingRect = []

# for contour in contours:
#     # area = cv2.contourArea(contour)
#     (x, y, w, h) = cv2.boundingRect(contour)
#     boudingRect.append([x, y, w, h])
#     cv2.drawContours(imgContour, [contour], 0, 255, -1)
#     # print(x , ',' , y , ',' , w , ',' , h)
#     # cv2.rectangle(imgContour, (x, y), (x + w, y + h), (255, 255, 255), 2)

imgSegment, posCrop = segmentation.objShadow(
                        imgSample, imgMask)

cv2.imshow("Image Segment", imgSegment)

imgROI = []
for crop in posCrop:
    print(crop)  
    imgROI.append(imgSegment[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]])  
    # imgROI = [imgSegment[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]]]

cv2.imshow("Image crop1", imgROI[0])
cv2.imshow("Image crop2", imgROI[1])

cv2.imwrite(os.path.join("./test" , 'test.jpg'), imgROI[0])

cv2.waitKey(0)
cv2.destroyAllWindows()