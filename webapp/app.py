from flask import Flask, render_template, Response, request, send_from_directory, jsonify
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

global config

# load config
with open('./config.json', 'r') as f:
    config = json.load(f)

camera = camgrab.camgrab(config)
camera.threadGenFrames.do_run = False
if camera.threadGenFrames.is_alive():
    camera.threadGenFrames.stop()
# time.sleep(5)
# camera.gen_frames()

def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)

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
    global rawImage, diffImage
    result = {}
    jsonData = request.get_json()
    if request.method == 'POST':
        jsonData = request.get_json()
        print(jsonData)

        # match jsonData['browserEvent']:
            
        #     case 'loaded':
        #         camera.imgDiffBinTreshold = config['imgDiffBinTreshold']
        #         camera.imgAndBinTreshold =  config['imgAndBinTreshold']
        #         camera.medianBlur = config['medianBlur']
        #         print("loaded")

        #     case 'changeFeed':
        #         camera.imgDiffBinTreshold = config['imgDiffBinTreshold']
        #         camera.imgAndBinTreshold =  config['imgAndBinTreshold']
        #         camera.medianBlur = config['medianBlur']
        #         print("loaded")

        #     case 'changeProcessVal':
        #         camera.feedStatus = jsonData["feedStatus"]
        #         camera.imgDiffBinTreshold = jsonData['imgDiffBinTreshold']
        #         camera.imgAndBinTreshold = jsonData['imgAndBinTreshold']
        #         camera.medianBlur = jsonData['medianBlur']
        #         print("change process value")

        #     case 'capture':
        #         # camera.shotSetting()
        #         camera.captureAll()
        #         result['message'] = "success"
        #         return jsonify(result['message'])

        #     case 'params':
        #         jsonData = request.get_json()
        #         # write it back to the file
        #         with open('./config.json', 'w') as f:
        #             json.dump(merge(config, jsonData), f)
        #         result['message'] = "success"

        #     case 'closed':
        #         # camera.camRelease()
        #         print("closed")

        #     case 'feedStatus':
        #         subtract_background_feed = jsonData["feed"]
        #         # subtract_background_feed = jsonData["feedStatus"]["subtractBackground"]

        if  jsonData["browserEvent"] == "loaded":
            camera.imgDiffBinTreshold = config['imgDiffBinTreshold']
            camera.imgAndBinTreshold =  config['imgAndBinTreshold']
            camera.medianBlur = config['medianBlur']
            print("loaded")

        elif jsonData["browserEvent"] == "changeFeed":
            camera.feedStatus = jsonData["feedStatus"]
            print("change feed")

        elif jsonData["browserEvent"] == "changeProcessVal":
            camera.feedStatus = jsonData["feedStatus"]
            camera.imgDiffBinTreshold = jsonData['imgDiffBinTreshold']
            camera.imgAndBinTreshold = jsonData['imgAndBinTreshold']
            camera.medianBlur = jsonData['medianBlur']
            print("change process value")

        elif jsonData["browserEvent"] == "capture":
            # camera.shotSetting()
            camera.captureAll()
            result['message'] = "success"
            return jsonify(result['message'])

        elif jsonData["browserEvent"] == "params":
            jsonData = request.get_json()
            # write it back to the file
            with open('./config.json', 'w') as f:
                json.dump(merge(config, jsonData), f)
            result['message'] = "success"

        elif jsonData["browserEvent"] == "closed":
            # camera.camRelease()
            print("closed")

        elif jsonData["browserEvent"] == "feedStatus": 
            subtract_background_feed = jsonData["feed"]
            # subtract_background_feed = jsonData["feedStatus"]["subtractBackground"]

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # return Response(camera.thread_raw_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    if not camera.threadGenFrames.is_alive():
        camera.threadGenFrames.start()
    return Response(camera.raw_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/subtract_background')
def subtract_background():
    return Response(camera.subtract_background_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/config_feed')
# def config_feed():
#     # return Response(camera.thread_process_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
#     return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

camera.cap.release()
print("process destroyed")
