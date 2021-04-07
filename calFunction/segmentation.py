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


def obj(imgSample, imgMask):
    # contours, hierarchy = cv2.findContours(
    #     imgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # if len(contours) != 0:
    #     # find the biggest area of the contour
    #     big_contour = max(contours, key=cv2.contourArea)
    #     # draw filled contour on black background
    #     mask = np.zeros_like(imgSample)
    #     # mask[:, :] = (255, 0, 0)
    #     cv2.drawContours(mask, [big_contour], 0, (255, 255, 255), -1)
    # if debug == True:
    #     cv2.imshow("Mask", mask)
    height, width, channel = imgSample.shape
    imgMaskRgb = np.zeros_like(imgSample)
    imgMaskRgb[:, :, 0] = imgMask
    imgMaskRgb[:, :, 1] = imgMask
    imgMaskRgb[:, :, 2] = imgMask
    # apply mask to input image
    # Create a green screen image (background color is used to seperated the object).
    # ie. apple used green screen, mango used red screen.
    greenScreenImage = cv2.bitwise_and(imgSample, imgMaskRgb)
    if debug == True:
        cv2.imshow("Green Screen Masking Result", greenScreenImage)

    # draw boundary box of objet
    # x, y, w, h = cv2.boundingRect(big_contour)
    # # draw the 'human' contour (in green)
    # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)
    imgObj = maskObj(greenScreenImage)
    contours, hierarchy = cv2.findContours(
        imgObj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest area of the contour
        big_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(imgObj, [big_contour], 0, 255, -1)

        # # find centroid by image moment
        # M = cv2.moments(big_contour)
        # cx = int(M['m10']/M['m00'])
        # cy = int(M['m01']/M['m00'])
        # # cv2.circle(imgObj, (cx, cy), 5, (0), -1)

        # ellipse = cv2.fitEllipse(big_contour)
        # # imgObj = cv2.ellipse(imgObj, ellipse, 255, 1)
        # # imgObj = cv2.blur(imgObj, (10, 10))
        imgObj = cv2.medianBlur(imgObj, 9)
        if debug == True:
            cv2.imshow("Median Filtering", imgObj)
    return imgObj


def shadow(imgMask, imgObj):
    imgOut = np.zeros_like(imgObj)
    # morphology a little bit to imgObj
    # ret, imgMask = cv2.threshold(imgMask, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("Input Shadow Image", imgMask)
    imgShadow = cv2.bitwise_xor(imgMask, imgObj)
    # imgShadow = cv2.morphologyEx(imgShadow, cv2.MORPH_OPEN,
    #                              np.ones((15, 15), np.uint8))
    cv2.imshow("EX OR", imgShadow)

    # imgShadow = cv2.erode(imgShadow, np.ones((16, 16), np.uint8), iterations=1)
    contours, hierarchy = cv2.findContours(
        imgShadow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest area of the contour
        big_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(imgOut, [big_contour], 0, 255, -1)
        # imgShadow = cv2.morphologyEx(imgShadow, cv2.MORPH_OPEN,
        #                              np.ones((15, 15), np.uint8))
    return imgOut


def maskObj(img):
    # Define thresholds for channel 1 based on histogram settings
    channel1Min = 0.189 * 255
    channel1Max = 0.522 * 255

    # Define thresholds for channel 2 based on histogram settings
    channel2Min = 0.209 * 255
    channel2Max = 1.000 * 255

    # Define thresholds for channel 3 based on histogram settings
    channel3Min = 0.157 * 255
    channel3Max = 1.000 * 255

    imgMasked = np.zeros_like(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgMasked = cv2.inRange(
        hsv, (channel1Min, channel2Min, channel3Min), (channel1Max, channel2Max, channel3Max))
    return imgMasked


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
