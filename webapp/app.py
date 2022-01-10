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

app = Flask(__name__, template_folder='./view', static_folder='./view')
socketio = SocketIO(app)

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


@app.route('/requests', methods=['POST', 'GET'])
def recvHandler():
    return render_template('index.html')   

@app.route('/raw_feed')
def raw_feed():
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

# @app.route('/imgroi')
# def imgroi():
#     return Response(camera.img)

# @app.route('/config_feed')
# def config_feed():
#     # return Response(camera.thread_process_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
#     return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route("/stream")
# def stream():
#     print("stream")
#     result = {}
#     def generate():
#         # while True:
#         # yield "{message: %s}" % ("success")
#             # sleep(1)
#         # for i in range(500):
            
#         #     sleep(1)
#         result['message'] = "success"
#         return json.dumps(result)


#     return Response(generate(), mimetype="application/json")

# @app.route("/stream", methods=['POST', 'GET'])
# def stream():
#     # jsonData = request.get_json()
#     print("Stream")
#     return Response(camera.hsv_feed(), mimetype="application/json")

@socketio.on('connect')
def connect_event():
    camera.imgDiffBinTreshold = config['imgDiffBinTreshold']
    camera.imgAndBinTreshold =  config['imgAndBinTreshold']
    camera.medianBlur = config['medianBlur']
    print('socket has been connected')

@socketio.on('disconnect')
def disconnect_event():
    print('socket has been disconnected')

@socketio.on('feed-status')
def fedd_status_handle(jsonData):
    pyObj = json.loads(jsonData)
    camera.feedStatus = pyObj["feedStatus"]
    print("main streaming has been changed to ", pyObj["feedStatus"])

@socketio.on('process-value')
def process_value_handle(jsonData):
    pyObj = json.loads(jsonData)
    camera.imgDiffBinTreshold = jsonData['subtractTreshVal']
    camera.imgAndBinTreshold = jsonData['imgAndBinTreshold']
    camera.medianBlur = jsonData['medianBlur']
    print("main streaming has been changed to ", pyObj )


@socketio.on('slider-obj-hsv')
def slider_obj_hsv_event(jsonData):
    pyObj = json.loads(jsonData)
    # print('received json: ' + str(json))
    # print(pyObj['objH'][0])

@socketio.on('save-config')
def save_config_handle(jsonData):
    pyObj = json.loads(jsonData)
    if pyObj['saveParams'] == True:
        print("all of config has been saved")
        with open('./config.json', 'w') as f:
            json.dump(merge(config, jsonData), f)

@socketio.on('capture')
def capture_handle(jsonData):
    pyObj = json.loads(jsonData)
    if pyObj['capture'] == True:
        camera.captureAll()           #capture pic to directory

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)

camera.cap.release()
print("process destroyed")
