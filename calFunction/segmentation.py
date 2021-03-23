import cv2
import numpy as np

debug = False


def obj(imgSample, imgBin):
    contours, hierarchy = cv2.findContours(
        imgBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest area of the contour
        big_contour = max(contours, key=cv2.contourArea)
        # draw filled contour on black background
        mask = np.zeros_like(imgSample)
        # mask[:, :] = (255, 0, 0)
        cv2.drawContours(mask, [big_contour], 0, (255, 255, 255), -1)
        if debug == True:
            cv2.imshow("Mask", mask)

        # apply mask to input image
        # Create a green screen image (background color is used to seperated the object).
        # ie. apple used green screen, mango used red screen.
        greenScreenImage = cv2.bitwise_and(imgSample, mask)
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
            # imgObj = cv2.blur(imgObj, (10, 10))
        return imgObj


def shadow(imgBin, imgObj):
    # fill holes by contour filling
    imgShadow = cv2.bitwise_xor(imgBin, imgObj)
    imgShadow = cv2.erode(imgShadow, np.ones((16, 16), np.uint8), iterations=1)
    return imgShadow


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
