var subTreshVal = document.getElementById("subTreshVal"),
    subTreshValText = document.getElementById("subTreshValText");

var jsonData = {
    imgDiffBinTreshold: parseInt(subTreshVal.value),
    imgAndBinTreshold: parseInt(imgAndTreshVal.value),
    medianBlur: parseInt(medBlurVal.value),
    objShadowTresholdVal: parseInt(objShadowTreshVal.value),
    browserEvent: "normal",
    feedStatus: "rawImage"
};

// // Background Subtract Threshold
// subTreshVal.oninput = function () {
//     // postServ('/requests', 'subTreshVal', subTreshVal.value);
//     jsonData.subtractThesholdVal = subTreshVal.value;
//     subTreshValText.value = subTreshVal.value;
//     postjsonServ(jsonData);
// }
// subTreshValText.oninput = function () {
//     subTreshVal.value = subTreshValText.value;
// }

// // Median Blur
// var medBlurVal = document.getElementById("medBlurVal"),
//     medBlurValText = document.getElementById("medBlurValText");

// medBlurVal.oninput = function () {
//     // postServ('/requests', 'subTreshVal', medBlurVal.value);
//     medBlurValText.value = medBlurVal.value;
// }
// medBlurValText.oninput = function () {
//     medBlurVal.value = medBlurValText.value;
// }

// // Object Shadow Threshold
// var objShadowTreshVal = document.getElementById("objShadowTreshVal"),
//     objShadowTreshValText = document.getElementById("objShadowTreshValText");

// objShadowTreshVal.oninput = function () {
//     // postServ('/requests', 'subTreshVal', objShadowTreshVal.value);
//     objShadowTreshValText.value = objShadowTreshVal.value;
// }
// objShadowTreshValText.oninput = function () {
//     objShadowTreshVal.value = objShadowTreshValText.value;
// }

var ranges = document.querySelectorAll('input[type=range]');
ranges.forEach(
    range => range.addEventListener('input', () => {
            // console.log(range.id);
            jsonData.browserEvent = "changeProcessVal";
            if(range.id == "subTreshVal"){
                subTreshValText.value = range.value;
                jsonData.imgDiffBinTreshold = parseInt(range.value);
            }
            else if (range.id == "imgAndTreshVal"){
                imgAndTreshValText.value = range.value;
                jsonData.imgAndBinTreshold = parseInt(range.value);
            }
            else if (range.id == "medBlurVal"){
                medBlurValText.value = range.value;
                jsonData.medianBlur = parseInt(range.value);
            }
            else if (range.id == "objShadowTreshVal"){
                objShadowTreshValText.value = range.value;
                jsonData.objShadowTresholdVal = parseInt(range.value);
            }
            postjsonServ(jsonData);
            jsonData.browserEvent = "normal";
        }
    )
);

var texts = document.querySelectorAll('input[type=text]');
texts.forEach(
    text => text.addEventListener('input', () => {
            // console.log(range.id);
            jsonData.browserEvent = "changeProcessVal";
            if(text.id == "subTreshValText"){
                subTreshVal.value = text.value;
                jsonData.imgDiffBinTreshold = parseInt(text.value);
            }
            else if (text.id == "imgAndTreshValText"){
                imgAndTreshVal.value = text.value;
                jsonData.imgAndBinTreshold = parseInt(text.value);
            }
            else if (text.id == "medBlurValText"){
                medBlurVal.value = text.value;
                jsonData.medianBlur = parseInt(text.value);
            }
            else if (text.id == "objShadowTreshValText"){
                objShadowTreshVal.value = text.value;
                jsonData.objShadowTresholdVal = parseInt(text.value);
            }
            postjsonServ(jsonData);
            jsonData.browserEvent = "normal";
        }
    )
);


var radios = document.querySelectorAll('input[type=radio]');
radios.forEach(
    radio => radio.addEventListener('change', () => {
            // alert("radio.value");
            // if(radio.value == "subtractBackground"){
            //     jsonData.feedStatus.subtractBackground = ;
            // }
            jsonData.browserEvent = "changeFeed";
            jsonData.feedStatus = radio.value;
            postjsonServ(jsonData);
            jsonData.browserEvent = "normal";
        }
    )
);

function saveCapture(){
    jsonData.browserEvent = "capture";
    postjsonServ(jsonData);
    jsonData.browserEvent = "normal";
}

function saveParams(){
    jsonData.browserEvent = "params";
    postjsonServ(jsonData);
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