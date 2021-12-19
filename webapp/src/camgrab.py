import cv2
import queue
from threading import Thread
import datetime
import time
import os
import sys
import numpy as np
from skimage.morphology import skeletonize
from . import mathTools
from . import segmentation

############### for setting parameters referene #####################################
# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returnedchrome by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently


class camgrab:

    def __init__(self, config):
        self.cap = cv2.VideoCapture(0)
        self.setConfigDefault(config)
        self.imgBg = cv2.imread("./ref/background.jpg")
        self.feedStatus = "rawImage"
        self.imgDiffBinTreshold = 240
        self.imgAndBinTreshold = 50
        self.medianBlur = 12

        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

        # self.gen_frames()
        # self.threadRawFeed = threading.Thread(target=self.thread_raw_feed)
        # self.threadProcessFeed = threading.Thread(target=self.thread_process_feed)

        self.queueRawFeed = queue.Queue()
        self.queueSubBackgroundFeed = queue.Queue()
        self.queueImgAndFeed = queue.Queue()
        self.queueMorphFeed = queue.Queue()
        self.segmentSourceFeed = queue.Queue()

        self.threadGenFrames = Thread(target=self.gen_frames, args=(
            self.queueRawFeed, self.queueSubBackgroundFeed, self.queueImgAndFeed, self.queueMorphFeed, self.segmentSourceFeed), daemon=True)
        # self.threadRawFeed = Thread(target=self.thread_raw_feed)

    def setConfigDefault(self, config):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['height'])
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 1)  # manual mode
        self.cap.set(cv2.CAP_PROP_EXPOSURE, config['exposure'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST, config['contrast'])
        self.cap.set(cv2.CAP_PROP_HUE, config['hue'])
        self.cap.set(cv2.CAP_PROP_SATURATION, config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS, config['sharpness'])

    def setConfig(self, config):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.cap.set(cv2.CAP_PROP_EXPOSURE, config['exposure'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST, config['contrast'])
        self.cap.set(cv2.CAP_PROP_HUE, config['hue'])
        self.cap.set(cv2.CAP_PROP_SATURATION, config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS, config['sharpness'])

    def getConfig(self):
        loadConfig = {}
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        loadConfig['exposure'] = self.cap.get(cv2.CAP_PROP_EXPOSURE) - 1
        loadConfig['brightness'] = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        loadConfig['contrast'] = self.cap.get(cv2.CAP_PROP_CONTRAST)
        loadConfig['hue'] = self.cap.get(cv2.CAP_PROP_HUE)
        loadConfig['saturation'] = self.cap.get(cv2.CAP_PROP_SATURATION) + 64
        loadConfig['sharpness'] = self.cap.get(cv2.CAP_PROP_SHARPNESS)
        return loadConfig

    # def gen_frames(self):
    #     while True:
    #         if self.cap != 0:
    #             success, self.frame = self.cap.read()
    #             self.success = success
    #             if success:
    #                 self.success = False
    #                 # frame=cv2.flip(frame,1)
    #                 # if camOpen == False:
    #                 #     break
    #                 self.diffImage = cv2.cvtColor(
    #                     self.frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY)
    #                 # self.diffImage = cv2.absdiff(cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY), cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY))
    #                 ret, self.imgDiffBin = cv2.threshold(
    #                     self.diffImage, self.imgDiffBinTreshold, 255, cv2.THRESH_BINARY_INV)
    #                 self.imgAnd = cv2.bitwise_and(
    #                     self.imgDiffBin, self.diffImage)
    #                 ret, self.imgBin = cv2.threshold(
    #                     self.imgAnd, self.imgAndBinTreshold, 255, cv2.THRESH_BINARY)
    #                 self.imgOpening = cv2.morphologyEx(
    #                     self.imgBin, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    #                 self.imgOpening = cv2.medianBlur(
    #                     self.imgOpening, self.medianBlur)
    #                 self.imgSegmentBin, posCrop = segmentation.objShadow(
    #                     self.frame, self.imgOpening)

    #                 for crop in posCrop:
    #                     if not crop[0] < 1 or crop[1] < 1:
    #                         cv2.rectangle(self.imgSegmentBin, (crop[0], crop[1]), (
    #                             crop[0]+crop[2], crop[1]+crop[3]), (255, 255, 255), 2)
    #                 # cv2.rectangle(self.imgSegmentBin, (crop[1], crop[2]), (crop[1]+crop[3], crop[2]+crop[4]), (0, 255, 0), 2)
    #                 # print(crop)
    #                 try:
    #                     if self.feedStatus == "rawImage":
    #                         ret, buffer = cv2.imencode('.jpg', self.frame)
    #                     elif self.feedStatus == "subtractBackground":
    #                         ret, buffer = cv2.imencode('.jpg', self.diffImage)
    #                     elif self.feedStatus == "binaryImage":
    #                         ret, buffer = cv2.imencode('.jpg', self.imgDiffBin)
    #                     elif self.feedStatus == "andImage":
    #                         ret, buffer = cv2.imencode('.jpg', self.imgAnd)
    #                     elif self.feedStatus == "morphologyImage":
    #                         ret, buffer = cv2.imencode('.jpg', self.imgOpening)
    #                     elif self.feedStatus == "segmentImage":
    #                         ret, buffer = cv2.imencode(
    #                             '.jpg', self.imgSegmentBin)
    #                     else:
    #                         ret, buffer = cv2.imencode('.jpg', self.frame)
    #                     frameByte = buffer.tobytes()
    #                     yield (b'--frame\r\n'
    #                            b'Content-Type: image/jpeg\r\n\r\n' + frameByte + b'\r\n')
    #                     # return frameByte
    #                 except Exception as e:
    #                     pass
    #             else:
    #                 pass
    #         else:
    #             pass

    def gen_frames(self, queueRawFeed, queueSubBackground, queueImgAndFeed, queueMorphFeed, segmentSourceFeed):
        while True:
            if self.cap != 0:
                success, frame = self.cap.read()
                self.success = success
                if success:
                    # print("Fire")
                    self.success = False
                    queueRawFeed.put(frame)
                    diffImage = cv2.cvtColor(
                        frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY)
                    ret, imgDiffBin = cv2.threshold(
                        diffImage, self.imgDiffBinTreshold, 255, cv2.THRESH_BINARY_INV)
                    queueSubBackground.put(diffImage)
                    imgAnd = cv2.bitwise_and(
                        imgDiffBin, diffImage)
                    ret, imgBin = cv2.threshold(
                        imgAnd, self.imgAndBinTreshold, 255, cv2.THRESH_BINARY)
                    queueImgAndFeed.put(imgBin)
                    imgOpening = cv2.morphologyEx(
                        imgBin, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                    imgOpening = cv2.medianBlur(
                        imgOpening, self.medianBlur)
                    queueMorphFeed.put(imgOpening)
                    imgSegmentSource, imgSegmentBlack, imgROI, posCrop = segmentation.objShadow(
                        frame, imgOpening)
                    segmentSourceFeed.put(imgSegmentSource)
                else:
                    pass
            else:
                pass
   
    def raw_feed(self):
        # self.threadGenFrames.start()
        while True:
            # self.threadGenFrames.join()
            frame = self.queueRawFeed.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def subtract_background_feed(self):
        # self.threadGenFrames.start()
        while True:
            # self.threadGenFrames.join()
            frame = self.queueSubBackgroundFeed.get()
            # self.diffImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def imgAnd_feed(self):
        # self.threadGenFrames.start()
        while True:
            # self.threadGenFrames.join()
            frame = self.queueImgAndFeed.get()
            # self.diffImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def morph_feed(self):
        # self.threadGenFrames.start()
        while True:
            # self.threadGenFrames.join()
            frame = self.queueMorphFeed.get()
            # self.diffImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def segmented_feed(self):
        # self.threadGenFrames.start()
        while True:
            # self.threadGenFrames.join()
            frame = self.segmentSourceFeed.get()
            # self.diffImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(self.imgBg, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def shotSetting(self):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        now = datetime.datetime.now()
        p = os.path.sep.join(
            ['shots', "shot_{}.jpg".format(str(now).replace(":", ''))])
        cv2.imwrite(p, self.frame)

    def captureAll(self):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        now = datetime.datetime.now()
        p = os.path.sep.join(
            ['./capture/', "{}".format(str(now).replace(":", ''))])
        try:
            os.mkdir(p)
        except OSError as error:
            pass
        # p = os.path.join(['./capture/', "{}".format(str(now).replace(":",''))])
        print(p)
        cv2.imwrite(os.path.join(p, "imgraw.jpg"), self.frame)
        cv2.imwrite(os.path.join(p, "imgdiff.jpg"), self.diffImage)
        cv2.imwrite(os.path.join(p, "imgAnd.jpg"), self.imgAnd)
        cv2.imwrite(os.path.join(p, "imgBin.jpg"), self.imgBin)
        cv2.imwrite(os.path.join(p, "imgopening.jpg"), self.imgOpening)
        cv2.imwrite(os.path.join(p, "imgsegment.jpg"), self.imgSegmentBin)

    def camRelease(self):
        self.cap.release()

        pass
