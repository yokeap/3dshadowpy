    var exposure = document.getElementById("expVal"),
        brightness = document.getElementById("brightnessVal"),
        contrast = document.getElementById("contrastVal"),
        hue = document.getElementById("hueVal"),
        saturation = document.getElementById("saturationVal"),
        sharpness = document.getElementById("sharpnessVal");

    var exposureText = document.getElementById("expValText"),
        brightnessText = document.getElementById("brightnessValText"),
        contrastText = document.getElementById("contrastValText"),
        hueText = document.getElementById("hueValText"),
        saturationText = document.getElementById("saturationValText"),
        sharpnessText = document.getElementById("sharpnessValText");

    var jsonData = {
        exposure : parseInt(exposure.value),
        brightness : parseInt(brightness.value),
        contrast : parseInt(contrast.value),
        hue : parseInt(hue.value),
        saturation : parseInt(saturation.value),
        sharpness : parseInt(sharpness.value),
        browserEvent : "closed"
    };

    exposure.oninput = function() {
        jsonData.exposure = parseInt(exposure.value);
        exposureText.value = exposure.value;
        postjsonServ("/config", jsonData);
    } 

    brightness.oninput = function() {
        jsonData.brightness = parseInt(brightness.value);
        brightnessText.value = brightness.value;
        postjsonServ("/config", jsonData);
    } 

    contrast.oninput = function() {
        jsonData.contrast = parseInt(contrast.value);
        contrastText.value = contrast.value;
        postjsonServ("/config", jsonData);
    } 

    hue.oninput = function() {
        jsonData.hue = parseInt(hue.value);
        hueText.value = hue.value;
        postjsonServ("/config", jsonData);
    } 

    saturation.oninput = function() {
        jsonData.saturation = parseInt(saturation.value);
        saturationText.value = saturation.value;
        postjsonServ("/config", jsonData);
    } 
    
    sharpness.oninput = function() {
        jsonData.sharpness = parseInt(sharpness.value);
        sharpnessText.value = sharpness.value;
        postjsonServ("/config", jsonData);
    } 

    exposureText.oninput = function() {
        jsonData.exposure = exposureText.value;
        exposure.value  = exposureText.value;
        postjsonServ("/config", jsonData);
    } 
    
    brightnessText.oninput = function() {
        jsonData.brightness = brightnessText.value;
        brightness.value  = brightnessText.value;
        postjsonServ("/config", jsonData);
    } 
    
    contrastText.oninput = function() {
        jsonData.contrast = contrastText.value;
        contrast.value  = contrastText.value;
        postjsonServ("/config", jsonData);
    } 
    
    hueText.oninput = function() {
        jsonData.hue = hueText.value;
        hue.value  = hueText.value;
        postjsonServ("/config", jsonData);
    } 
    
    saturationText.oninput = function() {
        jsonData.saturation = saturationText.value;
        saturation.value  = saturationText.value;
        postjsonServ("/config", jsonData);
    } 

    sharpnessText.oninput = function() {
        jsonData.sharpness = sharpnessText.value;
        sharpness.value  = sharpnessText.value;
        postjsonServ("/config", jsonData);
    }

    function saveConfig(){
        var jsonConfig = {
            "width": 1600,
            "height": 1200,
            "exposure": parseInt(exposure.value),
            "brightness": parseInt(brightness.value),
            "contrast": parseInt(contrast.value),
            "hue": parseInt(hue.value),
            "saturation": parseInt(saturation.value),
            "sharpness": parseInt(sharpness.value)
        }
        postjsonServ("/config-save", jsonConfig);
    }

    function loadDefault(){
        jsonData.browserEvent = "config-load";
        postjsonServ("/config", jsonData);
        jsonData.browserEvent = "normal";
    }

    function saveCapture(){
        jsonData.browserEvent = "capture";
        postjsonServ("/config", jsonData);
        jsonData.browserEvent = "normal";
    }

    function setAllParams(jsonVal){
        exposure.value = jsonVal.exposure
        brightness.value = jsonVal.brightness;
        contrast.value = jsonVal.constrastVal;
        hue.value = jsonVal.hue;
        saturation.value = jsonVal.saturation;
        sharpness.value = jsonVal.sharpness;

        exposureText.value = jsonVal.exposure
        brightnessText.value = jsonVal.brightness;
        contrastText.value = jsonVal.contrast;
        hueText.value = jsonVal.hue;
        saturationText.value = jsonVal.saturation;
        sharpnessText.value = jsonVal.sharpness;

    }
    
    document.addEventListener('DOMContentLoaded', (event) => {
        exposureText.value = exposure.value;
        brightnessText.value = brightness.value
        contrastText.value = contrast.value 
        hueText.value = hue.value
        saturationText.value = saturation.value
        sharpnessText.value = sharpness.value
        jsonData.browserEvent = "loaded";
        postjsonServ("/config", jsonData);
        jsonData.browserEvent = "normal";
    })
    
    window.addEventListener('beforeunload', function (e) {
        jsonData.browserEvent = "closed";
        // postjsonServ("/config", jsonData);
        // e.preventDefault();
        // e.returnValue = '';
        // alert("Fire");
    });
    
    




    
    