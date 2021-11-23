var subTreshVal = document.getElementById("subTreshVal"),
    subTreshValText = document.getElementById("subTreshValText");

var jsonData = {
    subtractThesholdVal: subTreshVal.value,
    browserEvent: "normal",
    feedStatus: {
        subtractBackground: false
    }
};

// Background Subtract Threshold
subTreshVal.oninput = function () {
    // postServ('/requests', 'subTreshVal', subTreshVal.value);
    jsonData.subtractThesholdVal = subTreshVal.value;
    subTreshValText.value = subTreshVal.value;
    postjsonServ(jsonData);
}
subTreshValText.oninput = function () {
    subTreshVal.value = subTreshValText.value;
}

// Object Shadow Threshold
var objShadowTreshVal = document.getElementById("objShadowTreshVal"),
    objShadowTreshValText = document.getElementById("objShadowTreshValText");

objShadowTreshVal.oninput = function () {
    // postServ('/requests', 'subTreshVal', objShadowTreshVal.value);
    objShadowTreshValText.value = objShadowTreshVal.value;
}
objShadowTreshValText.oninput = function () {
    objShadowTreshVal.value = objShadowTreshValText.value;
}

// Median Blur
var medBlurVal = document.getElementById("medBlurVal"),
    medBlurValText = document.getElementById("medBlurValText");

medBlurVal.oninput = function () {
    // postServ('/requests', 'subTreshVal', medBlurVal.value);
    medBlurValText.value = medBlurVal.value;
}
medBlurValText.oninput = function () {
    medBlurVal.value = medBlurValText.value;
}

function swtRawImage_onChange() {
    if (document.getElementById('swtRawImage').checked) {
        document.getElementById("img-raw").style.display = 'block';
    }
    else {
        document.getElementById("img-subtractBg").style.display = 'none';
    }
}

function swtSubtractBackground_onChange() {
    jsonData.browserEvent = "feedStatus"
    if (document.getElementById('swtSubtractBackground').checked) {
        document.getElementById("img-subtractBg").style.display = 'block';

        jsonData.feedStatus.subtractBackground = true;
    }
    else {
        document.getElementById("img-subtractBg").style.display = 'block';
        jsonData.feedStatus.subtractBackground = false;
    }
    postjsonServ(jsonData);
    jsonData.browserEvent = "normal"
}

function swtBinaryImage_onChange() {
    if (document.getElementById('swtBinaryImage').checked) {
        // push subtract background to img tag
        document.getElementById("img-binary").style.display = 'block';
    }
    else {
        // remove or hidden img tag
        document.getElementById("img-binary").style.display = 'none';
    }
}

function swtAndImage_onChange() {
    if (document.getElementById('swtAndImage').checked) {
        // push subtract background to img tag
        document.getElementById("img-and").style.display = 'block';
    }
    else {
        // remove or hidden img tag
        document.getElementById("img-and").style.display = 'none';
    }
}

function swtMorphology_onChange() {
    if (document.getElementById('swtMorphology').checked) {
        // push subtract background to img tag
        document.getElementById("img-morphology").style.display = 'block';
    }
    else {
        // remove or hidden img tag
        document.getElementById("img-morphology").style.display = 'none';
    }
}

function swtObjResultSegment_onChange() {
    if (document.getElementById('swtObjResultSegment').checked) {
        // push subtract background to img tag
        document.getElementById("img-resultSegment").style.display = 'block';
    }
    else {
        // remove or hidden img tag
        document.getElementById("img-resultSegment").style.display = 'none';
    }
}

function swtObjImage_onChange() {
    if (document.getElementById('swtObjImage').checked) {
        // push subtract background to img tag
        document.getElementById("img-obj").style.display = 'block';
    }
    else {
        // remove or hidden img tag
        document.getElementById("img-obj").style.display = 'none';
    }
}

function swtShadowImage_onChange() {
    if (document.getElementById('swtShadowImage').checked) {
        // push subtract background to img tag
        document.getElementById("img-shadow").style.display = 'block';
    }
    else {
        // remove or hidden img tag
        document.getElementById("img-shadow").style.display = 'none';
    }
}

function saveCapture(){
    jsonData.browserEvent = "capture";
    postjsonServ("/config", jsonData);
    jsonData.browserEvent = "normal";
}

document.addEventListener('DOMContentLoaded', (event) => {
    subTreshValText.value = subTreshVal.value;
    objShadowTreshValText.value = objShadowTreshVal.value;
    medBlurValText.value = medBlurVal.value;

    jsonData.browserEvent = "loaded";
    postjsonServ(jsonData);
})

window.addEventListener('beforeunload', function (e) {
    jsonData.browserEvent = "closed";
    postjsonServ(jsonData);
    // e.preventDefault();
    // e.returnValue = '';
    // alert("Fire");
});