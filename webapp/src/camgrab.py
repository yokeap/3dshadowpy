import cv2
import datetime
import time
import os
import sys

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
        self.imgBg = cv2.imread("../ref/background.png")

        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

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
        loadConfig['exposure'] = self.cap.get(cv2.CAP_PROP_EXPOSURE)
        loadConfig['brightness'] = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        loadConfig['contrast'] = self.cap.get(cv2.CAP_PROP_CONTRAST)
        loadConfig['hue'] = self.cap.get(cv2.CAP_PROP_HUE)
        loadConfig['saturation'] = self.cap.get(cv2.CAP_PROP_SATURATION)
        loadConfig['sharpness'] = self.cap.get(cv2.CAP_PROP_SHARPNESS)
        return loadConfig

    def gen_frames(self, frameType):
        while True:
            if self.cap != 0:
                success, frame = self.cap.read()
                if success:
                    # frame=cv2.flip(frame,1)
                    # if camOpen == False:
                    #     break
                    diffImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    if frameType == "gray":
                        try:
                            ret, buffer = cv2.imencode('.png', diffImage)
                            frameByte = buffer.tobytes()
                            yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frameByte + b'\r\n')
                            return frameByte
                        except Exception as e:
                            pass
                    else:
                        try:
                            ret, buffer = cv2.imencode('.jpg', frame)
                            frameByte = buffer.tobytes()
                            yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frameByte + b'\r\n')
                            return frameByte
                        except Exception as e:
                            pass
                else:
                    pass
            else:
                pass

    def encodeResponse(self, frame):
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frameByte = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frameByte + b'\r\n')
        except Exception as e:
            pass

    def shotSetting(self):
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        now = datetime.datetime.now()
        p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
        cv2.imwrite(p, self.frame)
    
    def camRelease(self):
        self.cap.release()

        pass