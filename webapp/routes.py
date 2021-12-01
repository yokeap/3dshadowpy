from flask import Flask, render_template, Response, request, Blueprint, jsonify

routes = Blueprint('routes', __name__, template_folder='./view', static_folder='./view')

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
            # camera.setConfig(result)
            # jsonTemp = config
            # jsonTemp["event"] = "loaded"
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
    result = {}
    jsonData = request.get_json()
    if request.method == 'POST':
        jsonData = request.get_json()
        print(jsonData)
        if jsonData["browserEvent"] == "changeFeed":
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
            camOpen = False
            print("closed")

        elif jsonData["browserEvent"] == "feedStatus": 
            # subtract_background_feed = jsonData["feed"]
            subtract_background_feed = jsonData["feedStatus"]["subtractBackground"]

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(camera.gen_frames("process"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/config_feed')
def config_feed():
    return Response(camera.gen_frames("config"), mimetype='multipart/x-mixed-replace; boundary=frame')