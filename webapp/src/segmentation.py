import cv2
import numpy as np
import math
from . import mathTools

debug = True


def draw_angled_rec(x0, y0, width, height, angle, img):

    _angle = math.radians(90-angle)
    b = math.cos(_angle) * 0.5
    a = math.sin(_angle) * 0.5
    posOrigin = (int(x0 - a * height - b * width),
                 int(y0 + b * height - a * width))
    posDestination = (int(x0 + a * height - b * width),
                      int(y0 - b * height - a * width))
    pt2 = (int(2 * x0 - posOrigin[0]), int(2 * y0 - posOrigin[1]))
    pt3 = (int(2 * x0 - posDestination[0]), int(2 * y0 - posDestination[1]))

    cv2.line(img, posOrigin, posDestination, (0, 0, 255), 1)
    cv2.line(img, posDestination, pt2, (0, 0, 255), 1)
    cv2.line(img, pt2, pt3, (0, 0, 255), 1)
    cv2.line(img, pt3, posOrigin, (0, 0, 255), 1)
    return img

def objShadow(imgSource, imgOpening):
    x = 0
    y = 0
    w = 0
    h = 0
    margin = 60
    boudingRect = []
    imgArrayROI = []

    imgInput = imgSource

    imgMaskRGB = np.zeros_like(imgInput)
    imgMaskRGB[:, :, 0] = imgOpening
    imgMaskRGB[:, :, 1] = imgOpening
    imgMaskRGB[:, :, 2] = imgOpening

    imgSegmentBlackColor = cv2.bitwise_and(imgInput, imgMaskRGB)

    contours, hierarchy = cv2.findContours(
        imgOpening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        OriginX = x - round(margin / 2)
        OriginY = y - round(margin / 2)
        Width = w + margin
        Height = h + margin
        # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)
        boudingRect.append([OriginX, OriginY, Width, Height])
        cv2.rectangle(imgInput, (OriginX, OriginY), (x + Width, y + Height), (255, 255, 255), 2)
        imgArrayROI.append(imgSegmentBlackColor[OriginY:OriginY + Height, OriginX:OriginX + Width])  
    
    return imgInput, imgSegmentBlackColor, imgArrayROI, boudingRect

def obj(imgROI, imgHSV, hue, saturation, value):
    # Define thresholds for channel 1 based on histogram settings
    channel1Min = int(float(hue["min"]) * 360)
    channel1Max = int(float(hue["max"]) * 360)

    # Define thresholds for channel 2 based on histogram settings
    channel2Min = int(float(saturation["min"]) * 255)
    channel2Max = int(float(saturation["max"]) * 255)

    # Define thresholds for channel 3 based on histogram settings
    channel3Min = int(float(value["min"]) * 255)
    channel3Max = int(float(value["max"]) * 255)

    imgObj = np.zeros_like(imgROI)
    # imgHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
    imgObj = cv2.inRange(
        imgHSV, (channel1Min, channel2Min, channel3Min), (channel1Max, channel2Max, channel3Max))
    contours, hierarchy = cv2.findContours(
        imgObj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) != 0:
        # find the biggest area of the contour
        big_contour = max(contours, key=cv2.contourArea)
    cv2.drawContours(imgObj, [big_contour], 0, (255, 255, 255), -1)
    # imgObj = cv2.morphologyEx(imgObj, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)
    # masking process for image object with black backgroubd color
    imgMask = np.zeros_like(imgROI)
    imgMask[:, :, 0] = imgObj
    imgMask[:, :, 1] = imgObj
    imgMask[:, :, 2] = imgObj
    imgObjColor = cv2.bitwise_and(imgMask, imgROI)
    return imgObj, imgObjColor


def shadow(imgROI, imgObj):
    imgShadow = np.zeros_like(imgObj)
    imgROI = cv2.cvtColor(imgROI, cv2.COLOR_BGR2GRAY)
    ret, imgROI = cv2.threshold(imgROI, 1, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Input Shadow Image", imgROI)
    imgShadow = cv2.bitwise_xor(imgObj, imgROI)
    # cv2.imshow("EX OR", imgShadow)
    imgShadow = cv2.morphologyEx(imgShadow, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=1)

    # imgShadow = cv2.erode(imgShadow, np.ones((5, 5), np.uint8), iterations=1)
    # imgShadow = cv2.dilate(imgShadow, np.ones((5, 5), np.uint8), iterations=1)
    # contours, hierarchy = cv2.findContours(
    #     imgShadow, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Contour filtering to get largest area
    # area_thresh = 0
    # for c in contours:
    #     area = cv2.contourArea(c)
    #     if area > area_thresh:
    #         area = area_thresh
    #         big_contour = c
    # imgOut= np.zeros_like(imgObj)
    # if len(contours) != 0:
    #     # find the biggest area of the contour
    #     big_contour = max(contours, key=cv2.contourArea)
        
        # x, y, w, h = cv2.boundingRect(big_contour)
        # imgShadow = cv2.medianBlur(imgShadow, 9)
        # cropped_contour = imgShadow[y:y+h, x:x+w]
        # imgShadow = cv2.morphologyEx(imgShadow, cv2.MORPH_OPEN,
        #                              np.ones((15, 15), np.uint8))
    # cv2.drawContours(imgShadow, big_contour, 0, 255, 1)
    return imgShadow


def OpeningObj(img):
    # Define thresholds for channel 1 based on histogram settings
    channel1Min = 0.189 * 360
    channel1Max = 0.522 * 360

    # Define thresholds for channel 2 based on histogram settings
    channel2Min = 0.209 * 255
    channel2Max = 1.000 * 255

    # Define thresholds for channel 3 based on histogram settings
    channel3Min = 0.157 * 255
    channel3Max = 1.000 * 255

    imgOpeninged = np.zeros_like(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    imgOpeninged = cv2.inRange(
        hsv, (channel1Min, channel2Min, channel3Min), (channel1Max, channel2Max, channel3Max))
    return imgOpeninged


def pseudoSkeleton(imgObj):
    imgPseudoSkel = np.zeros_like(imgObj)
    contours, hierarchy = cv2.findContours(
        imgObj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest area of the contour
        big_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(imgObj, [big_contour], 0, 255, -1)

        # find centroid by image moment
        M = cv2.moments(big_contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # cv2.circle(imgOriginal, (cx, cy), 5, (255, 0, 0), -1)

        ellipse = cv2.fitEllipse(big_contour)
        rect = cv2.minAreaRect(big_contour)
        # calculate vertices point for ellipsoid
        # first, calculate vector angle
        ellipseVectorAngleX = (ellipse[1][1]/2) * \
            math.cos(math.radians(90 - ellipse[2]))
        ellipseVectorAngleY = (ellipse[1][1]/2) * \
            math.sin(math.radians(90 - ellipse[2]))
        # left side
        ellipseVerticeLeftX = ellipse[0][0] - ellipseVectorAngleX
        ellipseVerticeLeftY = ellipse[0][1] - ellipseVectorAngleY
        # right side
        ellipseVerticeRightX = ellipse[0][0] + ellipseVectorAngleX
        ellipseVerticeRightY = ellipse[0][1] + ellipseVectorAngleY
        # calculate vertices point for rectangle (in half length)
        # first, calculate vector angle
        rectVectorAngleX = (rect[1][1]/2) * \
            math.cos(math.radians(90 - rect[2]))
        rectVectorAngleY = (rect[1][1]/2) * \
            math.sin(math.radians(90 - rect[2]))
        # left side
        rectHalfVerticesLeftX = rect[0][0] - rectVectorAngleX
        rectHalfVerticesLeftY = rect[0][1] - rectVectorAngleY
        # right side
        rectHalfVerticesRightX = rect[0][0] + rectVectorAngleX
        rectHalfVerticesRightY = rect[0][1] + rectVectorAngleY

        # cv2.ellipse(imgOriginal, ellipse, (255, 0, 0), 1)
        # cv2.circle(imgOriginal, (int(ellipseVerticeLeftX), int(ellipseVerticeLeftY)),
        #            5, (255, 0, 0), -1)
        # cv2.circle(imgOriginal, (int(rectHalfVerticesLeftX), int(rectHalfVerticesLeftY)),
        #            5, (255, 0, 0), -1)
        # # draw rectangle
        # imgOriginal = draw_angled_rec(
        #     rect[0][0], rect[0][1], rect[1][1], rect[1][0], rect[2], imgOriginal)

        posOrigin = [rectHalfVerticesLeftX, rectHalfVerticesLeftY]
        posDestination = [rectHalfVerticesRightX, rectHalfVerticesRightY]
        pos_1 = (int(rectHalfVerticesLeftX), int(rectHalfVerticesLeftY))
        pos_2 = (int(rectHalfVerticesRightX), int(rectHalfVerticesRightY))
        imgPseudoSkel = cv2.line(
            imgPseudoSkel, pos_1, pos_2, (255), 1)
        return posOrigin, posDestination, imgPseudoSkel


def shadowEdgeOnObj(imgObjColor, imgHSV, hue, saturation, value):
    # Define thresholds for channel 1 based on histogram settings
    channel1Min = int(float(hue["min"]) * 360)
    channel1Max = int(float(hue["max"]) * 360)

    # Define thresholds for channel 2 based on histogram settings
    channel2Min = int(float(saturation["min"]) * 255)
    channel2Max = int(float(saturation["max"]) * 255)

    # Define thresholds for channel 3 based on histogram settings
    channel3Min = int(float(value["min"]) * 255)
    channel3Max = int(float(value["max"]) * 255)

    imgShadowOnObj = np.zeros_like(imgObjColor)
    # hsv = cv2.cvtColor(imgObjColor, cv2.COLOR_BGR2HSV_FULL)
    imgShadowOnObj = cv2.inRange(
        imgHSV, (channel1Min, channel2Min, channel3Min), (channel1Max, channel2Max, channel3Max))
    contours, hierarchy = cv2.findContours(
        imgShadowOnObj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest area of the contour
        big_contour = max(contours, key=cv2.contourArea)
    cv2.drawContours(imgShadowOnObj, big_contour, 0, 255, -1)
    # imgShadowOnObj = cv2.erode(imgShadowOnObj, np.ones((3, 3), np.uint8), iterations=1)
    # imgShadowOnObj = cv2.dilate(imgShadowOnObj, np.ones((3, 3), np.uint8), iterations=1)
    imgShadowOnObj = cv2.morphologyEx(imgShadowOnObj, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)
    return imgShadowOnObj