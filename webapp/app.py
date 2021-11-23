from flask import Flask, render_template, Response, request, send_from_directory, jsonify
from src import camgrab
from jsonmerge import merge
import cv2
import sys
import json

app = Flask(__name__, template_folder='./view', static_folder='./view')

global config

# load config
with open('./config.json', 'r') as f:
    config = json.load(f)

camera = camgrab.camgrab(config)

# main route


@app.route('/')
def index():
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
            result = camera.getConfig()
            camera.setConfig(result)
            return jsonify(result)
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
    global subtract_background_feed
    subtract_background_feed = False
    result = {}
    if request.method == 'POST':
        jsonData = request.get_json()
        print(jsonData)
        if jsonData["browserEvent"] == "capture":
            # camera.shotSetting()
            result['message'] = "success"
            return jsonify(result['message'])
        if jsonData["browserEvent"] == "closed":
            camOpen = False
            print("closed")
        if jsonData["browserEvent"] == "feedStatus": 
            # subtract_background_feed = jsonData["feed"]
            subtract_background_feed = jsonData["feedStatus"]["subtractBackground"]

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(camera.gen_frames("raw"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/subtract_background')
def subtract_background():
    return Response(camera.gen_frames("gray"), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

camera.cap.release()
print("process destroyed")
