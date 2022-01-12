// var jsonData = {
//     imgDiffBinTreshold: parseInt(subtractTreshVal.value),
//     imgAndBinTreshold: parseInt(imgAndTreshVal.value),
//     medianBlur: parseInt(medBlurVal.value),
//     objShadowTresholdVal: parseInt(objShadowTreshVal.value),
//     browserEvent: "normal",
//     feedStatus: "rawImage"
// };


jsonData = {
    subtractTreshVal: parseInt(subtractTreshVal.value),
    imgAndBinTreshold: parseInt(imgAndTreshVal.value),
    medianBlur: parseInt(medBlurVal.value),
    objShadowTreshVal: parseInt(objShadowTreshVal.value)
}

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
            if(range.id === "subtractTreshVal"){
                subtractTreshValText.value = range.value;
                jsonData.subtractTreshVal = parseInt(range.value);
                socket.emit('process-value', JSON.stringify(jsonData))
            }
            else if (range.id === "imgAndTreshVal"){
                imgAndTreshValText.value = range.value;
                jsonData.imgAndBinTreshold =parseInt(range.value);
                socket.emit('process-value', JSON.stringify(jsonData))
            }
            else if (range.id === "medBlurVal"){
                medBlurValText.value = range.value;
                jsonData.medBlurVal = parseInt(range.value);
                socket.emit('process-value', JSON.stringify(jsonData))
            }
            else if (range.id === "objShadowTreshVal"){
                objShadowTreshValText.value = range.value;
                jsonData.objShadowTreshVal = parseInt(range.value);
                socket.emit('process-value', JSON.stringify(jsonData))
            }
            
        }
    )
);

var texts = document.querySelectorAll('input[type=text]');
texts.forEach(
    text => text.addEventListener('input', () => {
            // console.log(range.id);
            // jsonData.browserEvent = "changeProcessVal";
            if(text.id === "subtractTreshValText"){
                subtractTreshVal.value = text.value;
                // jsonData.imgDiffBinTreshold = parseInt(text.value);
            }
            else if (text.id === "imgAndTreshValText"){
                imgAndTreshVal.value = text.value;
                // jsonData.imgAndTreshold = parseInt(text.value);
            }
            else if (text.id === "medBlurValText"){
                medBlurVal.value = text.value;
                // jsonData.medianBlur = parseInt(text.value);
            }
            else if (text.id === "objShadowTreshValText"){
                objShadowTreshVal.value = text.value;
                // jsonData.objShadowTresholdVal = parseInt(text.value);
            }
            // postjsonServ(jsonData);
            // jsonData.browserEvent = "normal";
        }
    )
);


var radios = document.querySelectorAll('input[type=radio]');
radios.forEach(
    radio => radio.addEventListener('change', () => {
            socket.emit('feed-status', JSON.stringify({ feedStatus : radio.value }))
        }
    )
);

function saveCapture(){
    socket.emit('save-config', JSON.stringify({ capture : true }))
}

function saveParams(){
    socket.emit('save-config', JSON.stringify({ saveParams : true }))
}

document.addEventListener('DOMContentLoaded', (event) => {
    // subtractTreshValText.value = subtractTreshVal.value;
    // objShadowTreshValText.value = objShadowTreshVal.value;
    // medBlurValText.value = medBlurVal.value;
    // jsonData.browserEvent = "loaded";
    // postjsonServ(jsonData);
    socket.emit('message', "loaded")
})

window.addEventListener('beforeunload', function (e) {
    jsonData.browserEvent = "closed";
    // postjsonServ(jsonData);
    // e.preventDefault();
    // e.returnValue = '';
    // alert("Fire");
});
