from logging import debug
from flask import Flask, render_template, Response, request, send_from_directory, jsonify
from flask_socketio import SocketIO
from time import sleep
from math import sqrt
import plotly
import plotly.graph_objs as go
from src import camgrab
from jsonmerge import merge
import cv2
import sys
import json
import time
import pandas as pd
import numpy as np
from engineio.payload import Payload

Payload.max_decode_packets = 50

app = Flask(__name__, template_folder='./view', static_folder='./view')
socketio = SocketIO(app,ping_timeout=5,ping_interval=5)

global config

# load config
with open('./config.json', 'r') as f:
    config = json.load(f)

camera = camgrab.camgrab(config, socketio)
camera.threadGenFrames.do_run = False
if camera.threadGenFrames.is_alive():
    camera.threadGenFrames.stop()

def send_data():
    result = {}
    jsonData = request.get_json()
    result['message'] = "success"
    socketio.emit('data', json.dumps(result))

@app.route('/')
def index():
    # bar = create_plot()
    return render_template('index.html')

@app.route('/config', methods=['POST', 'GET'])
def configHandler():
    camera.socketConnectStatus = False
    result = {}
    if request.method == 'POST':
        jsonData = request.get_json()
        # write it back to the file
        print(jsonData)
        if jsonData["browserEvent"] == "capture":
            camera.shotSetting()
            result['message'] = "success"
            return jsonify(result['message'])
        elif jsonData["browserEvent"] == "config-load":
            camera.setConfigDefault(config["default"])
            return jsonify(config["default"])
        elif jsonData["browserEvent"] == "loaded":
            # camera.gen_frames()
            result = camera.getConfig()
            return jsonify(result)
        # elif jsonData["browserEvent"] == "close":
            
        else :
            print(jsonData)
            camera.cap.set(cv2.CAP_PROP_EXPOSURE, jsonData['exposure'])
            camera.cap.set(cv2.CAP_PROP_BRIGHTNESS, jsonData['brightness'])
            camera.cap.set(cv2.CAP_PROP_CONTRAST, jsonData['contrast'])
            camera.cap.set(cv2.CAP_PROP_HUE, jsonData['hue'])
            camera.cap.set(cv2.CAP_PROP_SATURATION, jsonData['saturation'])
            camera.cap.set(cv2.CAP_PROP_SHARPNESS, jsonData['sharpness'])
            result['message'] = "success"
            return jsonify(result['message'])
        # camera.setConfig(jsonData)
        

    elif request.method == 'GET':
        return render_template('camconfig.html')
    return render_template('camconfig.html')


@app.route('/config-save', methods=['POST', 'GET'])
def saveHandler():
    result = {}
    if request.method == 'POST':
        jsonData = request.get_json()
        # write it back to the file
        with open('./config.json', 'w') as f:
            json.dump(merge(config, jsonData), f)
        result['message'] = "success"
        return jsonify(result['message'])

    elif request.method == 'GET':
        return render_template('camconfig.html')
    return render_template('camconfig.html')


# @app.route('/requests')
# def recvHandler():
#     return render_template('index.html')   

@app.route('/config_feed')
def config_feed():
    camera.configFeedStatus = True
    # return Response(camera.thread_raw_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    if not camera.threadGenFrames.is_alive():
        camera.threadGenFrames.start()
    return Response(camera.raw_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/raw_feed')
def raw_feed():
    camera.configFeedStatus = False
    # return Response(camera.thread_raw_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    if not camera.threadGenFrames.is_alive():
        camera.threadGenFrames.start()
    return Response(camera.raw_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/subtract_background')
def subtract_background():
    return Response(camera.subtract_background_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/imgand')
def imgand():
    return Response(camera.imgAnd_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/imgmorph')
def imgmorph():
    return Response(camera.morph_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/imgsegentedcrop')
def imgsegentedcrop():
    return Response(camera.segmented_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/imgroi')
def imgroi():
    return Response(camera.roi_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/imgshadow')
def imgshadow():
    return Response(camera.shadow_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/imgshadowonobj')
def imgshadowonobj():
    return Response(camera.shadow_on_obj_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def connect_event():
    # send out config loaded to html
    camera.socketConnectStatus = True
    camera.imgDiffBinTreshold = config['imgDiffBinTreshold']
    camera.imgAndBinTreshold =  config['imgAndBinTreshold']
    camera.medianBlur = config['medianBlur']
    print('socket has been connected')

@socketio.on('message')
def message_handle(message):
    if message == "loaded":
        print('html dom has been successfully loaded')
        camera.socketConnectStatus = True
        jsonData = {}
        jsonData['subtractTreshVal'] = config['imgDiffBinTreshold']
        jsonData['imgAndBinTreshVal'] =  config['imgAndBinTreshold']
        jsonData['medianBlur'] =  config['medianBlur']
        jsonData['objShadowTreshVal'] =  config['objShadowTresholdVal']
        socketio.emit('data-params', json.dumps(jsonData))
        jsonData = {}
        jsonData['slider_h_obj'] = config['obj']['hue']
        jsonData['slider_s_obj'] = config['obj']['saturation']
        jsonData['slider_v_obj'] = config['obj']['value']
        jsonData['slider_h_shadow'] = config['shadowOnObj']['hue']
        jsonData['slider_s_shadow'] = config['shadowOnObj']['saturation']
        jsonData['slider_v_shadow'] = config['shadowOnObj']['value']
        socketio.emit('data-obj-hsv', json.dumps(jsonData))
        
@socketio.on('disconnect')
def disconnect_event():
    # camera.threadGenFrames.stop()
    camera.socketConnectStatus = False
    print('socket has been disconnected')

@socketio.on('feed-status')
def fedd_status_handle(jsonData):
    pyObj = json.loads(jsonData)
    camera.feedStatus = pyObj["feedStatus"]
    print("main streaming has been changed to ", pyObj["feedStatus"])

@socketio.on('process-value')
def process_value_handle(jsonData):
    pyObj = json.loads(jsonData)
    camera.imgDiffBinTreshold = int(pyObj['subtractTreshVal'])
    camera.imgAndBinTreshold = int(pyObj['imgAndTreshVal'])
    camera.medianBlur = int(pyObj['medBlurVal'])
    config['imgDiffBinTreshold']
    config['imgDiffBinTreshold']
    config['medianBlur']
    config['objShadowTresholdVal']
    
@socketio.on('slider-obj-hsv')
def slider_obj_hsv_event(jsonData):
    pyObj = json.loads(jsonData)
    camera.objHue = pyObj["hue"]
    camera.objSaturation = pyObj["saturation"]
    camera.objValue = pyObj["value"]

@socketio.on('slider-shadow-hsv')
def slider_obj_hsv_event(jsonData):
    pyObj = json.loads(jsonData)
    camera.shadowHue = pyObj["hue"]
    camera.shadowSaturation = pyObj["saturation"]
    camera.shadowValue = pyObj["value"]

@socketio.on('save-config')
def save_config_handle(jsonData):
    pyObj = json.loads(jsonData)
    if pyObj['saveParams'] == True:
        config['imgDiffBinTreshold'] = camera.imgDiffBinTreshold
        config['imgAndBinTreshold'] = camera.imgAndBinTreshold 
        config['medianBlur'] = camera.medianBlur
        # config['objShadowTresholdVal']
        config['obj']['hue'] = camera.objHue
        config['obj']['saturation'] = camera.objSaturation
        config['obj']['value'] = camera.objValue
        config['shadowOnObj']['hue'] = camera.shadowHue
        config['shadowOnObj']['saturation'] = camera.shadowSaturation
        config['shadowOnObj']['value'] = camera.shadowValue
        print("all of config has been saved")
        with open('./config.json', 'w') as f:
            json.dump(config, f)
    else:
        print("save-config channel has not key:", pyObj)

@socketio.on('capture')
def capture_handle(jsonData):
    pyObj = json.loads(jsonData)
    if pyObj['capture'] == True:
        camera.captureAll()           #capture pic to directory
    else:
        print("capture channel has not key:", pyObj)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)

camera.cap.release()
print("process destroyed")
