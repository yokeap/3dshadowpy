import cv2
import queue
from threading import Thread
import datetime
import time
import os
import sys
import json
import numpy as np
import pandas as pd
from skimage.morphology import skeletonize
from . import mathTools
from . import segmentation
from . import reconstruct

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

    def __init__(self, config, socket):
        # self.objReconstruct = reconstruct.reconstruct(1.0, config)
        # for test with fish
        self.objReconstruct = reconstruct.reconstruct(1, config)
        self.cap = cv2.VideoCapture(0)
        self.setConfig(config)
        # self.imgBg = cv2.fastNlMeansDenoisingColored(cv2.imread("./ref/background.jpg"), h =2)
        self.imgBg = cv2.cvtColor(cv2.imread("./ref/background.jpg"), cv2.COLOR_BGR2GRAY)
        self.feedStatus = "rawImage"
        self.imgDiffBinTreshold = config["imgDiffBinTreshold"]
        self.imgAndBinTreshold = config['imgAndBinTreshold']
        self.medianBlur = config['medianBlur']
        self.objHue = config["obj"]["hue"]
        self.objSaturation = config["obj"]["saturation"]
        self.objValue = config["obj"]["value"]
        self.shadowHue = config["shadowOnObj"]["hue"]
        self.shadowSaturation = config["shadowOnObj"]["saturation"]
        self.shadowValue = config["shadowOnObj"]["value"]
        self.socket = socket
        self.socketConnectStatus = False
        self.configFeedStatus = False
        self.objJson = {}

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
        self.queueROIFeed = queue.Queue()
        self.queueShadow = queue.Queue()
        self.queueShadowOnObjFeed = queue.Queue()

        self.threadGenFrames = Thread(target=self.gen_frames, args=(
            self.queueRawFeed, self.queueSubBackgroundFeed, self.queueImgAndFeed, 
            self.queueMorphFeed, self.segmentSourceFeed, self.queueROIFeed, self.queueShadow,
            self.queueShadowOnObjFeed), daemon=True)
        # self.threadRawFeed = Thread(target=self.thread_raw_feed)

    def setConfigDefault(self, config):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['height'])
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)  # manual mode
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
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['height'])
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)  # manual mode
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 1)  # manual mode
        self.cap.set(cv2.CAP_PROP_EXPOSURE, config['exposure'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST, config['contrast'])
        self.cap.set(cv2.CAP_PROP_HUE, config['hue'])
        self.cap.set(cv2.CAP_PROP_SATURATION, config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS, config['sharpness'])

    def setInitParams(self, config):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        

    def getConfig(self):
        loadConfig = {}
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        loadConfig['exposure'] = self.cap.get(cv2.CAP_PROP_EXPOSURE) 
        loadConfig['brightness'] = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        loadConfig['contrast'] = self.cap.get(cv2.CAP_PROP_CONTRAST)
        loadConfig['hue'] = self.cap.get(cv2.CAP_PROP_HUE)
        loadConfig['saturation'] = self.cap.get(cv2.CAP_PROP_SATURATION)
        loadConfig['sharpness'] = self.cap.get(cv2.CAP_PROP_SHARPNESS)
        return loadConfig

    def gen_frames(self, queueRawFeed, queueSubBackground, queueImgAndFeed, queueMorphFeed, segmentSourceFeed, queueROIFeed, queueShadow, queueShadowOnObjFeed):
        end = 0
        while True:
            if self.cap != 0:
                start = time.time()
                success, self.frame = self.cap.read()
                # self.frame = cv2.GaussianBlur(self.frame,(5,5),0)
                # self.frame = cv2.fastNlMeansDenoisingColored(self.frame, h=2)
                try:
                    self.success = success
                    if success == True and self.configFeedStatus == True:
                        self.success = False
                        queueRawFeed.put(self.frame)
                    if success == True and self.socketConnectStatus == True and self.feedStatus != "freeze":
                        # for test with fish
                        # self.imgBg = cv2.imread('../sample-image/bg-1.JPG')
                        # self.frame = cv2.imread('../sample-image/fish-1.JPG')
                        # height, width, channels = self.frame.shape
                        # height = int(height * 0.2)
                        # width = int(width * 0.2)
                        # self.imgBg = cv2.resize(self.imgBg, (width, height))
                        # self.frame = cv2.resize(self.frame, (width, height))

                        # print("Fire")
                        # start timer
                        # start = time.time()
                        self.success = False
                        self.rawframe = self.frame.copy()
                        queueRawFeed.put(self.frame)
                        self.diffImage = cv2.absdiff(cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY), self.imgBg)
                        ret, self.imgDiffBin = cv2.threshold(
                            self.diffImage, self.imgDiffBinTreshold, 255, cv2.THRESH_BINARY)
                        self.imgDiffMorphBin = cv2.morphologyEx(
                            self.imgDiffBin, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
                        # ret, self.imgDiffBin = cv2.threshold(
                        #     self.diffImage, self.imgDiffBinTreshold, 255, cv2.THRESH_BINARY_INV)
                        # queueSubBackground.put(self.diffImage)
                        # self.imgAnd = cv2.bitwise_and(
                        #     self.imgDiffBin, self.diffImage)
                        # ret, self.imgBin = cv2.threshold(
                        #     self.imgAnd, self.imgAndBinTreshold, 255, cv2.THRESH_BINARY)
                        # queueImgAndFeed.put(self.imgBin)
                        # self.imgOpening = cv2.morphologyEx(
                        #     self.imgBin, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                        # try:
                        #     self.imgOpening = cv2.medianBlur(
                        #         self.imgOpening, self.medianBlur)
                        # except Exception as e:
                        #     pass
                        queueMorphFeed.put(self.imgDiffMorphBin)
                        # self.imgSegmentSource, self.imgSegmentBlack, self.imgROI, self.posCrop = segmentation.objShadow(
                        #     self.frame, self.imgDiffMorphBin)
                        self.imgROI, self.posCrop = segmentation.singleObjShadow(self.frame, self.imgDiffMorphBin )
                        segmentSourceFeed.put(self.frame)
                        try:
                            self.imgObj, self.imgSkeleton = self.process_imgObj(self.imgROI[0])
                            queueROIFeed.put(self.imgObj)
                            queueShadowOnObjFeed.put(self.imgSkeleton)
                            self.imgShadow = segmentation.shadow(self.imgROI[0], self.imgObj)
                            queueShadow.put(self.imgShadow)
                            # self.imgShadowOnObj = self.process_imgShadowOnObj(self.imgObjColor)
                            # queueShadowOnObjFeed.put(self.imgShadowOnObj)
                            self.objReconstruct.reconstruct(self.frame, self.imgObj, self.imgSkeleton, self.imgShadow, self.posCrop )
                            ptCloud, volume, length = self.objReconstruct.reconstructVolume(0.05)
                            end = time.time()
                            print("processed time = ", (end - start), "s")
                            if self.socketConnectStatus == True:
                                self.objJson = {
                                    "ptCloud" : {
                                        "x": ptCloud[:, 0].tolist(),
                                        "y": ptCloud[:, 1].tolist(),
                                        "z": ptCloud[:, 2].tolist(),
                                    },
                                    "volume": volume,
                                    "length": length,
                                    "computeTime": (end - start)
                                }
                                self.socket.emit('reconstruction-data', json.dumps(self.objJson))
                                # self.objReconstruct.volumeChart(end - start)
                        except Exception as e:
                            print(e)
                            queueROIFeed.put(np.zeros_like(self.frame))
                            queueShadow.put(np.zeros_like(self.frame))
                            queueShadowOnObjFeed.put(np.zeros_like(self.frame))
                            pass
                    else:
                        pass
                except Exception as e:
                    print(e)
                    pass
            else:
                pass

    def process_imgObjColor(self, imgROI):
        objJson = {}
        imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
        h, s, v = imageHSV[:,:,0], imageHSV[:,:,1], imageHSV[:,:,2]
        h = np.transpose(cv2.calcHist([h],[0],None,[360],[0,360]))
        s = np.transpose(cv2.calcHist([s],[0],None,[256],[0,256]))
        v = np.transpose(cv2.calcHist([v],[0],None,[256],[0,256]))
        objJson['hist_h'] = h.tolist()
        objJson['hist_h_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        objJson['hist_s'] = s.tolist()
        objJson['hist_s_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        objJson['hist_v'] = v.tolist()
        objJson['hist_v_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        if self.socketConnectStatus == True:
            self.socket.emit('hsv-obj-data', json.dumps(objJson))
        imgObj, imgObjColor = segmentation.obj(imgROI, imageHSV, self.objHue, self.objSaturation, self.objValue)
        return imgObj, imgObjColor

    def process_imgObj(self, imgROI):
        objJson = {}
        imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
        h, s, v = imageHSV[:,:,0], imageHSV[:,:,1], imageHSV[:,:,2]
        h = np.transpose(cv2.calcHist([h],[0],None,[360],[0,360]))
        s = np.transpose(cv2.calcHist([s],[0],None,[256],[0,256]))
        v = np.transpose(cv2.calcHist([v],[0],None,[256],[0,256]))
        objJson['hist_h'] = h.tolist()
        objJson['hist_h_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        objJson['hist_s'] = s.tolist()
        objJson['hist_s_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        objJson['hist_v'] = v.tolist()
        objJson['hist_v_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        if self.socketConnectStatus == True:
            self.socket.emit('hsv-obj-data', json.dumps(objJson))
        imgObj, imgSkeleton = segmentation.obj(imgROI, imageHSV, self.objHue, self.objSaturation, self.objValue)
        return imgObj, imgSkeleton

    def process_imgShadowOnObj(self, imgROI):
        shadowJson = {}
        imageHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV_FULL)
        h, s, v = imageHSV[:,:,0], imageHSV[:,:,1], imageHSV[:,:,2]
        # df=pd.DataFrame(h, columns=["x", "y"])
        h = np.transpose(cv2.calcHist([h],[0],None,[360],[0,360]))
        s = np.transpose(cv2.calcHist([s],[0],None,[256],[0,256]))
        v = np.transpose(cv2.calcHist([v],[0],None,[256],[0,256]))
        shadowJson['hist_h'] = h.tolist()
        shadowJson['hist_h_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        shadowJson['hist_s'] = s.tolist()
        shadowJson['hist_s_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        shadowJson['hist_v'] = v.tolist()
        shadowJson['hist_v_ymax'] = (np.mean(h) + 0.5 * np.std(h)).tolist()
        if self.socketConnectStatus == True:
            self.socket.emit('hsv-shadow-data', json.dumps(shadowJson))
        imgShadowOnObj = segmentation.shadowEdgeOnObj(imgROI, imageHSV, self.shadowHue, self.shadowSaturation, self.shadowValue)
        return imgShadowOnObj 
   
    def raw_feed(self):
        # self.threadGenFrames.start()
        while True:
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

    def roi_feed(self):
        while True:
            frame = self.queueROIFeed.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def shadow_feed(self):
        while True:
            frame = self.queueShadow.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def shadow_on_obj_feed(self):
        while True:
            frame = self.queueShadowOnObjFeed.get()
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
        cv2.imwrite(os.path.join(p, "imgraw.jpg"), self.rawframe)
        cv2.imwrite(os.path.join(p, "imgdiff.jpg"), self.diffImage)
        cv2.imwrite(os.path.join(p, "imgAnd.jpg"), self.imgAnd)
        cv2.imwrite(os.path.join(p, "imgBin.jpg"), self.imgBin)
        cv2.imwrite(os.path.join(p, "imgopening.jpg"), self.imgOpening)
        cv2.imwrite(os.path.join(p, "imgsegment.jpg"), self.imgSegmentBlack)
        try:
            cv2.imwrite(os.path.join(p, "imgroi.jpg"), self.imgROI[0])
            cv2.imwrite(os.path.join(p, "imgObjColor.jpg"), self.imgObjColor)
            cv2.imwrite(os.path.join(p, "imgShadow.jpg"), self.imgShadow)
            cv2.imwrite(os.path.join(p, "imgShadowOnObj.jpg"), self.imgShadowOnObj)
            with open(os.path.join(p, "reconstruct.json"), 'w') as f:
                json.dump(self.objJson, f)
        except:

            pass

    def camRelease(self):
        self.cap.release()

        pass
