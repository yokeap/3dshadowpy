import cv2
import numpy as np
import numpy.matlib

# Define thresholds for channel 1 based on histogram settings
channel1Min = 0.189 * 255
channel1Max = 0.522 * 255

# Define thresholds for channel 2 based on histogram settings
channel2Min = 0.209 * 255
channel2Max = 1.000 * 255

# Define thresholds for channel 3 based on histogram settings
channel3Min = 0.157 * 255
channel3Max = 1.000 * 255

# Create mask based on chosen histogram thresholds

# #color boundaries [H, S, V]
# lower = (channel1Min, chan, 210)
# upper = (channel1Max, 130, 255)


def segmentObj(img):
    height, width, channels = img.shape
    sliderBW = np.zeros_like(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # sliderBW = mask3ch2bin(hsv, channel1Min, channel2Min,
    #                        channel3Min, channel1Max, channel2Max, channel3Max)

    # sliderBW[:, :, 0] = (hsv[:, :, 0] >= channel1Min) & (
    #     hsv[:, :, 0] <= channel1Max)
    # sliderBW[:, :, 1] = (hsv[:, :, 1] >= channel2Min) & (
    #     hsv[:, :, 1] <= channel2Max)
    # sliderBW[:, :, 2] = (hsv[:, :, 2] >= channel3Min) & (
    #     hsv[:, :, 2] <= channel3Max)
    # maskedRGBImage = img
    # ch1 = numpy.matlib.repmat(sliderBW, 1, 1).astype(int)
    # maskedRGBImage[:, :, 0] = ch1 * img[:, :, 2]
    # maskedRGBImage[:, :, 1] = ch1 * img[:, :, 1]
    # maskedRGBImage[:, :, 2] = ch1 * img[:, :, 0]
    maskedRGBImage = cv2.inRange(
        hsv, (channel1Min, channel2Min, channel3Min), (channel1Max, channel2Max, channel3Max))
    # bw = np.array(sliderBW)
    return maskedRGBImage


# def binImage3ch(img):
#     height, width, channels = img.shape
#     maskedRGBImage = np.zeros([height, width, 1], dtype=np.uint8)
#     sliderBW = mask3ch2bin(img, 1, 1, 1, 255, 255, 255)
#     ch1 = numpy.matlib.repmat(sliderBW, 1, 1).astype(int)
#     maskedRGBImage[:, :, 0] = ch1 * 255
#     # bw = np.array(sliderBW)
#     return maskedRGBImage


def mask3ch2bin(img, ch1Min, ch2Min, ch3Min, ch1Max, ch2Max, ch3Max):
    sliderBW = (img[:, :, 0] >= ch1Min) & (img[:, :, 0] <= ch1Max) \
        & (img[:, :, 1] >= ch2Min) & (img[:, :, 1] <= ch2Max) \
        & (img[:, :, 2] >= ch3Min) & (img[:, :, 2] <= ch3Max)
    return sliderBW
